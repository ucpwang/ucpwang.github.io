---
title: 'GitHub Actions로 Astro 사이트 자동 배포하기'
date: 2025-11-22
description: 'Astro 사이트를 GitHub Pages에 자동으로 배포하는 워크플로우 설정 방법. 브랜치 전략부터 배포 확인까지 단계별로 설명합니다.'
tags: ['GitHub Actions', 'CI/CD', 'Astro', '배포']
draft: false
---

## 왜 GitHub Actions인가

Astro는 빌드가 필요한 프레임워크다. `npm run build`로 `dist/` 폴더를 만들고, 이걸 서빙해야 한다. 직접 `dist/`를 커밋하는 방법도 있지만, 이건 소스와 빌드 결과가 섞이는 문제가 있다.

GitHub Actions를 쓰면:

- `src/`만 커밋 (소스만 관리)
- push 시 Actions가 자동으로 빌드
- 빌드 결과를 Pages에 배포

## 기본 워크플로우

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [master]
  workflow_dispatch: # 수동 실행 가능

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm # 의존성 캐싱

      - uses: actions/configure-pages@v5
        id: pages

      - run: npm ci # package-lock.json 기준 설치
      - run: npm run build

      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

## GitHub Pages 설정

저장소 → Settings → Pages → Source를 **"GitHub Actions"**로 변경해야 한다.

기본값인 "Deploy from a branch"를 그대로 두면 Actions가 배포해도 반영되지 않는다.

## cache: npm의 효과

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: npm # 이게 핵심
```

이 한 줄이 `node_modules` 캐싱을 자동으로 처리한다. `package-lock.json`이 변경되지 않으면 `npm ci` 대신 캐시를 쓴다.

빌드 시간: 캐시 없이 약 45초 → 캐시 있으면 약 15초

## workflow_dispatch: 수동 실행

```yaml
on:
  push:
    branches: [master]
  workflow_dispatch: # GitHub UI에서 수동 실행 버튼
```

코드 변경 없이 배포를 다시 트리거하고 싶을 때 유용하다. Actions 탭 → 워크플로우 → "Run workflow" 버튼.

## 배포 확인

배포 후 확인 순서:

1. Actions 탭 → 초록 체크 확인
2. Settings → Pages → 배포 URL 확인
3. `https://ucpwang.github.io` 접속

첫 배포는 DNS 전파 때문에 3~5분 걸릴 수 있다.

## concurrency 설정의 중요성

```yaml
concurrency:
  group: pages
  cancel-in-progress: false
```

`cancel-in-progress: false`는 진행 중인 배포를 취소하지 않는다는 의미다. 배포 중에 또 push가 들어와도 현재 배포를 완료한 뒤 다음 배포가 시작된다.

`true`로 설정하면 이전 배포가 취소되고 새 배포가 시작된다. 빠르지만 배포 중 사이트가 불완전한 상태일 수 있다.

## 마무리

이 워크플로우 하나로 "코드 push → 자동 빌드 → 자동 배포"가 완성된다. 이후로는 `git push`만 하면 된다.
