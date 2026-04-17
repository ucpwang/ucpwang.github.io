---
title: 'Claude Code Hooks로 자동화 파이프라인 만들기'
date: 2026-03-10
description: 'PostToolUse, PreToolUse, SessionStart 훅을 활용해 AI 작업 환경을 자동화하는 실전 패턴을 공유합니다.'
tags: ['ClaudeCode', '자동화', '개발환경']
draft: false
---

## Hooks란 무엇인가

Claude Code의 Hooks는 특정 이벤트가 발생했을 때 쉘 커맨드를 자동으로 실행하는 기능이다. 쉽게 말하면 **git hooks를 AI 작업 흐름에 적용한 것**이다.

사용 가능한 이벤트:

- `PreToolUse` — 도구 실행 전
- `PostToolUse` — 도구 실행 후
- `SessionStart` — 세션 시작 시
- `Stop` — AI가 응답을 완료했을 때
- `PreCompact` / `PostCompact` — 컨텍스트 압축 전후

## 가장 유용한 패턴: 자동 포매터

파일을 저장할 때마다 자동으로 prettier를 실행하는 훅이다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path // empty' | { read -r f; [ -n \"$f\" ] && npx prettier --write \"$f\" --log-level silent; } 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

이 훅 덕분에 AI가 생성한 코드는 항상 포맷된 상태로 저장된다. "prettier 돌려줘"를 매번 말할 필요가 없다.

## stdin에서 파일 경로 추출하기

훅 커맨드는 stdin으로 JSON 페이로드를 받는다.

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts"
  }
}
```

`jq -r '.tool_input.file_path // empty'`로 파일 경로를 추출하고, 파이프로 read한 뒤 커맨드에 넘긴다. `// empty`는 키가 없을 때 null 대신 빈 문자열을 반환해서 에러를 방지한다.

## Stop Hook으로 Git 상태 체크

AI 작업이 끝날 때마다 커밋되지 않은 변경사항이 있으면 알려주는 훅이다.

```bash
#!/bin/bash
UNCOMMITTED=$(git status --porcelain 2>/dev/null)
if [ -n "$UNCOMMITTED" ]; then
  echo '{"systemMessage": "⚠️ 커밋되지 않은 변경사항이 있습니다."}'
fi
```

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/stop-hook-git-check.sh"
          }
        ]
      }
    ]
  }
}
```

`systemMessage` 키를 JSON으로 stdout에 출력하면 Claude Code UI에 메시지가 표시된다.

## 주의사항

훅이 실패해도 기본적으로 작업은 계속된다. 블로킹 동작이 필요하면 `continue: false`를 JSON으로 반환해야 한다.

```json
{ "continue": false, "stopReason": "빌드 실패로 인해 중단합니다." }
```

하지만 대부분의 포매터/린터 훅은 `|| true`로 끝내서 조용히 실패하게 두는 것이 좋다.

## 결론

훅을 잘 설계하면 AI와 작업할 때 반복적인 "이것도 해줘"를 없앨 수 있다. 핵심은 **AI가 코드를 쓸 때마다 자동으로 품질 게이트가 작동하는 구조**를 만드는 것이다.
