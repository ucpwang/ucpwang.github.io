# [ucpwang.github.io](https://ucpwang.github.io)

Jacob.c의 개인 블로그 및 프로필 사이트. GitHub Pages에 정적 호스팅된다.

## 스택

- **Astro v5.18** — 정적 사이트 생성
- **Pretendard Variable** — 한글 본문 + 제목 통일
- **Pagefind** — 정적 사이트 전문 검색
- **GitHub Actions** → **GitHub Pages** — `master` push 시 자동 빌드·배포

상세 구조·디자인 토큰·페이지별 아키텍처는 [CLAUDE.md](./CLAUDE.md)에 정리되어 있다.

## 개발

```bash
npm install      # 의존성 설치
npm run dev      # 개발 서버 (http://localhost:4321)
npm run build    # 프로덕션 빌드 → dist/
npm run preview  # 빌드 결과물 미리보기
npm run format   # prettier 일괄 포맷
```

## TODO

이 프로젝트의 모든 미해결 작업은 여기서만 관리한다 (단일 소스).

### 인프라 / 의존성

- [ ] **Astro v6 마이그레이션** — `astro.config.mjs`의 `legacy.collectionsBackwardsCompat` 플래그 제거. `src/content/config.ts`를 `src/content.config.ts`로 이동하고 모든 콜렉션을 Content Layer API(`loader: glob(...)`)로 전환. v6에서 legacy 지원이 제거되므로 사전 작업 필요
- [ ] **GitHub Actions Node 24 대비** — `.github/workflows/deploy.yml`의 `actions/checkout@v4`, `actions/setup-node@v4`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`, `actions/upload-artifact@v4`가 Node 20 사용. 2026-06-02부터 Node 24 기본, 2026-09-16에 Node 20 제거. 각 액션의 최신 버전 점검·업데이트 필요

### 개발 워크플로우

- [ ] **원격 환경 Slack 전송 구조 개선** — 원격 접속 상태(Claude Code on the web 등)에서도 Slack 메시지·이미지 캡처본 전송이 가능하도록 파이프라인 구축. 목적: 스크린샷 등 결과물을 메신저로 즉시 공유해 원격 피드백 루프 확보. Slack MCP 서버 설정, Bot Token/Team ID 환경변수 주입 경로, 이미지 업로드(`files.upload`) 권한 스코프 설계 포함

## 라이선스

콘텐츠와 코드는 별도 라이선스 명시 전까지 저자 보유.
