# NotebookLM Research Automation

YouTube 영상 검색 → NotebookLM 소스 업로드 → 분석 → 결과물 생성까지의 리서치 워크플로우를 **Claude Code**와 함께 자동화하는 프로젝트.

이 프로젝트는 Claude Code의 [커스텀 스킬](https://docs.anthropic.com/en/docs/claude-code/skills) 시스템을 활용합니다. 자연어로 Claude에게 요청하면, 등록된 스킬이 자동으로 트리거되어 YouTube 검색과 NotebookLM 조작을 수행합니다.

## 프로젝트 구조

```
notebooklm/
├── .claude/skills/
│   ├── yt-search.md              # YouTube 검색 스킬 정의
│   └── notebooklm-research.md    # NotebookLM 리서치 스킬 정의
├── scripts/
│   └── yt_search.py              # YouTube 검색 스크립트 (yt-dlp 기반)
├── output/                        # 생성된 결과물 저장 폴더
├── CLAUDE.md                      # Claude Code 프로젝트 설정
└── README.md
```

## 설치

### 1. 필수 도구 설치

```bash
# Python 패키지
pip install yt-dlp "notebooklm-py[browser]"

# Playwright 브라우저 (notebooklm-py 인증에 필요)
playwright install chromium
```

### 2. NotebookLM 인증 설정

```bash
# Google 계정으로 로그인 (브라우저가 열림)
notebooklm login

# 인증이 정상적으로 되었는지 확인
notebooklm auth check --test
```

인증 정보는 `~/.notebooklm/storage_state.json`에 저장됩니다.

> **WSL 환경 주의:**
> WSL에서는 브라우저가 직접 열리지 않을 수 있습니다.
> 이 경우 Windows 측에서 `notebooklm login`을 실행하여 로그인한 뒤,
> 생성된 `storage_state.json` 파일을 WSL의 `~/.notebooklm/` 경로로 복사하세요.

### 3. Claude Code 설치

[Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)가 설치되어 있어야 합니다.

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# macOS (Homebrew)
brew install --cask claude-code

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Windows (WinGet)
winget install Anthropic.ClaudeCode
```

이 프로젝트 폴더에서 `claude`를 실행하면, `.claude/skills/` 아래의 스킬과 `CLAUDE.md`의 프로젝트 설정이 자동으로 로드됩니다.

---

## Claude Code와 함께 사용하기

이 프로젝트의 핵심 사용법입니다. 프로젝트 루트에서 `claude`를 실행한 뒤, 자연어로 요청하면 됩니다.

### YouTube 검색 스킬

다음과 같은 요청을 하면 `.claude/skills/yt-search.md` 스킬이 트리거됩니다:

```
> 유튜브에서 "AI 에이전트" 관련 영상 10개 찾아줘
> YouTube에서 notebooklm 튜토리얼 검색해줘
> AI 디자인 트렌드 영상 20개 찾아서 results.json에 저장해줘
```

Claude가 내부적으로 `scripts/yt_search.py`를 실행하여 검색 결과를 보여줍니다.

### NotebookLM 리서치 스킬

다음과 같은 요청을 하면 `.claude/skills/notebooklm-research.md` 스킬이 트리거됩니다:

```
> NotebookLM에 노트북 만들어서 이 영상들 분석해줘
> 이 유튜브 링크들을 NotebookLM에 넣고 핵심 주제를 정리해줘
> 인포그래픽으로 만들어줘
> 팟캐스트 스타일로 오디오 요약 생성해줘
```

### 통합 워크플로우 (한 번에 요청)

검색부터 결과물 생성까지 한 문장으로 요청할 수 있습니다:

```
> "AI 에이전트 개발" 유튜브 영상 10개 검색해서 NotebookLM으로 분석하고 인포그래픽 만들어줘
```

이 경우 Claude가 아래 단계를 순서대로 자동 수행합니다:

1. `yt_search.py`로 YouTube 검색
2. `notebooklm create`로 노트북 생성
3. 검색된 영상 URL을 `notebooklm source add`로 하나씩 추가
4. `notebooklm ask`로 분석
5. `notebooklm generate`로 결과물 생성
6. `notebooklm download`로 `output/` 폴더에 다운로드

---

## 수동 CLI 사용법

Claude Code 없이 터미널에서 직접 명령어를 실행할 수도 있습니다.

### YouTube 검색

```bash
# 기본 검색 (JSON 형식, 10개)
python scripts/yt_search.py -q "검색어"

# 텍스트 형식으로 5개 검색
python scripts/yt_search.py -q "AI 자동화" -n 5 -f text

# 파일로 저장
python scripts/yt_search.py -q "notebooklm tutorial" -n 20 -o results.json
```

**옵션 목록:**

| 옵션 | 단축 | 설명 | 기본값 |
|------|------|------|--------|
| `--query` | `-q` | 검색어 (필수) | - |
| `--count` | `-n` | 결과 수 | 10 |
| `--output` | `-o` | 출력 파일 경로 | stdout |
| `--format` | `-f` | 출력 형식 (`json` / `text`) | `json` |

**출력 예시 (JSON):**

```json
{
  "summary": {
    "query": "AI agent",
    "total_results": 10
  },
  "videos": [
    {
      "title": "영상 제목",
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "channel": "채널명",
      "channel_url": "https://www.youtube.com/@channel",
      "view_count": 12345,
      "upload_date": "2025-01-15",
      "duration": 600,
      "duration_string": "10:00",
      "description": "영상 설명...",
      "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg",
      "like_count": 100
    }
  ]
}
```

### NotebookLM 노트북 관리

```bash
# 노트북 생성
notebooklm create "노트북 이름"

# 노트북 목록 조회
notebooklm list

# 특정 노트북 선택 (이후 명령에서 사용됨)
notebooklm use <notebook_id>

# 노트북 삭제
notebooklm delete <notebook_id>
```

### 소스 추가

```bash
# YouTube URL 추가
notebooklm source add "https://www.youtube.com/watch?v=VIDEO_ID"

# 웹 페이지 URL 추가
notebooklm source add "https://example.com/article"

# 텍스트 직접 추가
notebooklm source add --text "분석할 텍스트 내용"

# 로컬 파일 추가
notebooklm source add --file ./document.pdf

# 현재 소스 목록 확인
notebooklm source list
```

### 질문 및 분석

```bash
notebooklm ask "이 영상들에서 가장 많이 언급되는 주제는?"
notebooklm ask "핵심 주제와 실무 적용 방법을 정리해줘"
```

### 결과물 생성

```bash
# 오디오 오버뷰 (팟캐스트 스타일, 생성 완료까지 대기)
notebooklm generate audio "핵심 내용을 요약해줘" --wait

# 인포그래픽 (가로 방향)
notebooklm generate infographic --orientation landscape

# 슬라이드 덱
notebooklm generate slide-deck

# 마인드맵
notebooklm generate mind-map

# 퀴즈 (난이도 지정 가능)
notebooklm generate quiz --difficulty medium

# 플래시카드
notebooklm generate flashcards
```

### 결과물 다운로드

```bash
# 오디오 다운로드
notebooklm download audio ./output/podcast.mp3

# 인포그래픽 다운로드
notebooklm download infographic ./output/infographic.png

# 슬라이드 다운로드
notebooklm download slide-deck ./output/slides.pdf
```

---

## 수동 통합 워크플로우 예시

"AI 디자인" 관련 YouTube 영상을 모아서 분석하고 인포그래픽을 만드는 전체 과정:

```bash
# Step 1: YouTube 검색
python scripts/yt_search.py -q "AI design workflow 2025" -n 10 -o results.json

# Step 2: 노트북 생성
notebooklm create "AI 디자인 리서치"

# Step 3: 검색 결과에서 URL을 추출하여 소스 추가
#         (results.json의 videos[].url 값을 사용)
notebooklm source add "https://www.youtube.com/watch?v=abc123"
notebooklm source add "https://www.youtube.com/watch?v=def456"
notebooklm source add "https://www.youtube.com/watch?v=ghi789"
# ... 2-3초 간격으로 추가

# Step 4: 분석 질문
notebooklm ask "이 영상들의 핵심 주제와 공통 패턴을 분석해줘"

# Step 5: 결과물 생성
notebooklm generate infographic --orientation landscape

# Step 6: 다운로드
notebooklm download infographic ./output/ai-design-infographic.png
```

---

## 주의사항

- **비공식 API**: `notebooklm-py`는 비공식 API를 사용합니다. 프로토타입 및 개인 리서치 용도로만 사용하세요.
- **Rate Limit**: 소스 추가 시 2-3초 간격을 두세요. 너무 빠르게 연속 요청하면 차단될 수 있습니다.
- **소스 제한**: 노트북당 최대 약 50개의 소스를 추가할 수 있습니다.
- **인증 갱신**: 인증 쿠키는 1-2주마다 만료됩니다. `notebooklm login`으로 재인증하세요.
- **생성 시간**: 오디오, 인포그래픽 등의 결과물은 생성에 시간이 걸립니다. `--wait` 플래그를 사용하면 완료까지 대기합니다.
- **output 폴더**: 생성된 결과물은 `output/` 폴더에 저장되며, `.gitignore`에 포함되어 git에 커밋되지 않습니다.
