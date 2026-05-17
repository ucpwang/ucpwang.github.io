---
name: blog-post-author
description: ucpwang.github.io 블로그 포스트(`src/content/blog/*.md`)를 작성·수정할 때 사용한다. frontmatter 스키마, 파일명 컨벤션, 톤·구조 가이드, 태그 선택 기준, 코드 블록 작성 규칙을 담는다. 새 블로그 글, 포스트 보완, 메타데이터 수정, draft 관리 시 반드시 트리거.
---

# blog-post-author — 블로그 포스트 작성 가이드

`src/content/blog/` 하위 Markdown 파일을 작성·수정할 때 따르는 규칙.

## 파일 위치·네이밍

- 경로: `src/content/blog/`
- 파일명: `YYYY-MM-DD-slug.md` (예: `2026-05-17-view-transitions.md`)
  - 날짜는 발행 예정일. 미래 날짜도 허용.
  - slug는 영문 소문자 + 하이픈. 띄어쓰기/한글/언더스코어 금지.

## Frontmatter 스키마 (`src/content/config.ts`)

```yaml
---
title: '포스트 제목' # 필수, string
date: 2026-05-17 # 필수, YYYY-MM-DD
description: '카드/OG용 요약' # 필수, 1~2문장
tags: ['Astro', 'CI/CD'] # 선택, 기본 []
draft: false # 선택, true면 빌드 제외
---
```

**주의:**

- `description`은 홈/블로그 카드와 OG 메타에 노출된다. 추측성 표현 대신 글의 핵심을 한 줄로.
- `tags`는 배열. 단일 태그도 `['Astro']`처럼 배열로.
- 태그명은 사람이 읽는 형태(`'CI/CD'`, `'GitHub Actions'`). 슬러그 변환은 `tagToSlug()`가 한다 — frontmatter에는 원본 그대로.

## 톤·문체

기존 포스트 10개의 패턴(`src/content/blog/2025-*.md`, `2026-*.md`):

- **존댓말 X, 평어체 O** — "~다", "~한다" 형태
- 1인칭 사용 OK ("나는", "내가")
- 코드 예시는 짧고 자족적. 전체 파일을 붙여넣지 않는다.
- 단락은 짧게. 한 단락이 5~6줄 넘으면 끊는다.
- 첫 문단은 도입(왜 이 글인가). 마지막 문단은 결론/요점 재진술.

**새 포스트 작성 시 권장 절차:**

1. 같은 주제군의 기존 포스트 1~2개를 읽고 톤을 매칭한다.
2. 글의 골격을 (도입 → 본론 2~3 섹션 → 결론) 순서로 구성.
3. 코드 블록에는 언어 표기 (` ```ts `, ` ```css `).

## 태그 선택 기준

- 이미 존재하는 태그를 우선 재사용. 새 태그 신설은 보수적으로.
- 기존 태그 목록은 `src/content/blog/` 모든 frontmatter의 `tags`를 grep으로 확인.
- 슬래시 포함 태그(`'CI/CD'`)는 허용 — 라우팅은 `tagToSlug()`가 처리.

## 본문 구조 가이드

````markdown
---
title: '...'
date: ...
description: '...'
tags: [...]
---

도입부 단락. 왜 이 주제를 다루는가, 누가 읽으면 좋은가.

## 첫 번째 섹션

본문...

```ts
// 코드 예시 — 언어 표기 필수
const foo: number = 1;
```

## 두 번째 섹션

...

## 정리

요점 재진술. 다음 행동(다른 글 링크 등)이 있으면 여기서.
````

## draft 관리

- 작성 중인 글은 `draft: true`로 두면 빌드에서 제외된다.
- 발행 준비 완료 시 `draft: false`로 토글하거나 필드 자체 삭제 (기본값 false).
- `draft: true` 포스트는 verify.py에 카운트되지 않으므로 `npm run build` 후 `/blog` 페이지의 "N개의 포스트" 카운트가 변할 수 있음에 유의.

## 검증

작성 후 `verifier` 에이전트가 다음을 자동 확인:

1. 빌드 통과 (`npm run build`)
2. `/blog` 페이지의 포스트 카운트 갱신
3. 새 태그 추가 시 `/blog/tag/{slug}` 라우트 생성

## 자주 하는 실수

- 파일명 날짜와 frontmatter `date` 불일치 → 둘을 같은 날짜로
- `description` 누락 → 필수 필드, 빌드 실패
- 태그를 배열이 아닌 문자열로 작성 → 스키마 위반
- 슬러그에 한글 포함 → URL 인코딩 깨짐
