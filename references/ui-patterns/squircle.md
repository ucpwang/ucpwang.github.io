# 스쿼클 (Squircle) 레퍼런스

## 개념

단순한 원호(circular arc)가 아닌 연속 곡률(continuous curvature, G2-continuous)로 모서리를 처리하는 기법.
Apple이 iOS 아이콘부터 전체 UI에 적용하는 "프리미엄 실루엣"의 핵심.

일반 `border-radius`: 직선 → 갑자기 원호 (불연속)
스쿼클: 직선 → 점진적으로 곡선 → 완전한 곡선 (연속)

---

## 레퍼런스

| 이름 | URL | 메모 |
|------|-----|------|
| Figma Blog — "Desperately Seeking Squircles" | https://www.figma.com/blog/desperately-seeking-squircles/ | 스쿼클 수학, G2 연속성, Figma 60% smoothing 파라미터 설명. 필독 |
| Squircle.js — Apple 사용 사례 | https://squircle.js.org/blog/squircles-in-apple-design | Apple이 적용하는 모든 위치 + 60% smoothing 파라미터 |
| Squircle.js — 웹 구현 방법 | https://squircle.js.org/blog/squircles-in-web-design | SVG clip-path, CSS Houdini, 네이티브 CSS `corner-shape` 구현법 |
| MDN — CSS corner-shape | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/corner-shape | 표준 명세. `corner-shape: squircle` (Chromium 플래그 뒤에 있음) |
| Figma Community — Super Squircle 파일 | https://www.figma.com/community/file/979319952548488986/super-squircle-icon-shape | Figma에서 바로 쓸 수 있는 파라메트릭 스쿼클 쉐이프 |

---

## 웹 구현 현실

현재 네이티브 CSS `corner-shape`는 Chromium 실험적 플래그 단계.
실용적인 방법:

```css
/* 방법 1: SVG clip-path (모든 브라우저) */
clip-path: path("M ...");

/* 방법 2: squircle.js 라이브러리 */
/* https://squircle.js.org */

/* 방법 3: 근사값 — border-radius + 적절한 값으로 흉내 */
border-radius: 30% 30% 30% 30% / 30% 30% 30% 30%;
```

---

## 블로그 적용 포인트

- PostCard 모서리: `border-radius` 대신 squircle clip-path
- Tag pill: 작은 사이즈라 `border-radius: 6px`로 근사 가능
- Avatar/프로필 이미지: 아이콘 크기라면 squircle이 효과 극대화
