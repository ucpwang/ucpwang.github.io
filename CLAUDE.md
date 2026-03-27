# CLAUDE.md

이 파일은 이 저장소에서 작업하는 AI 어시스턴트를 위한 가이드입니다.

## 프로젝트 개요

[ucpwang.github.io](http://ucpwang.github.io)에 GitHub Pages로 호스팅되는 개인 블로그 및 포트폴리오 사이트입니다. 사이트는 두 가지 영역으로 구성됩니다:

1. **루트 블로그** — Strapdown.js를 통한 클라이언트 사이드 Markdown 렌더링을 사용하는 정적 HTML 파일
2. **포트폴리오 사이트** (`jacobs_mac_house/`) — Bootstrap Clean Blog 테마를 사용한 멀티 페이지 포트폴리오

## 저장소 구조

```
ucpwang.github.io/
├── index.html                    # 메인 랜딩 페이지 / 블로그 인덱스
├── README.md                     # 프로젝트 설명 (간략)
├── bower.json                    # 프론트엔드 의존성 목록
├── CLAUDE.md                     # 이 파일
├── images/                       # 블로그 포스트 이미지 (PNG)
├── js/
│   ├── clean-blog.js             # 블로그 테마 JS (~1057줄)
│   └── clean-blog.min.js         # 압축 버전
├── jacobs_mac_house/             # 포트폴리오 서브디렉토리 (~36 MB)
│   ├── index.html                # 포트폴리오 랜딩 페이지
│   ├── about.html                # 소개 페이지
│   ├── contact.html              # 연락처 페이지
│   ├── post.html                 # 블로그 포스트 템플릿
│   ├── css/                      # 컴파일된 CSS (Bootstrap + Clean Blog 테마)
│   ├── less/                     # LESS 소스 파일
│   │   ├── clean-blog.less       # 메인 테마 LESS
│   │   ├── variables.less        # 테마 변수
│   │   └── mixins.less           # LESS 믹스인
│   └── ...                       # AdminLTE, GreenSock 등 벤더 라이브러리
└── 20YYMMDD_topic_name.*         # 블로그 포스트 (.md + .html 쌍)
```

## 블로그 포스트 규칙

블로그 포스트는 다음 네이밍 규칙을 따릅니다:

```
YYYYMMDD_주제_부제.md    # Markdown 소스
YYYYMMDD_주제_부제.html  # 렌더링된 HTML 래퍼
```

### 블로그 포스트 동작 방식

각 `.html` 파일은 Strapdown.js가 클라이언트 사이드에서 렌더링할 수 있도록 Markdown을 `<textarea>` 요소로 감쌉니다:

```html
<!DOCTYPE html>
<html>
<head>...</head>
<body>
<textarea theme="united">
# 블로그 포스트 제목

Markdown 내용...
</textarea>
<script src="http://strapdownjs.com/v/0.2/strapdown.js"></script>
</body>
</html>
```

`.md` 파일에는 Markdown 원본 내용이 담깁니다.

**새 블로그 포스트 추가 방법:**
1. `YYYYMMDD_주제_부제.md` 파일을 Markdown 내용으로 생성
2. 위 Strapdown.js 템플릿을 사용하여 `YYYYMMDD_주제_부제.html` 파일 생성
3. `index.html`의 블로그 목록 섹션에 링크 항목 추가

## 기술 스택

| 계층 | 기술 |
|------|------|
| 호스팅 | GitHub Pages (정적) |
| CSS 프레임워크 | Bootstrap 3.3.5 (CDN) |
| 블로그 테마 | StartBootstrap Clean Blog |
| CSS 전처리기 | LESS (`jacobs_mac_house/less/` 내 소스) |
| Markdown 렌더링 | Strapdown.js (CDN, 클라이언트 사이드) |
| 패키지 매니저 | Bower (프론트엔드 의존성) |
| 아이콘 | Font Awesome 4.1.0 |
| 폰트 | Google Fonts (Lora, Open Sans) |

## 스타일 규칙

- 기본 색상: `#0085a1` (청록색) — 링크 및 강조
- 본문 텍스트: `#404040` (진한 회색)
- 본문 폰트: Lora (세리프)
- 제목 폰트: Open Sans (산세리프)
- `jacobs_mac_house/css/`의 **컴파일된 CSS를 직접 수정하지 말 것** — 대신 `jacobs_mac_house/less/` 내 LESS 소스를 수정할 것

### 테마 스위처

`index.html`에는 페이지 로드 시 7개의 Bootstrap CDN 테마 중 하나를 무작위로 선택하는 JavaScript 코드가 포함되어 있습니다:

- Cerulean, Cyborg, Journal, Simplex, Slate, Spacelab, United

## 개발 워크플로우

### 루트 레벨 빌드 불필요

루트 레벨 블로그는 별도의 빌드 과정이 없습니다. HTML, CSS, JS 파일이 GitHub Pages에서 직접 서빙됩니다.

### LESS 컴파일 (포트폴리오 섹션만 해당)

`jacobs_mac_house/` 디렉토리에는 Grunt 기반 빌드가 있습니다 (AdminLTE 2.3.0):

```bash
cd jacobs_mac_house
npm install     # grunt 및 플러그인 설치
grunt           # LESS 컴파일, CSS/JS 압축, 이미지 최적화
grunt watch     # 파일 변경 감지
```

### 배포

`master` 브랜치에 push하면 GitHub Pages가 자동으로 배포합니다. CI/CD 파이프라인은 없습니다.

```bash
git push origin master
```

## 브랜치 전략

- `master` — 프로덕션 브랜치, GitHub Pages에 자동 배포
- 기능 브랜치는 `<출처>/설명-접미사` 패턴을 따릅니다 (예: `claude/add-feature-XYZ`, `copilot/설명`)

## 콘텐츠 가이드라인

- 블로그 포스트는 한국어 또는 영어로 작성합니다 (기존 포스트는 한국어)
- 이미지는 `/images/` 디렉토리에 저장합니다
- 이미지 크기는 웹에 적합하게 유지합니다 (기존 이미지: 97 KB~363 KB)
- 꼭 필요한 경우가 아니라면 대용량 바이너리 파일이나 벤더 라이브러리를 커밋하지 않습니다

## 주요 파일 참조

| 파일 | 용도 |
|------|------|
| `index.html` | 블로그 인덱스 — 새 포스트 추가 시 반드시 업데이트 |
| `bower.json` | 프론트엔드 의존성 목록 (Bootstrap, jQuery 등) |
| `js/clean-blog.js` | 블로그 주요 인터랙션 (네비게이션 바, 스크롤 등) |
| `jacobs_mac_house/less/variables.less` | 테마 색상/폰트 변수 — 시각적 스타일 변경 시 수정 |

## 주의 사항

- `jacobs_mac_house/` 내 벤더 디렉토리(`AdminLTE/`, `startbootstrap-clean-blog-gh-pages/` 등)의 파일을 수정하지 말 것
- 기능 개발 시 `master`에 직접 push하지 말고 기능 브랜치를 사용할 것
- `node_modules/`나 `bower_components/`는 저장소에 추가하지 말 것 (gitignore에 등록됨)
- `jacobs_mac_house/` 디렉토리는 ~36 MB이므로 대용량 에셋 추가를 지양할 것
