# 뉴모피즘 (Neumorphism) 레퍼런스

## 개념

배경색과 동일한 계열의 밝은/어두운 이중 그림자로 소프트한 3D 부조 효과를 만드는 기법.
다크 뉴모피즘은 딥 차콜 배경에서 작동하며, 하이라이트 섀도우와 다크 섀도우를 함께 사용.

```css
/* 다크 뉴모피즘 기본 패턴 */
box-shadow:
  -4px -4px 8px rgba(255, 255, 255, 0.04),   /* 하이라이트 */
   4px  4px 8px rgba(0, 0, 0, 0.4);           /* 딥 섀도우 */
```

---

## 레퍼런스

| 이름 | URL | 메모 |
|------|-----|------|
| Dribbble — Dark Neumorphism 모음 | https://dribbble.com/tags/dark-neumorphism | 다크 뉴모피즘 샷 전체 태그. 스마트홈/뮤직 플레이어 UI 다수 |
| Behance — Neomorphic Darkness UI Kit | https://www.behance.net/gallery/90329723/Neomorphic-Darkness-Free-UI-Kit | Adobe XD 무료 킷. 피치 블랙 배경에 완전히 커밋한 드문 사례 |
| Dribbble — Dark Mode by Karen Chiu | https://dribbble.com/shots/10060733-Neumorphism-UI-Design-Dark-Mode | 딥 차콜에서의 섀도우 비율 조정 레퍼런스 |
| 25 Neumorphism Inspirations | https://superdevresources.com/neumorphism-ui-design-inspiration/ | Spotify, Tesla 다크 UI 뉴모피즘 변형 포함 |
| Dashboard Freebie (Dark) | https://dribbble.com/shots/12050811--Freebie-Project-manager-dashboard-Neumorphism-Dark-UI | 카드 그리드 레이아웃에 뉴모피즘 적용된 실제 예시 |

---

## 실전 도구

**neumorphism.io** — https://neumorphism.io/

배경색을 입력하면 `box-shadow` 값을 자동 계산해주는 CSS 생성기.
다크 모드: `#1a1a1a` 등 딥 차콜 값 입력 → flat/concave/convex 선택 → 토큰에 바로 적용.

---

## 블로그 적용 포인트

- PostCard: flat 뉴모피즘 (hover 시 pressed로 전환)
- Code block: concave (패인 느낌)
- Header/Nav: 최소한의 ambient shadow만 (너무 강하면 dated 느낌)
- Tag pill: convex (튀어나온 느낌)
