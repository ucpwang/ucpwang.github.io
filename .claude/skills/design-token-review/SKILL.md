---
name: design-token-review
description: Astro 블로그의 디자인 토큰 절대 원칙 위반을 검사할 때 사용. CSS에서 색상/간격/폰트/그림자/border-radius/transition이 하드코딩됐는지 grep으로 찾고, design-tokens/tokens.json과 src/styles/tokens.css의 동기화 여부를 확인한다. Astro 컴포넌트나 CSS 변경 후 검토할 때 반드시 트리거.
---

# design-token-review — 디자인 토큰 위반 검사

CLAUDE.md의 절대 원칙: **색상·간격·폰트·그림자·border-radius·transition을 하드코딩하지 않는다.** 항상 `var(--*)` 사용.

## 검사 항목

### 1. 하드코딩 색상 (HEX/rgb/hsl/색상명)

```bash
# HEX 색상 (단, tokens.json/tokens.css 자체는 제외)
grep -rn -E '#[0-9a-fA-F]{3,8}\b' src/ \
  --include='*.astro' --include='*.css' --include='*.svelte' --include='*.tsx' \
  | grep -v 'tokens.css'

# rgb()/rgba()/hsl()
grep -rn -E '(rgb|rgba|hsl|hsla)\s*\(' src/ \
  --include='*.astro' --include='*.css' \
  | grep -v 'tokens.css'
```

**예외 허용:**

- `tokens.css` 파일 자체 (변수 정의처)
- `transparent`, `currentColor`, `inherit` 같은 키워드 (이건 OK)

### 2. 하드코딩 spacing/font-size (px/rem/em 리터럴)

```bash
# CSS 속성 값으로 px/rem 직접 사용 — margin/padding/gap/font-size 등
grep -rn -E '(margin|padding|gap|font-size|line-height|width|height)\s*:\s*[0-9]+(\.[0-9]+)?(px|rem|em)' src/ \
  --include='*.astro' --include='*.css' \
  | grep -v 'tokens.css'
```

**예외 허용:**

- `0` / `0px` / `100%` / `auto` / `1fr` 같은 값
- 미디어 쿼리의 breakpoint (예: `@media (max-width: 768px)`)
- `1px` 라인 (`border: 1px solid var(--color-border)` — 1px은 토큰 미정의 시 허용)

### 3. 하드코딩 box-shadow / border-radius / transition

```bash
grep -rn -E '(box-shadow|border-radius|transition)\s*:' src/ \
  --include='*.astro' --include='*.css' \
  | grep -v 'var(--' \
  | grep -v 'tokens.css'
```

`var(--shadow-*)`, `var(--radius-*)`, `var(--transition-*)`를 쓰는지 확인.

### 4. tokens.json ↔ tokens.css 동기화

`design-tokens/tokens.json`이 변경됐으면 `src/styles/tokens.css`의 해당 변수도 같은 값으로 갱신됐는지 확인.

```bash
# 두 파일 동시 변경됐는지 git status로 확인
git diff --name-only HEAD | grep -E '(tokens\.json|tokens\.css)'
```

한쪽만 변경됐다면 CRITICAL. 다른 쪽도 함께 갱신 지시.

### 5. 사용 가능한 토큰 목록 (CLAUDE.md 참조)

**Color:** `--color-brand[/-light/-dark]`, `--color-text-{primary,secondary,muted}`, `--color-bg-{base,elevated,code}`, `--color-border[/-strong]`
**Typography:** `--font-{heading,body,mono}`, `--text-{xs,sm,base,lg,xl,2xl,3xl,4xl}`, `--font-{normal,medium,semibold,bold}`, `--leading-{tight,normal,relaxed}`
**Spacing:** `--space-{1,2,3,4,6,8,12,16,24}`
**Other:** `--radius-{sm,md,lg,full}`, `--shadow-{sm,md,lg}`, `--transition-{fast,base,slow}`

표현하려는 값이 토큰에 없으면 **컴포넌트에 새 값을 정의하지 말고**, tokens.json/tokens.css에 추가하라고 author에게 지시.

## 추가 일관성 검사

### 6. 태그 슬러그 직접 생성

```bash
grep -rn -E 'tag.*\.toLowerCase\(\)|tag.*replace\(' src/ --include='*.astro' --include='*.ts' \
  | grep -v 'src/utils/tag.ts'
```

→ 직접 슬러그를 만들지 말고 `tagToSlug()` 사용. `src/utils/tag.ts`에서 import.

### 7. Props 타입 누락 (Astro 컴포넌트)

새 `.astro` 파일이 `interface Props` 또는 `type Props`를 가지는지 확인.

### 8. BaseLayout 미사용 (페이지)

`src/pages/` 하위 `.astro` 파일이 `BaseLayout`을 import해서 사용하는지 확인. (단, `[...slug].astro`처럼 `PostLayout`을 쓰는 경우는 예외)

## 출력 형식

reviewer 에이전트가 사용할 때는 `_workspace/03_reviewer_findings.md`에 다음 형식으로 기록:

```markdown
### [CRITICAL] src/components/Foo.astro:42 — 하드코딩 색상

- 위반: 디자인 토큰 절대 원칙 (#1a1a1a)
- 이유: 다크 테마 일관성 + 토큰 변경 시 누락 위험
- 수정: `color: var(--color-text-primary);`로 교체
```

## 자주 발생하는 패턴

| 패턴                                     | 대체                                     |
| ---------------------------------------- | ---------------------------------------- |
| `color: #f0f0f0`                         | `color: var(--color-text-primary)`       |
| `background: #171717`                    | `background: var(--color-bg-elevated)`   |
| `padding: 24px`                          | `padding: var(--space-6)`                |
| `font-size: 1.125rem`                    | `font-size: var(--text-lg)`              |
| `border-radius: 12px`                    | `border-radius: var(--radius-md)`        |
| `box-shadow: 0 4px 10px rgba(0,0,0,0.5)` | `box-shadow: var(--shadow-md)`           |
| `transition: all 250ms ease`             | `transition: all var(--transition-base)` |
