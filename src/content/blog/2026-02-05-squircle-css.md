---
title: '스쿼클(Squircle)을 CSS로 구현하는 현실적인 방법'
date: 2026-02-05
description: 'Apple이 쓰는 연속 곡률 모서리를 웹에서 구현하는 방법들을 비교하고, 2026년 현재 가장 실용적인 선택을 정리합니다.'
tags: ['CSS', 'UI', '디자인', '스쿼클']
draft: false
---

## 스쿼클이란 무엇인가

iOS 앱 아이콘의 모서리를 자세히 보면 일반적인 `border-radius`와 다르다. 직선에서 곡선으로 전환될 때 **갑자기 꺾이지 않고** 부드럽게 이어진다.

이것이 **연속 곡률(G2-continuous curvature)**이고, 이 형태를 스쿼클(squircle)이라고 부른다.

```
일반 border-radius:  직선 → [갑자기] → 원호
스쿼클:             직선 → [점진적으로] → 최대 곡률 → [점진적으로] → 직선
```

수학적으로는 라메 곡선(Lamé curve)의 특수한 형태다.

## CSS border-radius의 한계

`border-radius: 30px`는 정확히 반지름 30px인 원호를 모서리에 붙인다. 곡선이 시작되는 지점과 끝나는 지점에서 불연속이 발생한다. 육안으로 보면 모서리가 "각져" 보이는 느낌이다.

Figma는 "Corner smoothing" 파라미터(0~100%)로 이를 조절한다. Apple의 앱 아이콘은 **60% smoothing**이 표준이다.

## 구현 방법 비교

### 방법 1: SVG clip-path (모든 브라우저)

```css
.squircle {
  clip-path: path(
    'M 0,30 C 0,10 10,0 30,0 L 70,0 C 90,0 100,10 100,30 L 100,70 C 100,90 90,100 70,100 L 30,100 C 10,100 0,90 0,70 Z'
  );
}
```

완벽한 스쿼클이지만 크기가 변하면 path를 다시 계산해야 한다.

### 방법 2: squircle.js 라이브러리

```bash
npm install @squircle-js/react
```

```jsx
import { Squircle } from '@squircle-js/react';

<Squircle cornerRadius={20} cornerSmoothing={0.6}>
  <div>내용</div>
</Squircle>;
```

동적으로 계산해주지만 JS 의존성이 생긴다.

### 방법 3: CSS Houdini (Chrome 실험적)

```css
@property --squircle-radius { ... }

.squircle {
  --squircle-radius: 20px;
  --squircle-smooth: 0.6;
  border-radius: paint(squircle);
}
```

아직 표준이 아니고 Chrome만 지원한다.

### 방법 4: 네이티브 CSS corner-shape (미래)

```css
/* CSS Level 5 명세 — 아직 실험적 */
.squircle {
  border-radius: 20px;
  corner-shape: squircle;
}
```

Chromium에서 플래그 뒤에 숨어있다. 표준화되면 가장 깔끔한 방법이 된다.

## 2026년 현재 실용적인 선택

솔직히 말하면, 대부분의 경우 **`border-radius`를 좀 더 크게 주는 것**으로 충분하다.

| 요소 크기                 | 권장 방법                      |
| ------------------------- | ------------------------------ |
| 아이콘/아바타 (48px 이하) | SVG clip-path 또는 squircle.js |
| 카드/패널 (100px 이상)    | `border-radius: 18px`으로 근사 |
| 버튼/태그                 | `border-radius: 8px` 충분      |

스쿼클의 차이는 작은 크기에서 극적으로 드러나고, 큰 컴포넌트에서는 `border-radius`와 시각적으로 거의 같다.

## 이 블로그의 선택

현재는 `border-radius` 기반으로 토큰을 정의하고, 나중에 `corner-shape`가 안정화되면 한 줄만 바꾸면 된다.

```css
/* 지금 */
--radius-lg: 18px;

/* 미래 (토큰 값 변경 불필요, 컴포넌트에 추가만) */
.card {
  border-radius: var(--radius-lg);
  corner-shape: squircle; /* 추가 */
}
```

토큰 시스템이 있으면 이런 마이그레이션이 쉽다.
