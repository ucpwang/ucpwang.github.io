#!/usr/bin/env python3
"""
사이트 전체 기능 검증 체크리스트
사용: npm run build && npm run preview & sleep 2 && python3 scripts/verify.py
"""
import urllib.request
import sys
import time
import os

BASE = os.environ.get("BASE", "http://localhost:4321")
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

print("\n══════════════════════════════════════")
print("  사이트 기능 검증 체크리스트")
print("══════════════════════════════════════\n")

# ── 1. 페이지 응답 상태 ──────────────────────────
print("① 페이지 로드 (HTTP 200)")
pages = ["/", "/blog", "/search", "/about",
         "/blog/2026-04-15-astro-design-system",
         "/blog/tag/css", "/blog/tag/ci-cd",
         "/blog/tag/github-actions"]
for p in pages:
    status, _ = fetch(p)
    check(p, status == 200, f"HTTP {status}")

# ── 2. 정적 에셋 ─────────────────────────────────
print("\n② 정적 에셋")
assets = ["/pagefind/pagefind-ui.css", "/pagefind/pagefind-ui.js",
          "/pagefind/pagefind.js", "/favicon.svg"]
for a in assets:
    status, body = fetch(a)
    min_size = 10 if a.endswith(".svg") else 100
    check(a, status == 200 and len(body) > min_size, f"HTTP {status}, {len(body)}B")

# ── 3. 홈페이지 ──────────────────────────────────
print("\n③ 홈페이지 (/)  ")
_, body = fetch("/")
check("Jacob.c 제목", "Jacob.c" in body)
check("최근 포스트 섹션", "최근 포스트" in body or "RECENT POSTS" in body)
check("포스트 카드 존재", "post-card" in body)
check("모든 포스트 보기 링크", "/blog" in body)
check("헤더 네비게이션 4개", body.count('site-header__nav-link') >= 4)
check("검색 링크 헤더에 존재", "/search" in body)
check("소개 링크 헤더에 존재", "/about" in body)
check("푸터 존재", "site-footer" in body)
check("GitHub 링크", "github.com/ucpwang" in body)

# ── 4. 블로그 인덱스 ─────────────────────────────
print("\n④ 블로그 인덱스 (/blog)")
_, body = fetch("/blog")
check("10개의 포스트", "10개의 포스트" in body)
check("태그 클라우드 존재", "tag-cloud" in body)
check("CSS 태그 링크", "/blog/tag/css" in body.lower())
check("포스트 카드 다수", body.count("post-card") >= 5)

# ── 5. 태그 페이지 ───────────────────────────────
print("\n⑤ 태그 페이지")
_, body = fetch("/blog/tag/css")
check("/blog/tag/css 로드", "CSS" in body and "포스트" in body)
check("블로그 back 링크", "← 블로그" in body or "/blog" in body)

_, body = fetch("/blog/tag/ci-cd")
check("/blog/tag/ci-cd 로드 (CI/CD 슬러그)", "CI/CD" in body or "포스트" in body)

_, body = fetch("/blog/tag/github-actions")
check("/blog/tag/github-actions 로드", "GitHub Actions" in body or "포스트" in body)

# ── 6. 포스트 상세 ───────────────────────────────
print("\n⑥ 포스트 상세 페이지")
_, body = fetch("/blog/2026-04-15-astro-design-system")
check("포스트 제목 렌더링", "디자인 시스템" in body)
check("읽기 시간 표시", "읽기" in body and "분" in body)
check("스크롤 진행 바", "reading-progress" in body)
check("태그 링크 존재", "/blog/tag/" in body)
check("목록으로 링크", "/blog" in body)
check("prose 클래스", "prose" in body)

# ── 7. 검색 페이지 ───────────────────────────────
print("\n⑦ 검색 페이지 (/search)")
_, body = fetch("/search")
check("검색 제목", "검색" in body)
check("pagefind CSS가 <head>에 로드", body.find("pagefind-ui.css") < body.find("</head>"))
check("pagefind 초기화 스크립트", "PagefindUI" in body or "pagefind-ui.js" in body)
check("</html> 이후 잔류 태그 없음", not body.strip().endswith(">") or
      body.rfind("</html>") > body.rfind("pagefind-ui.css"))

# ── 8. About 페이지 ──────────────────────────────
print("\n⑧ About 페이지 (/about)")
_, body = fetch("/about")
check("Jacob 이름", "Jacob" in body or "황유현" in body)
check("관심 분야 섹션", "관심 분야" in body or "지금 다루는 일들" in body or "interest" in body.lower())
check("LinkedIn 링크", "linkedin.com" in body)
check("이메일 링크", "mailto:" in body)

# ── 9. 다크 테마 CSS 변수 ────────────────────────
print("\n⑨ 다크 테마 CSS 변수 (빌드된 CSS)")
try:
    with open("dist/_astro/_slug_.Ztud8cIs.css") as f:
        css = f.read()
except:
    # 파일명이 다를 수 있으므로 glob
    import glob, os
    files = glob.glob("dist/_astro/*.css")
    css = ""
    for f in files:
        css += open(f).read()

check("배경색 #0f0f0f", "#0f0f0f" in css or "0f0f0f" in css)
check("브랜드 컬러 #c0c0c0", "#c0c0c0" in css or "c0c0c0" in css)
check("텍스트 #f0f0f0", "#f0f0f0" in css or "f0f0f0" in css)
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
