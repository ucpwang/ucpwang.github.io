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

### 콘텐츠

- [ ] `archive/` 디렉터리의 구 포스트(2015~2016) 중 가치 있는 글을 선별해 신규 포스트로 마이그레이션 검토
- [ ] About 페이지 타임라인의 `20XX-20XX` 플레이스홀더를 실제 연도로 채우기 (CLAUDE.md 5.2.타임라인 참조)
- [ ] 환경변수 `PUBLIC_CONTACT_EMAIL`, `PUBLIC_LINKEDIN_URL`을 `.env.local`에 설정 (미설정 시 About 페이지 연락 섹션에 플레이스홀더 노출)

### 정합성

- [ ] CLAUDE.md 16장은 "`references/`는 gitignore됨"이라 기술하지만, 일부 공용 참조 파일(`references/README.md`, `colors/`, `design/`, `fonts/`, `ui-patterns/` 하위)은 실제로 트래킹 중. 의도를 정리해 CLAUDE.md 또는 .gitignore 중 하나를 일관되게 맞출 것
- [ ] iCloud Drive 동기화 충돌로 `references/` 하위에 ` 2` 접미사 중복 파일 다수 발생. 일괄 정리 (이번 .gitignore 보강으로 트래킹은 안 되나 디스크상 파일은 잔존)

## 라이선스

콘텐츠와 코드는 별도 라이선스 명시 전까지 저자 보유.
