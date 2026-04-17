---
title: 'CSS Custom Properties로 테마 시스템 만들기'
date: 2025-10-14
description: 'CSS 변수(Custom Properties)의 진짜 힘을 활용해 다크/라이트 테마, 디자인 토큰, 컴포넌트 API를 설계하는 패턴을 정리합니다.'
tags: ['CSS', '디자인시스템', '테마', '웹개발']
draft: false
---

## CSS 변수가 SCSS 변수와 다른 이유

많은 개발자가 CSS Custom Properties(CSS 변수)를 단순히 "CSS에서 쓸 수 있는 SCSS 변수" 정도로 이해한다. 하지만 핵심적인 차이가 있다.

**SCSS 변수**: 빌드 시 값으로 대체됨. 런타임에 변경 불가.

```scss
$color-brand: #6366f1;
// 빌드 후: color: #6366f1; (변수 사라짐)
```

**CSS Custom Properties**: 런타임에 DOM에 살아있음. JavaScript로 변경 가능.

```css
:root {
  --color-brand: #6366f1;
}
/* 런타임에도 var(--color-brand)로 남아있음 */
```

이 차이가 테마 시스템을 가능하게 만든다.

## 다크/라이트 테마 구현

```css
:root {
  --color-bg: #ffffff;
  --color-text: #171717;
  --color-brand: #6366f1;
}

[data-theme='dark'] {
  --color-bg: #0f0f0f;
  --color-text: #f0f0f0;
  --color-brand: #818cf8; /* 다크에서 더 밝은 버전 */
}
```

HTML에 `data-theme` 속성만 바꾸면 모든 컴포넌트가 동시에 업데이트된다.

```js
document.documentElement.setAttribute('data-theme', 'dark');
```

## 계층적 토큰 시스템

좋은 디자인 토큰 시스템은 두 계층으로 나뉜다.

**Primitive tokens (원시값):**

```css
:root {
  --blue-500: #6366f1;
  --gray-900: #111827;
}
```

**Semantic tokens (의미값):**

```css
:root {
  --color-brand: var(--blue-500); /* 원시값 참조 */
  --color-bg-base: var(--gray-900);
}
```

Semantic 토큰을 컴포넌트에서 사용하면, Primitive 값을 바꾸거나 테마를 바꿀 때 컴포넌트 코드를 건드리지 않아도 된다.

## 컴포넌트 API로서의 CSS 변수

CSS 변수는 컴포넌트에 "외부에서 주입 가능한 값"을 정의하는 데 쓸 수 있다.

```css
.button {
  /* 기본값 정의 */
  --btn-bg: var(--color-brand);
  --btn-color: #ffffff;
  --btn-radius: var(--radius-md);

  background: var(--btn-bg);
  color: var(--btn-color);
  border-radius: var(--btn-radius);
}

/* 사용하는 쪽에서 오버라이드 */
.button--danger {
  --btn-bg: #ef4444;
}

.sidebar .button {
  --btn-radius: var(--radius-sm); /* 사이드바에서는 작은 radius */
}
```

JavaScript 없이 CSS만으로 컴포넌트 변형을 만들 수 있다.

## @property로 타입 안전성 추가

```css
@property --card-opacity {
  syntax: '<number>'; /* number 타입만 허용 */
  inherits: false;
  initial-value: 1;
}
```

`@property`를 쓰면:

1. 타입 검증 (잘못된 값 무시)
2. 애니메이션 가능 (숫자형 변수는 transition 작동)
3. 상속 제어 (`inherits: false`로 부모에서 상속 안 됨)

## 실용적인 팁

```css
/* 계산에도 활용 */
.hero {
  --hero-height: 600px;
  height: var(--hero-height);
  margin-top: calc(var(--hero-height) / -2);
}

/* 미디어 쿼리와 조합 */
:root {
  --container-width: 720px;
}
@media (max-width: 768px) {
  :root {
    --container-width: 100%;
  }
}
```

## 결론

CSS Custom Properties는 단순한 변수 기능을 넘어, 런타임 테마 시스템과 컴포넌트 API를 CSS만으로 구현할 수 있게 한다. 디자인 시스템을 만들 때 이 기능을 제대로 활용하면 JavaScript 의존성을 크게 줄일 수 있다.
