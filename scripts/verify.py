#!/usr/bin/env python3
"""
사이트 전체 기능 검증 (자가발견형)

src/content/blog/*.md를 파싱해 검증 대상(포스트 슬러그·태그)을 동적으로 결정한다.
콘텐츠가 추가·삭제되어도 이 스크립트는 수정할 필요 없다.

사용: npm run build && npm run preview -- --port 4321 & sleep 3 && python3 scripts/verify.py
"""
import urllib.request
import sys
import os
import glob
import re

BASE = os.environ.get("BASE", "http://localhost:4321")
BLOG_DIR = os.environ.get("BLOG_DIR", "src/content/blog")

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
results = []


def check(label, condition, detail=""):
    status = PASS if condition else FAIL
    results.append(condition)
    suffix = f"  ({detail})" if detail and not condition else ""
    print(f"  {status} {label}{suffix}")


def fetch(path):
    try:
        r = urllib.request.urlopen(f"{BASE}{path}", timeout=5)
        return r.status, r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return 0, str(e)


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if line.startswith("tags:"):
            arr = re.search(r"\[(.*)\]", line)
            if arr:
                fm["tags"] = re.findall(r"['\"]([^'\"]+)['\"]", arr.group(1))
            else:
                fm["tags"] = []
        elif line.startswith("draft:"):
            fm["draft"] = "true" in line.lower()
    return fm


def tag_to_slug(tag):
    """Mirror of src/utils/tag.ts:tagToSlug. 두 구현이 분기되지 않게 동기 유지 필요."""
    s = tag.lower()
    s = re.sub(r"[/\s]+", "-", s)
    s = re.sub(r"[^a-z0-9가-힣-]", "", s)
    s = re.sub(r"-+", "-", s)
    s = re.sub(r"^-|-$", "", s)
    return s


def discover_posts():
    posts = []
    for path in sorted(glob.glob(f"{BLOG_DIR}/*.md")):
        with open(path) as f:
            fm = parse_frontmatter(f.read())
        if fm.get("draft"):
            continue
        slug = os.path.splitext(os.path.basename(path))[0]
        posts.append({"slug": slug, "tags": fm.get("tags", [])})
    return posts


posts = discover_posts()
all_tags = sorted({t for p in posts for t in p["tags"]})

print("\n══════════════════════════════════════")
print(f"  사이트 기능 검증 (포스트 {len(posts)}개, 태그 {len(all_tags)}개)")
print("══════════════════════════════════════\n")

# ── ① 기본 페이지 응답 ──────────────────────────
print("① 페이지 로드 (HTTP 200) — 기본 페이지")
for p in ["/", "/blog", "/search", "/about"]:
    status, _ = fetch(p)
    check(p, status == 200, f"HTTP {status}")

# ── ② 정적 에셋 ─────────────────────────────────
print("\n② 정적 에셋")
for asset, min_size in [
    ("/pagefind/pagefind-ui.css", 100),
    ("/pagefind/pagefind-ui.js", 100),
    ("/pagefind/pagefind.js", 100),
    ("/favicon.svg", 10),
]:
    status, body = fetch(asset)
    check(asset, status == 200 and len(body) > min_size, f"HTTP {status}, {len(body)}B")

# ── ③ 홈페이지 구조 ─────────────────────────────
print("\n③ 홈페이지 (/)")
_, body = fetch("/")
check("Jacob.c 제목", "Jacob.c" in body)
check("헤더 네비게이션 4개", body.count("site-header__nav-link") >= 4)
check("블로그 링크", "/blog" in body)
check("검색 링크", "/search" in body)
check("소개 링크", "/about" in body)
check("푸터", "site-footer" in body)
check("GitHub 링크", "github.com/ucpwang" in body)
if posts:
    check("최근 포스트 섹션 렌더", 'class="post-card' in body)
else:
    check("빈 상태 메시지", "아직 작성된 포스트가 없습니다" in body)

# ── ④ 블로그 인덱스 (동적 카운트) ───────────────
print("\n④ 블로그 인덱스 (/blog)")
_, body = fetch("/blog")
check(f"{len(posts)}개의 포스트 카운트", f"{len(posts)}개의 포스트" in body)
if posts:
    check("태그 클라우드 요소 렌더", 'class="tag-cloud' in body)
    check("포스트 카드 다수 노출", body.count('class="post-card') >= 1)
else:
    check("태그 클라우드 요소 미렌더", 'class="tag-cloud' not in body)
    check("빈 상태 메시지", "아직 작성된 포스트가 없습니다" in body)

# ── ⑤ 포스트 상세 (자동 발견) ───────────────────
if posts:
    print(f"\n⑤ 포스트 상세 페이지 ({len(posts)}개)")
    for p in posts:
        status, _ = fetch(f"/blog/{p['slug']}")
        check(f"/blog/{p['slug']}", status == 200, f"HTTP {status}")
    # 임의의 한 포스트로 구조 체크 (가장 최근 = 정렬 마지막)
    _, body = fetch(f"/blog/{posts[-1]['slug']}")
    check("읽기 시간 표시", "읽기" in body and "분" in body)
    check("스크롤 진행 바 (reading-progress)", "reading-progress" in body)
    check("prose 본문 컨테이너", "prose" in body)
    check("태그 링크 존재", "/blog/tag/" in body)

# ── ⑥ 태그 페이지 (자동 발견) ───────────────────
if all_tags:
    print(f"\n⑥ 태그 페이지 ({len(all_tags)}개)")
    for t in all_tags:
        slug = tag_to_slug(t)
        status, body = fetch(f"/blog/tag/{slug}")
        check(f"/blog/tag/{slug}  ({t})", status == 200 and "포스트" in body, f"HTTP {status}")

# ── ⑦ 검색 페이지 ───────────────────────────────
print("\n⑦ 검색 페이지 (/search)")
_, body = fetch("/search")
check("검색 제목", "검색" in body)
check("pagefind CSS가 <head>에 로드", body.find("pagefind-ui.css") < body.find("</head>"))
check("pagefind 초기화 스크립트", "PagefindUI" in body or "pagefind-ui.js" in body)

# ── ⑧ About 페이지 ──────────────────────────────
print("\n⑧ About 페이지 (/about)")
_, body = fetch("/about")
check("Jacob 또는 황유현 이름", "Jacob" in body or "황유현" in body)
check("CISO 역할 표기", "CISO" in body)
check("LinkedIn 링크", "linkedin.com" in body)
check("이메일 링크", "mailto:" in body)

# ── ⑨ 다크 테마 CSS 변수 (빌드 결과물) ──────────
print("\n⑨ 다크 테마 CSS 변수")
files = glob.glob("dist/_astro/*.css")
css = "".join(open(f).read() for f in files)
check("배경색 #0f0f0f", "0f0f0f" in css)
check("브랜드 컬러 #c0c0c0", "c0c0c0" in css)
check("텍스트 #f0f0f0", "f0f0f0" in css)
check("CSS 토큰 변수 선언", "--color-brand" in css)

# ── 결과 요약 ────────────────────────────────────
total = len(results)
passed = sum(results)
failed = total - passed
print(f"\n══════════════════════════════════════")
print(f"  결과: {passed}/{total} 통과", end="")
if failed:
    print(f"  \033[31m({failed}개 실패)\033[0m")
else:
    print(f"  \033[32m(전체 통과)\033[0m")
print("══════════════════════════════════════\n")
sys.exit(0 if failed == 0 else 1)
