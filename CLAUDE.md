# CLAUDE.md

이 파일은 이 저장소에서 작업하는 AI 어시스턴트를 위한 가이드입니다.
**반드시 전체를 읽고 작업하세요.** 특히 디자인 토큰 규칙과 컴포넌트 패턴은 절대 원칙입니다.

---

## 프로젝트 개요

[ucpwang.github.io](https://ucpwang.github.io)에 GitHub Pages로 호스팅되는 개인 블로그 사이트입니다.

- **프레임워크**: Astro (정적 사이트 생성)
- **스타일**: CSS Custom Properties 기반 디자인 시스템 (토큰 우선)
- **콘텐츠**: Astro Content Collections (Markdown)
- **배포**: GitHub Actions → GitHub Pages (master 브랜치 push 시 자동 빌드)

---

## 저장소 구조

```
ucpwang.github.io/
├── .claude/
│   └── settings.json              # Claude Code 권한 + hooks (자동 prettier)
├── .github/
│   └── workflows/
│       └── deploy.yml             # Astro 빌드 → GitHub Pages 배포
├── scripts/
│   └── verify.py                  # 전체 기능 검증 체크리스트 (배포 전 필수 실행)
├── src/
│   ├── components/
│   │   ├── BaseHead.astro         # <head> 공통 (메타, 폰트, CSS 임포트)
│   │   ├── Header.astro           # 사이트 헤더 / 네비게이션
│   │   ├── Footer.astro           # 사이트 푸터
│   │   ├── PostCard.astro         # 블로그 목록 카드
│   │   └── Tag.astro              # 포스트 태그
│   ├── content/
│   │   ├── config.ts              # Content Collections 스키마
│   │   └── blog/                  # 블로그 포스트 (.md 파일들)
│   ├── layouts/
│   │   ├── BaseLayout.astro       # 공통 레이아웃 (Header + Footer)
│   │   └── PostLayout.astro       # 블로그 포스트 레이아웃
│   ├── pages/
│   │   ├── index.astro            # 홈 (최신 포스트 목록)
│   │   ├── search.astro           # 전문 검색 (Pagefind)
│   │   ├── about.astro            # 소개 페이지
│   │   └── blog/
│   │       ├── index.astro        # 전체 포스트 목록 + 태그 클라우드
│   │       ├── [...slug].astro    # 개별 포스트 렌더링
│   │       └── tag/
│   │           └── [tag].astro    # 태그별 필터링 페이지
│   ├── utils/
│   │   └── tag.ts                 # 태그 슬러그 변환 유틸 (tagToSlug, slugToTag)
│   └── styles/
│       ├── tokens.css             # 디자인 토큰 → CSS 변수 (여기서만 값 정의)
│       ├── global.css             # 리셋 + 글로벌 타이포그래피
│       └── prose.css              # 마크다운 본문 스타일
├── public/
│   ├── favicon.svg                # 사이트 파비콘
│   └── images/                    # 정적 이미지
├── design-tokens/
│   └── tokens.json                # 디자인 토큰 단일 소스 (tokens.css와 동기화)
├── archive/                       # 구 Strapdown.js 포스트 (참조용 보존)
├── astro.config.mjs
├── package.json
├── tsconfig.json
└── .prettierrc
```

---

## 디자인 시스템 규칙 (절대 원칙)

### 1. 토큰 사용 강제

**색상, 간격, 폰트, 그림자를 절대 하드코딩하지 마세요.**
항상 CSS 변수를 사용합니다:

```css
/* WRONG */
color: #1a1a1a;
font-size: 1.125rem;
margin-top: 24px;

/* RIGHT */
color: var(--color-text-primary);
font-size: var(--text-lg);
margin-top: var(--space-6);
```

### 2. 토큰 참조 순서

1. `design-tokens/tokens.json` — 단일 소스 (값 변경 시 여기를 수정)
2. `src/styles/tokens.css` — CSS 변수로 변환 (tokens.json과 동기화 유지)
3. 컴포넌트 `.astro` 파일의 `<style>` — 변수만 사용

### 3. 사용 가능한 토큰 목록

**Color**

```
--color-brand           브랜드 메인 색상
--color-brand-light     브랜드 밝은 변형
--color-brand-dark      브랜드 어두운 변형
--color-text-primary    주 텍스트
--color-text-secondary  보조 텍스트
--color-text-muted      흐린 텍스트
--color-bg-base         기본 배경
--color-bg-elevated     카드/요소 배경
--color-bg-code         코드 블록 배경
--color-border          기본 테두리
--color-border-strong   강조 테두리
```

**Typography**

```
--font-heading          제목용 폰트 패밀리
--font-body             본문용 폰트 패밀리
--font-mono             코드/모노스페이스 폰트
--text-xs  --text-sm  --text-base  --text-lg  --text-xl
--text-2xl  --text-3xl  --text-4xl
--font-normal  --font-medium  --font-semibold  --font-bold
--leading-tight  --leading-normal  --leading-relaxed
```

**Spacing**

```
--space-1   0.25rem    --space-2   0.5rem
--space-3   0.75rem    --space-4   1rem
--space-6   1.5rem     --space-8   2rem
--space-12  3rem       --space-16  4rem
--space-24  6rem
```

**Other**

```
--radius-sm  --radius-md  --radius-lg  --radius-full
--shadow-sm  --shadow-md  --shadow-lg
--transition-fast  --transition-base  --transition-slow
```

---

## Astro 컴포넌트 패턴

### 컴포넌트 파일 구조

```astro
---
// 1. 임포트
import type { CollectionEntry } from 'astro:content';

// 2. Props 타입 정의 (항상 명시)
interface Props {
  title: string;
  date: Date;
  description?: string;
}

// 3. Props 구조분해
const { title, date, description } = Astro.props;
---

<!-- 4. 템플릿 -->
<article class="post-card">
  <h2>{title}</h2>
  {description && <p>{description}</p>}
</article>

<!-- 5. 스타일 (토큰 변수만 사용) -->
<style>
  .post-card {
    background: var(--color-bg-elevated);
    border-radius: var(--radius-md);
    padding: var(--space-6);
  }
</style>
```

### 네이밍 규칙

- 컴포넌트 파일: `PascalCase.astro` (예: `PostCard.astro`)
- 페이지 파일: `kebab-case.astro` 또는 `[param].astro`
- CSS 클래스: `kebab-case` (예: `.post-card`, `.site-header`)
- CSS 변수: `--category-name` 형식 (예: `--color-brand`, `--space-4`)

### 레이아웃 사용

모든 페이지는 반드시 `BaseLayout.astro`를 사용합니다:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="페이지 제목" description="페이지 설명">
  <!-- 콘텐츠 -->
</BaseLayout>
```

---

## 블로그 포스트 추가 방법

### 1. 파일 생성

`src/content/blog/YYYY-MM-DD-slug.md` 형식으로 생성:

```markdown
---
title: '포스트 제목'
date: 2026-03-27
description: '포스트 요약 (카드/OG에 사용됨)'
tags: ['태그1', '태그2']
draft: false
---

본문 내용 (Markdown)
```

### 2. Content Collections 스키마 (필수 필드)

| 필드          | 타입     | 필수 | 설명                                    |
| ------------- | -------- | ---- | --------------------------------------- |
| `title`       | string   | ✅   | 포스트 제목                             |
| `date`        | date     | ✅   | 발행일 (YYYY-MM-DD)                     |
| `description` | string   | ✅   | 요약문                                  |
| `tags`        | string[] | -    | 태그 목록 (기본값 `[]`)                 |
| `draft`       | boolean  | -    | `true`면 빌드에서 제외 (기본값 `false`) |

### 3. 확인

```bash
npm run dev  # http://localhost:4321/blog 에서 확인
```

---

## 개발 명령어

```bash
npm run dev      # 개발 서버 시작 (http://localhost:4321)
npm run build    # 프로덕션 빌드 → dist/ (pagefind 인덱싱 포함)
npm run preview  # 빌드 결과물 미리보기 (http://localhost:4321)
npm run format   # prettier로 전체 파일 포맷
```

---

## 배포 전 검증 루프 (필수)

**어떤 기능을 추가/수정하든 배포 전에 반드시 검증 루프를 완료해야 합니다.**

```bash
npm run build && npm run preview -- --port 4321 &
sleep 3
python3 scripts/verify.py
kill %1
```

- `47/47 전체 통과`가 확인된 후에만 커밋·배포한다
- 실패 항목이 있으면 수정 → 재빌드 → 재검증 반복
- 검증 스크립트(`scripts/verify.py`)는 전체 기능을 커버하며, 새 기능 추가 시 해당 체크 항목도 함께 추가한다

---

## 배포

**자동 배포**: `master` 브랜치에 push하면 GitHub Actions가 자동으로:

1. `npm ci` → `npm run build` 실행
2. `dist/` 디렉토리를 GitHub Pages에 배포

**최초 설정 필요**: GitHub 저장소 Settings → Pages → Source를 "GitHub Actions"로 변경.

빌드 결과물(`dist/`)은 `.gitignore`에 포함되어 있어 커밋하지 않습니다.

---

## 브랜치 전략

- `master` — 프로덕션. push 시 자동 빌드+배포
- 기능 브랜치: `<출처>/설명-접미사` (예: `claude/add-about-page-XYZ`)
- 기능 완성 후 PR → master 병합

---

## 주의 사항

- `design-tokens/tokens.json`을 수정할 때는 `src/styles/tokens.css`도 동기화
- `src/styles/tokens.css`에서만 CSS 변수 값을 정의 — 다른 파일에서 값 정의 금지
- `public/` 디렉토리는 그대로 서빙됨 (빌드 과정 없음)
- `archive/` 디렉토리는 구 포스트 보존용 — 수정하지 말 것
- `jacobs_mac_house/` 디렉토리는 구 포트폴리오 — 건드리지 말 것
- `node_modules/`, `dist/`, `bower_components/`는 gitignore됨 — 커밋하지 말 것
- 태그 URL은 반드시 `tagToSlug()` (`src/utils/tag.ts`) 를 통해 생성 — 슬래시·공백 포함 태그(CI/CD 등) 대응
- 검색 페이지(`search.astro`)는 pagefind 인덱싱 대상 제외 필수 (`pagefindIgnore={true}`)
- 외부 라이브러리 CSS가 Svelte 스코프 선택자로 특이도를 높이는 경우, `!important` 대신 JS에서 런타임 style 주입 방식을 사용
