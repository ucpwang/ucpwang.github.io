---
title: 'Pretendard: 한국 웹 타이포그래피의 새 기준'
date: 2026-02-20
description: 'Pretendard가 왜 한국 웹 개발자들의 기본 폰트가 됐는지, 올바른 사용법과 성능 최적화 방법을 정리합니다.'
tags: ['타이포그래피', '폰트', 'CSS', '한국어']
draft: false
---

## Pretendard가 특별한 이유

2021년에 등장한 Pretendard는 3년 만에 한국 정부 UI/UX 공식 서체로 지정됐다. 이 폰트가 기존 한국어 웹 폰트들과 다른 점은 무엇인가?

**기존 선택지의 문제:**

- **나눔고딕**: 웨이트 종류가 적고 영문 자간이 어색하다
- **맑은 고딕**: Windows 전용, 크로스 플랫폼에서 일관성 없음
- **Apple SD Gothic Neo**: macOS/iOS 전용
- **Google Noto Sans KR**: 한글은 좋지만 영문이 다른 폰트와 혼용 시 부조화

Pretendard는 **Inter**(최고의 영문 UI 폰트)와 **Source Han Sans**(어도비의 한글 폰트)를 기반으로 두 언어가 자연스럽게 어우러지도록 설계됐다.

## 설치 방법 3가지

### 1. CDN (가장 빠른 시작)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css"
/>
```

```css
font-family:
  'Pretendard Variable',
  Pretendard,
  -apple-system,
  BlinkMacSystemFont,
  'Apple SD Gothic Neo',
  sans-serif;
```

### 2. npm 설치 (번들러 환경)

```bash
npm install pretendard
```

```css
@import 'pretendard/dist/web/variable/pretendardvariable.css';
```

### 3. 서브셋 (용량 최적화)

전체 Pretendard는 꽤 크다. 실제 사용하는 글자만 포함한 서브셋 버전을 쓰면 용량을 80% 이상 줄일 수 있다.

```html
<!-- 서브셋: 2.3MB → 약 400KB -->
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-subset.min.css"
/>
```

## Variable Font의 장점

Pretendard Variable은 하나의 파일로 모든 웨이트(100~900)를 표현한다.

```css
/* 정적 폰트: 9개 파일 로드 */
/* Variable 폰트: 1개 파일로 모든 웨이트 */

.heading {
  font-weight: 700;
}
.subheading {
  font-weight: 600;
}
.body {
  font-weight: 400;
}
.caption {
  font-weight: 300;
}
```

브라우저가 필요한 웨이트를 하나의 파일에서 插值(interpolate)해서 렌더링한다.

## 웨이트 페어링 가이드

다크 미니멀 블로그 기준 권장 조합:

| 요소           | 웨이트       | 크기     |
| -------------- | ------------ | -------- |
| 대형 헤딩 (h1) | 700 Bold     | 3rem     |
| 섹션 헤딩 (h2) | 600 SemiBold | 1.875rem |
| 소제목 (h3)    | 600 SemiBold | 1.5rem   |
| 본문           | 400 Regular  | 1rem     |
| 메타/날짜      | 300 Light    | 0.875rem |
| 강조 인라인    | 500 Medium   | —        |

## 결론

Pretendard는 한글과 영문이 함께 등장하는 한국 웹 환경에서 현재 최선의 선택이다. Variable 폰트로 성능도 챙기고, 서브셋으로 용량도 줄이면 타이포그래피 때문에 고민할 일이 없어진다.
