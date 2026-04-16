# 다크 모노크로매틱 컬러 레퍼런스

## 방향

딥 차콜 + 매트 블랙 + 브러시드 실버 어센트.
색상(hue) 없이 밝기(lightness)와 질감(texture)만으로 계층 표현.

---

## 레퍼런스 팔레트

### Linear 스타일 (딥 다크)
```
배경 (base)      #0a0a0a  — 거의 순수 블랙
배경 (elevated)  #111111  — 카드/패널
배경 (code)      #1a1a1a  — 코드 블록
테두리           #222222  — 기본 구분선
테두리 (strong)  #333333  — 강조 구분선
```

### Vercel 스타일 (순수 블랙 + 화이트)
```
배경             #000000  — 순수 블랙
텍스트 primary   #ffffff  — 순수 화이트
텍스트 secondary #888888  — 미드 그레이
테두리           #333333
```

### 브러시드 실버 어센트 (금속 느낌)
```
brand (silver)   #a8a8a8  — 브러시드 알루미늄
brand light      #d4d4d4  — 하이라이트
brand dark       #6b6b6b  — 다크 메탈
```

---

## 레퍼런스 사이트

| 이름 | URL | 메모 |
|------|-----|------|
| Vercel 디자인 가이드 | https://vercel.com/design/guidelines | 순수 블랙/화이트. "restraint as premium" |
| Linear 리디자인 포스트 | https://linear.app/now/how-we-redesigned-the-linear-ui | 딥 차콜 + 8px 스케일 |
| Apple HIG Dark Mode | https://developer.apple.com/design/human-interface-guidelines/dark-mode | base/elevated 2단계 시스템의 원본 |
| Wall of Portfolios Dark | https://www.wallofportfolios.in/dark-theme | 다크 포트폴리오 서베이 |

---

## 뉴모피즘 섀도우 값 (딥 차콜 기준)

배경 `#1a1a1a` 기준 (neumorphism.io 생성):

```css
/* Flat (기본 카드) */
box-shadow:
  -4px -4px 8px rgba(255, 255, 255, 0.03),
   4px  4px 8px rgba(0, 0, 0, 0.5);

/* Concave (누른 상태 / 코드 블록) */
box-shadow:
  inset -4px -4px 8px rgba(255, 255, 255, 0.03),
  inset  4px  4px 8px rgba(0, 0, 0, 0.5);

/* Convex (태그 pill / 버튼) */
box-shadow:
  -2px -2px 5px rgba(255, 255, 255, 0.05),
   2px  2px 5px rgba(0, 0, 0, 0.4);
```

---

## Phase 2 토큰 적용 후보

```json
"color": {
  "brand": {
    "base":  "#a8a8a8",
    "light": "#d4d4d4",
    "dark":  "#6b6b6b"
  },
  "text": {
    "primary":   "#f0f0f0",
    "secondary": "#a0a0a0",
    "muted":     "#606060"
  },
  "bg": {
    "base":     "#0a0a0a",
    "elevated": "#141414",
    "code":     "#1a1a1a"
  },
  "border": {
    "default": "#222222",
    "strong":  "#333333"
  }
}
```

Phase 2에서 `tokens.json`에 적용 예정.
