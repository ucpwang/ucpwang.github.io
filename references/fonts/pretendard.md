# Pretendard 폰트 레퍼런스

## 개요

Inter + Source Han Sans 기반의 Neo-grotesque 서체.
9가지 정적 웨이트 + Variable 폰트 축 제공.
SIL Open Font License — 상업적 사용 무료.
2024년 4월 한국 정부 UI/UX 시스템 기본 서체로 지정됨.

---

## 레퍼런스

| 이름 | URL | 메모 |
|------|-----|------|
| 공식 GitHub | https://github.com/orioncactus/pretendard | CDN 링크, 서브셋(`pretendard-subset`), Variable 폰트 사용법 |
| Adobe Fonts | https://fonts.adobe.com/fonts/pretendard | 웨이트별 스펙시멘. 한/영 혼용 시 가독성 확인용 |
| Fonts In Use | https://fontsinuse.com/typefaces/202260/pretendard | 실제 제품/출판물에서의 사용 사례 |

---

## CDN 사용법

```html
<!-- Pretendard Variable (권장) -->
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css" />

<!-- 서브셋 (용량 최적화) -->
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-subset.min.css" />
```

```css
font-family: 'Pretendard Variable', Pretendard, -apple-system,
  BlinkMacSystemFont, 'Apple SD Gothic Neo', sans-serif;
```

---

## 웨이트 페어링 (다크 미니멀 방향)

| 용도 | 웨이트 | CSS |
|------|--------|-----|
| 대형 헤딩 (h1) | Bold 700 | `font-weight: 700` |
| 서브 헤딩 (h2~h3) | SemiBold 600 | `font-weight: 600` |
| 본문 | Regular 400 | `font-weight: 400` |
| 캡션 / 메타 | Light 300 | `font-weight: 300` |
| 강조 인라인 | Medium 500 | `font-weight: 500` |

---

## 토큰 적용 방향

```json
// design-tokens/tokens.json 업데이트 예시
"typography": {
  "font": {
    "heading": "'Pretendard Variable', Pretendard, -apple-system, sans-serif",
    "body": "'Pretendard Variable', Pretendard, -apple-system, sans-serif",
    "mono": "'JetBrains Mono', 'Fira Code', monospace"
  }
}
```

Phase 2에서 `tokens.json`의 TBD 값을 위 내용으로 채울 예정.
