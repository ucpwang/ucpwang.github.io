---
title: 'Astro로 나만의 디자인 시스템 만들기'
date: 2026-04-15
description: 'CSS Custom Properties를 단일 소스로 삼아 토큰 기반 디자인 시스템을 설계하고, Claude Code 하네스와 연동하는 과정을 기록합니다.'
tags: ['Astro', '디자인시스템', 'CSS', 'ClaudeCode']
draft: false
---

## 왜 디자인 시스템인가

블로그를 새로 만들면서 가장 먼저 결정한 것이 디자인 시스템이었다. 단순히 예쁜 사이트를 만들고 싶은 게 아니라, **AI와 함께 작업할 때 일관성을 유지하는 도구**가 필요했다.

Claude Code에게 "버튼 색상을 바꿔줘"라고 했을 때 하드코딩된 `#0085a1`이 코드베이스 곳곳에 박혀있다면? 수십 개 파일을 수동으로 수정해야 한다. 하지만 `var(--color-brand)`를 쓰면 `tokens.css` 한 줄만 바꾸면 된다.

## 토큰 구조 설계

토큰은 세 계층으로 나눴다.

```
design-tokens/tokens.json    ← 단일 소스 (숫자/값)
src/styles/tokens.css        ← CSS 변수로 변환
컴포넌트 <style>             ← 변수만 참조, 값 없음
```

`tokens.json`에서 값을 관리하고, `tokens.css`에 CSS Custom Properties로 옮기는 과정은 수동이지만 명확하다. 나중에 빌드 스크립트로 자동화할 수 있다.

```json
{
  "color": {
    "brand": {
      "base": "#c0c0c0",
      "light": "#e0e0e0",
      "dark": "#808080"
    }
  }
}
```

```css
:root {
  --color-brand: #c0c0c0;
  --color-brand-light: #e0e0e0;
  --color-brand-dark: #808080;
}
```

## Astro 컴포넌트 패턴

Astro의 스코프드 CSS는 디자인 시스템과 잘 어울린다. 컴포넌트 내부에서는 변수만 쓰고, 값은 절대 하드코딩하지 않는다.

```astro
<style>
  /* WRONG */
  .card {
    background: #171717;
  }

  /* RIGHT */
  .card {
    background: var(--color-bg-elevated);
  }
</style>
```

이 원칙 하나로 테마 전환, 다크/라이트 모드, AI 협업 시 일관성이 모두 해결된다.

## Claude Code 하네스와의 연동

`CLAUDE.md`에 토큰 사용 원칙을 명시해두면 AI가 컴포넌트를 생성할 때 자동으로 변수를 사용한다. `.claude/settings.json`의 PostToolUse 훅은 파일 저장 시 자동으로 prettier를 실행해준다.

> 코드 품질 게이트를 사람이 신경 쓰지 않아도 되는 구조가 핵심이다.

## 결론

디자인 시스템은 사치가 아니다. 특히 AI와 함께 작업할 때는 **AI가 따를 수 있는 규칙**을 명확히 정의하는 것이 생산성의 핵심이다. 토큰 하나 잘 만들어두면 수십 번의 대화에서 "색상 하드코딩하지 마세요"를 반복하지 않아도 된다.
