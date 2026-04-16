# 디자인 방향 개요

## 핵심 키워드

- Ultra-minimalist / 극도의 미니멀
- Dark monochromatic — deep charcoal, matte black, brushed silver accent
- Neumorphic soft ambient shadows (뉴모픽 소프트 섀도우)
- Squircle geometry (연속 곡률 모서리)
- Korean typography — Pretendard / Apple SD Gothic Neo
- Apple + Material Design 문법

---

## 주요 레퍼런스 사이트

### "Calm Interface" 철학

| 사이트 | URL | 핵심 포인트 |
|--------|-----|------------|
| Linear App 디자인 철학 | https://linear.app/now/how-we-redesigned-the-linear-ui | "calm interface" — 딥 블랙 배경, Inter, 8px 스페이싱 스케일, 모든 픽셀이 이유가 있음 |
| Vercel 디자인 가이드라인 | https://vercel.com/design/guidelines | 순수 블랙/화이트, Geist 폰트, 0 장식 색상. "restraint as premium signal" |
| Josh W. Comeau 블로그 | https://www.joshwcomeau.com/ | 다크 미니멀 개발자 블로그 최고 벤치마크. 타이포그래피 리듬 정교함 |

### Apple 공식 가이드

| 사이트 | URL | 핵심 포인트 |
|--------|-----|------------|
| Apple HIG — Dark Mode | https://developer.apple.com/design/human-interface-guidelines/dark-mode | base/elevated 2단계 배경 시스템, 섀도우 대신 밝기로 elevation 표현. 우리 토큰(`--color-bg-base` / `--color-bg-elevated`)의 직접적 원본 |

### 포트폴리오 갤러리

| 사이트 | URL | 핵심 포인트 |
|--------|-----|------------|
| Wall of Portfolios — Dark | https://www.wallofportfolios.in/dark-theme | 다크 포트폴리오 큐레이션. 벤치마크 + 회피 대상 탐색용 |

---

## 이 방향이 우리 사이트에 주는 시사점

1. **배경색**: `#0a0a0a` ~ `#1a1a1a` 범위의 진한 차콜 → Phase 2에서 `--color-bg-base` 값으로 확정
2. **강조색**: 브러시드 실버 계열 (`#a0a0a0` ~ `#d0d0d0`) — 색상 없는 금속 광택
3. **elevation**: 그림자가 아닌 밝기 차이로 레이어 표현 (Apple 방식)
4. **여백**: Linear의 8px 스케이링 → 이미 토큰에 반영됨
