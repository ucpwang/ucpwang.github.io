---
name: astro-harness
description: ucpwang.github.io Astro 블로그의 통합 작업 오케스트레이터. 블로그 포스트 작성/수정, Astro 컴포넌트/페이지 변경, 디자인 토큰(tokens.json/tokens.css) 수정, 배포 전 검증(verify.py 전체 통과) 작업을 planner-author-reviewer-verifier 4인 서브 에이전트 파이프라인으로 분기하여 처리한다. 새 글 쓰기, 포스트 추가/수정/보완, 다시 작성, 태그 변경, 이전 결과 개선, 컴포넌트 추가/리팩토링, 디자인 토큰 변경, 색상/간격 조정, 빌드 검증, verify 실행 같은 요청 시 반드시 이 스킬을 트리거. 단순 질문(파일 위치 묻기 등)은 직접 답해도 됨.
---

# astro-harness — 통합 작업 오케스트레이터

이 저장소(`ucpwang.github.io`)의 모든 작업을 4인 서브 에이전트 파이프라인으로 분기·실행한다.

**메인 클로드가 오케스트레이터.** 이 스킬을 트리거한 메인 클로드 자신이 각 단계에서 `Agent` 도구를 호출하여 4명을 순차적으로 가동한다. 클로드코드 표준 도구(`Agent`, `TodoWrite`, 파일 IO)만 사용하며, 별도 팀 통신 도구는 없다.

## 에이전트와 보조 스킬

| 에이전트   | 역할                              | subagent_type     | 사용 스킬                           |
| ---------- | --------------------------------- | ----------------- | ----------------------------------- |
| `planner`  | 작업 분기·명세 작성               | `general-purpose` | (없음)                              |
| `author`   | 실제 파일 작성/수정               | `general-purpose` | `blog-post-author` (블로그 작업 시) |
| `reviewer` | CLAUDE.md 절대 원칙 + 일관성 검토 | `general-purpose` | `design-token-review`               |
| `verifier` | `npm run build` + `verify.py`     | `general-purpose` | `build-verify`                      |

**모든 `Agent` 호출에 다음을 반드시 명시:**

- `subagent_type: "general-purpose"`
- `model: "opus"`
- `description`: `"planner|author|reviewer|verifier: <작업 한 줄 요약>"`

## Phase 0: 컨텍스트 확인 (필수 시작)

워크플로우 시작 전에 `_workspace/` 존재 여부와 사용자 요청 의도를 보고 실행 모드를 결정한다.

| 상태                                    | 모드        | 행동                                                     |
| --------------------------------------- | ----------- | -------------------------------------------------------- |
| `_workspace/` 없음                      | 초기 실행   | `mkdir _workspace` 후 신규 진행                          |
| 있고 + 사용자가 **부분 수정** 요청      | 부분 재실행 | 해당 에이전트만 재호출 (예: "본문 톤만 다시" → author만) |
| 있고 + 사용자가 **새 작업** 요청        | 새 실행     | `mv _workspace _workspace_prev_$(date +%s)` 후 신규      |
| 있고 + 사용자가 **이전 결과 개선** 요청 | 이어쓰기    | 기존 파일 유지, 해당 단계부터 재실행                     |

판단이 모호하면 사용자에게 한 번 확인한다.

`TodoWrite`로 다음 항목을 작성하여 진행 상태를 가시화한다:

1. Phase 1: planner 명세 작성
2. Phase 2: author 구현
3. Phase 3: reviewer 검토 (반복 가능)
4. Phase 4: verifier 빌드+검증 (반복 가능)
5. Phase 5: 최종 보고

## Phase 1: planner 호출

`Agent` 도구로 planner를 호출. prompt 구조 예시:

```
역할: planner 에이전트로서 .claude/agents/planner.md의 지시를 따른다.

사용자 원문:
"<사용자의 원문 요청 그대로>"

실행 모드: <초기/부분 재실행/새 실행/이어쓰기>
_workspace/ 상태: <비어있음 / 다음 파일 존재: ...>

요구사항:
- _workspace/01_planner_spec.md 작성
- 작업 유형 판정: blog-post / ui-component / design-token / verify-only
- 반환 메시지 첫 줄에 한 줄 요약 명시
```

**`verify-only`로 판정되면** Phase 2(author), Phase 3(reviewer)을 건너뛰고 Phase 4(verifier)로 점프한다. planner의 반환 메시지 첫 줄을 보고 분기.

## Phase 2: author 호출

planner 명세를 prompt에 인용하여 author를 `Agent`로 호출:

```
역할: author 에이전트로서 .claude/agents/author.md의 지시를 따른다.
블로그 포스트 작업이면 .claude/skills/blog-post-author/SKILL.md를 먼저 읽는다.

명세 파일: _workspace/01_planner_spec.md
핵심 지시 (인용):
<spec 파일의 author 지시 섹션 내용 인용>

요구사항:
- 명세에 따라 파일 수정/생성
- 디자인 토큰 절대 원칙 준수 (var(--*))
- 디자인 토큰 변경 시 tokens.json과 tokens.css 양쪽 동기화
- _workspace/02_author_changes.md 작성
- 반환 메시지 첫 줄에 변경 파일 수와 핵심 변경 명시
```

`spec ambiguity:` 반환이면 사용자에게 모호함 확인 후 planner 재호출.

## Phase 3: reviewer 호출 (반복 가능, 최대 3회)

```
역할: reviewer 에이전트로서 .claude/agents/reviewer.md의 지시를 따른다.
.claude/skills/design-token-review/SKILL.md의 grep 패턴으로 토큰 위반 검사.

명세 체크포인트: _workspace/01_planner_spec.md
author 변경 목록: _workspace/02_author_changes.md
검토 대상 파일: <변경 파일 경로 목록>

요구사항:
- 디자인 토큰 절대 원칙 + CLAUDE.md 체크리스트 전체 검사
- _workspace/03_reviewer_findings.md 작성
- 반환 첫 줄에 PASS 또는 REVISIONS_NEEDED: <CRITICAL 개수> 명시
```

**판정에 따른 분기:**

- `PASS` → Phase 4로
- `REVISIONS_NEEDED` → findings의 CRITICAL 항목을 author 재호출 prompt에 인용하여 Phase 2 재실행. 그 후 Phase 3 다시 (findings는 `_v2.md`, `_v3.md`로 분리). 최대 3회.
- 3회 후에도 PASS 안 되면 사용자 에스컬레이션 (`_workspace/` 보존).

## Phase 4: verifier 호출 (반복 가능, 최대 2회)

```
역할: verifier 에이전트로서 .claude/agents/verifier.md의 지시를 따른다.
.claude/skills/build-verify/SKILL.md의 실행 절차를 따른다.

이전 단계:
- _workspace/02_author_changes.md (인용)
- _workspace/03_reviewer_findings.md: PASS

요구사항:
- npm run build → preview 백그라운드 → verify.py 실행 → preview 정리
- _workspace/04_verifier_report.md 작성
- 반환 첫 줄에 판정: `N/N PASS` (verify.py 출력 마지막 줄 그대로) / `BUILD_FAILED: <라인>` / `VERIFY_FAILED: <개수>개`
```

**판정에 따른 분기:**

- `N/N PASS` (예: `35/35 PASS`) → Phase 5로
- `BUILD_FAILED` 또는 `VERIFY_FAILED` → 실패 내용을 author 재호출 prompt에 인용하여 Phase 2 재실행 → Phase 3 재검토(생략 가능) → Phase 4 재실행. 최대 2회.
- 최종 실패 시 사용자 에스컬레이션 (`_workspace/` 보존).

## Phase 5: 최종 보고 + 정리

메인 클로드가 사용자에게 직접 보고:

1. 변경 파일 목록 (`_workspace/02_author_changes.md`에서 인용)
2. verifier 결과 (`_workspace/04_verifier_report.md`에서 인용 — "N/N 통과")
3. 다음 권장 액션 (`git status` 확인, 커밋 메시지 초안 등)

**`_workspace/`는 삭제하지 않는다.** 사후 감사·이력 추적용으로 보존.

**피드백 수집:** "개선할 부분이나 다시 작업할 사항이 있으신가요?" 한 번 묻고, 답이 있으면 Phase 1로 회귀 (부분 재실행 모드).

## 데이터 전달

| 채널               | 용도                                               |
| ------------------ | -------------------------------------------------- |
| `_workspace/` 파일 | 모든 중간 산출물 (단일 진실 소스)                  |
| Agent prompt       | 메인 → 서브 에이전트 (필요한 컨텍스트를 모두 인용) |
| Agent 반환         | 서브 → 메인 (판정 + 한 줄 요약)                    |
| `TodoWrite`        | Phase 진행 추적                                    |

파일 네이밍: `_workspace/{phase번호}_{agent}_{artifact}.md` (예: `01_planner_spec.md`). 재호출 시 `_v2.md`, `_v3.md` 등으로 버전 분리.

## 에러 핸들링

| 상황                            | 처리                                                          |
| ------------------------------- | ------------------------------------------------------------- |
| planner가 작업 유형 미판정      | 사용자에게 한 번 확인                                         |
| author가 `spec ambiguity:` 반환 | planner에게 명세 보강 재호출                                  |
| reviewer 3회 연속 REVISIONS     | `_workspace/` 보존하고 사용자 에스컬레이션                    |
| verifier 빌드 2회 연속 실패     | 환경 문제 가능성. 사용자 에스컬레이션.                        |
| 포트 4321 점유 감지             | `lsof -i :4321` 결과 사용자에게 보고 후 승인받고 `kill <pid>` |

**상충 데이터 보존 원칙:** 모든 findings/report는 덮어쓰지 않고 `_v2`, `_v3`로 분리. 사후 추적용.

## 테스트 시나리오

**정상 — 블로그 포스트 신규 작성:**

1. 사용자: "Astro view transitions API 다뤄서 포스트 하나 써줘"
2. 메인: Phase 0 — `_workspace/` 없음, 초기 모드. TodoWrite로 5개 항목 등록.
3. Phase 1: `Agent({subagent_type: "general-purpose", model: "opus", description: "planner: view-transitions blog post"})` → 반환 `spec ready: blog-post`
4. Phase 2: `Agent(... author: write view-transitions post ...)` → `src/content/blog/2026-05-17-astro-view-transitions.md` 생성
5. Phase 3: `Agent(... reviewer: check new blog post ...)` → `PASS`
6. Phase 4: `Agent(... verifier: build + verify ...)` → `N/N PASS` (verify.py 출력 그대로 인용)
7. Phase 5: 메인이 사용자에게 보고

**에러 — 디자인 토큰 위반 발견:**

1. 사용자: "PostCard에 강조 배경 추가"
2. Phase 1~2: author가 `background: #1a1a1a` 하드코딩
3. Phase 3: reviewer가 `REVISIONS_NEEDED: 1 CRITICAL` 반환
4. Phase 2 재호출 (findings의 CRITICAL 항목을 prompt에 인용) → author가 `var(--color-bg-elevated)`로 수정
5. Phase 3 v2: PASS
6. Phase 4: PASS
7. Phase 5: 보고

**verify-only:**

1. 사용자: "지금 상태로 빌드 + verify만 돌려줘"
2. Phase 1: planner가 `verify-only` 판정
3. Phase 2, 3 건너뜀
4. Phase 4: verifier 실행
5. Phase 5: 결과 보고
