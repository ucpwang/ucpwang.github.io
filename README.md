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

### 블로그 콘텐츠 방향성

About 페이지 태그라인 **"서비스를 만들어 본 사람의 보안은 다릅니다"** 를 글의 차별화 축으로 삼는다. 새 포스트는 아래 3축 중 어디에 들어가는지 자문하고 쓴다. 셋 다 해당하지 않으면 일단 보류.

#### 축 1 — 개발×보안 교차점 (최우선, 차별화 축)

코드·아키텍처에서 시작해 보안 설계로 이어지는 글. 보안 담당자에게는 코드 관점을, 개발자에게는 보안 관점을 보여준다.

- [ ] MSA에서의 서비스 간 신뢰 — mTLS·서비스 메시·OAuth2 클라이언트 자격증명 비교
- [ ] Spring Boot에서 시큐리티 컨피그를 자유롭게 쓰는 패턴 — SecurityFilterChain 다중 정의와 함정
- [ ] DevSecOps 파이프라인 단계별 도구 매핑 — SAST(SonarQube)·SCA·컨테이너 스캔·IaC 스캔의 실효성 평가
- [ ] 개발자가 자주 만드는 인가(authorization) 버그 패턴 — IDOR·broken function-level authz 중심
- [ ] 로그에 개인정보 흘리는 흔한 실수와 마스킹 전략 — Logback/Slf4j MDC + 마스킹 컨버터

#### 축 2 — 클라우드 보안 아키텍처

DKtechin Kakao Cloud 이관·보안 인프라 구축 실무에서 나온 글. 추상론이 아니라 실제 도입·운영한 도구·아키텍처 기록.

- [ ] Kakao Cloud 이관 시 보안 아키텍처 재설계 회고 — 무엇을 가장 먼저 손봤나
- [ ] KMS·VPN·VDI 세트 배치 — 누가 어디로 접근하는지 그림으로 정리
- [ ] DB 접근제어를 Querypie로 — 도입 결정 기준, 운영자가 안 도망간 이유
- [ ] DLP는 왜 어렵나 — 차단 정책의 함정과 운영 부담 줄이는 단계적 도입
- [ ] 클라우드 시크릿 관리 — 환경변수·시크릿 매니저·IRSA의 트레이드오프

#### 축 3 — 리더십·커리어 회고

기술자에서 CISO까지의 전환 회고. 1인칭 평어체, 일반화 가능한 통찰 위주. 무용담은 지양.

- [ ] 개발 선임 → 기술전략 리더 → 정보보호 리더 → CISO — 각 전환점에서 깨진 가정들
- [ ] CISO 역할을 새로 정의해야 할 때 — 빈 자리에 들어가서 첫 90일에 한 일
- [ ] 보안팀과 개발팀이 충돌할 때 — 양쪽 다 해본 사람이 중재하는 법
- [ ] 사내 정보보호 뉴스레터를 1년 발간하며 배운 것 — 콘텐츠 설계와 구독률 끌어올리기
- [ ] 주니어 멘토링에서 Docker·K8s 심화 교육 설계 — 학습 경로 vs 실전 경로

#### 의도적으로 다루지 않는 축

- 정보보호 거버넌스·인증 실무 (ISMS-P, ISO 27001/27701 등) — 본업이지만 블로그 콘텐츠로는 보류
- 일반론 위주의 프론트엔드·CSS·디자인 시스템 글 — 이전 버전에서 정체성과 어긋났음

### 인프라 / 의존성

- [ ] **Astro v6 마이그레이션** — `astro.config.mjs`의 `legacy.collectionsBackwardsCompat` 플래그 제거. `src/content/config.ts`를 `src/content.config.ts`로 이동하고 모든 콜렉션을 Content Layer API(`loader: glob(...)`)로 전환. v6에서 legacy 지원이 제거되므로 사전 작업 필요
- [ ] **GitHub Actions Node 24 대비** — `.github/workflows/deploy.yml`의 `actions/checkout@v4`, `actions/setup-node@v4`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`, `actions/upload-artifact@v4`가 Node 20 사용. 2026-06-02부터 Node 24 기본, 2026-09-16에 Node 20 제거. 각 액션의 최신 버전 점검·업데이트 필요

## 라이선스

콘텐츠와 코드는 별도 라이선스 명시 전까지 저자 보유.
