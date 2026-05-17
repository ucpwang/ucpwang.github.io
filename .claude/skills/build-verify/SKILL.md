---
name: build-verify
description: ucpwang.github.io의 배포 전 검증 루프 실행. npm run build + npm run preview + python3 scripts/verify.py를 순차 실행하여 전체 통과를 확인한다. 빌드 실행, 검증 실행, verify 돌려달라, 배포 전 점검, 전체 통과 확인 요청 시 트리거.
---

# build-verify — 빌드·검증 실행 가이드

CLAUDE.md의 "배포 전 검증 루프"를 자동화한다.

## 표준 실행 절차

```bash
# 1. 빌드 (pagefind 인덱싱 포함)
npm run build

# 2. preview 서버를 백그라운드로 띄움 (포트 4321)
npm run preview -- --port 4321 &
PREVIEW_PID=$!

# 3. preview 서버가 응답할 때까지 잠시 대기 (최대 10초)
for i in 1 2 3 4 5; do
  curl -fsS http://localhost:4321/ > /dev/null 2>&1 && break
  sleep 1
done

# 4. verify.py 실행 (자가발견형 — 검증 항목 수는 콘텐츠에 따라 동적 결정)
python3 scripts/verify.py
VERIFY_EXIT=$?

# 5. preview 서버 정리 — 반드시 수행
kill $PREVIEW_PID 2>/dev/null
wait $PREVIEW_PID 2>/dev/null

# 6. 종료 코드로 판정
exit $VERIFY_EXIT
```

**Bash 도구로 실행 시:** preview 서버는 `run_in_background: true`로 띄우고, `lsof -i :4321` 또는 `kill <PID>`로 정리. `kill %1`은 셸 상태가 명령 간 유지되지 않으므로 사용 금지 — 명시적 PID 사용.

## verify.py 자가발견 동작 원리

verify.py는 실행 시점에 `src/content/blog/*.md`를 글로빙하여 다음을 동적으로 결정한다:

- `draft: false`인 포스트 슬러그 목록 → ⑤ 포스트 상세 섹션 자동 생성
- 모든 포스트의 `tags` 합집합 → ⑥ 태그 페이지 섹션 자동 생성 (Python에서 `tagToSlug` 미러링)
- ④ 블로그 인덱스의 "N개의 포스트" 카운트도 발견된 수로 자동 비교

**중요:** 포스트 추가/삭제만으로 verify.py 본체를 수정할 필요 없음. 다음 경우에만 verify.py를 손본다:

- 새 페이지/라우트가 추가됨 (예: `/projects`, `/talks`)
- 새 기능 컴포넌트가 추가됨 (예: 댓글, 뉴스레터 폼)
- `src/utils/tag.ts:tagToSlug`의 변환 로직이 변경됨 → Python 미러도 함께 갱신

## verify.py 출력 파싱

verify.py 출력 형식:

```
══════════════════════════════════════
  사이트 기능 검증 (포스트 N개, 태그 M개)
══════════════════════════════════════

① 페이지 로드 (HTTP 200) — 기본 페이지
  ✓ /
  ✓ /blog
  ✗ /search  (HTTP 404)
...
══════════════════════════════════════
  결과: A/B 통과  (C개 실패)
══════════════════════════════════════
```

- 라인이 `✗`로 시작하면 실패 항목. 라벨과 detail을 추출.
- 마지막의 `결과: A/B 통과` 라인이 종합 판정. B는 콘텐츠에 따라 동적이므로 비교는 `A == B` 또는 종료 코드로 한다.
- 종료 코드: 전체 통과 시 0, 실패 시 1.

## 실패 시 원인 매핑

| 섹션            | 자주 실패하는 원인                                                                |
| --------------- | --------------------------------------------------------------------------------- |
| ① 기본 페이지   | 라우트 누락, `BaseLayout.astro` 변경                                              |
| ② 정적 에셋     | `pagefind` 인덱싱 실패 (`npm run build`가 인덱싱까지 수행하는지)                  |
| ③ 홈페이지      | `Header.astro`/`Footer.astro` 텍스트 변경, 빈 상태 메시지 텍스트 변경             |
| ④ 블로그 인덱스 | "N개의 포스트" 카운트 문구 형식 변경, `tag-cloud` 클래스 변경                     |
| ⑤ 포스트 상세   | `[...slug].astro` 변경, `PostLayout.astro` 클래스명 변경 (prose/reading-progress) |
| ⑥ 태그 페이지   | `tagToSlug()` 로직 변경 (Python 미러 미동기화 포함), `[tag].astro` 변경           |
| ⑦ 검색 페이지   | pagefind CSS/JS 로딩 순서, `pagefindIgnore` 누락                                  |
| ⑧ About         | `about.astro`의 핵심 텍스트(CISO/Jacob/황유현/linkedin/mailto) 삭제               |
| ⑨ 다크 테마 CSS | tokens.css의 핵심 컬러 변수 누락                                                  |

특정 검증 항목이 실패하면 verify.py 해당 라인을 함께 보고하여 author가 어떤 검증을 만족시켜야 하는지 명확히 한다.

## 빌드 실패 vs verify 실패 구분

- **빌드 실패** (`npm run build` 비-0 종료): 타입 오류, 스키마 위반(frontmatter 필드 누락 등), import 깨짐
  → verify.py까지 가지 않음. 빌드 로그의 첫 에러를 author에게 전달.
- **빌드 성공 + verify 실패**: 라우팅/렌더링/CSS 변수 문제
  → ✗ 항목 목록을 author에게 전달.

## 검증 항목 갱신

콘텐츠(포스트·태그) 변경은 verify.py를 손댈 일이 아니다. 다음 경우에만 verify.py 수정:

1. **새 라우트 추가** — ① 또는 새 섹션에 `check()` 추가
2. **새 컴포넌트의 구조적 노출 검증** — 해당 섹션에 셀렉터 체크 추가
3. **`tagToSlug` 로직 변경** — verify.py의 `tag_to_slug()` 미러 함수도 함께 동기

이 경우에도 절대 카운트(예: "47개")는 박지 않는다. 항상 `len(posts)` 같은 동적 값으로.

## verifier 에이전트가 출력할 보고서 형식

```markdown
# verifier 보고

## 판정

PASS (또는 BUILD_FAILED / VERIFY_FAILED)

## 빌드 결과

- 명령: npm run build
- 종료 코드: 0
- 빌드 시간: 12.3s

## verify.py 결과

- 발견된 포스트: N개, 태그: M개
- 총 검증 항목: B개
- 통과: A개
- 실패: C개

## 실패 항목 (있으면)

- ✗ /blog/tag/some-tag (HTTP 404) — 섹션 ⑥
  - 원인 추정: tagToSlug 로직 변경 후 Python 미러 미동기
  - author 수정 제안: scripts/verify.py:tag_to_slug() 함수 동기화
```

## 자주 발생하는 운영 이슈

- **포트 4321 점유**: `lsof -i :4321`로 확인. 사용자에게 보고 후 승인 받고 kill.
- **preview 응답 지연**: 빌드 결과물이 깨졌을 가능성. `dist/` 존재 여부 + `dist/index.html` 사이즈 확인.
- **pagefind 자산 누락**: `dist/pagefind/` 디렉토리 확인. 없으면 `npm run build`가 pagefind를 트리거하지 않음 → `package.json`의 build 스크립트 확인.
- **태그 페이지 404가 갑자기 발생**: `src/utils/tag.ts:tagToSlug` 변경 후 verify.py의 `tag_to_slug()` 미러를 동기화하지 않은 경우. 두 함수가 같은 입력에 같은 출력을 내야 한다.
