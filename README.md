# NotebookLM Research Automation

YouTube 영상 검색부터 NotebookLM 분석, 결과물 생성까지 한번에 자동화하는 CLI 도구.

## 설치

### 필수 요구사항

- Python 3.10+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube 검색/메타데이터 추출
- [notebooklm-py](https://github.com/nichochar/notebooklm-py) — NotebookLM CLI 클라이언트 (비공식)

```bash
pip install yt-dlp "notebooklm-py[browser]"
playwright install chromium
```

### NotebookLM 인증

```bash
# Google 계정으로 로그인
notebooklm login

# 인증 확인
notebooklm auth check --test
```

> **WSL 사용자:** 브라우저 로그인이 안 될 수 있습니다. Windows에서 로그인 후 `~/.notebooklm/storage_state.json`을 WSL로 복사하세요.

## 사용법

### 1. YouTube 검색

```bash
# 기본 검색 (JSON, 10개)
python scripts/yt_search.py -q "검색어"

# 텍스트 형식으로 5개 검색
python scripts/yt_search.py -q "AI 자동화" -n 5 -f text

# 파일로 저장
python scripts/yt_search.py -q "notebooklm tutorial" -n 20 -o results.json
```

| 옵션 | 단축 | 설명 | 기본값 |
|------|------|------|--------|
| `--query` | `-q` | 검색어 (필수) | - |
| `--count` | `-n` | 결과 수 | 10 |
| `--output` | `-o` | 출력 파일 경로 | stdout |
| `--format` | `-f` | 출력 형식 (`json` / `text`) | `json` |

### 2. NotebookLM 노트북 생성

```bash
notebooklm create "리서치 주제명"
```

### 3. 소스 추가

```bash
# YouTube URL
notebooklm source add "https://www.youtube.com/watch?v=VIDEO_ID"

# 웹 URL
notebooklm source add "https://example.com/article"

# 텍스트
notebooklm source add --text "분석할 텍스트 내용"

# 파일
notebooklm source add --file ./document.pdf
```

### 4. 분석

```bash
notebooklm ask "이 영상들의 핵심 주제와 공통 패턴은?"
```

### 5. 결과물 생성 및 다운로드

```bash
# 오디오 오버뷰 (팟캐스트 스타일)
notebooklm generate audio "핵심 내용을 요약해줘" --wait
notebooklm download audio ./output/podcast.mp3

# 인포그래픽
notebooklm generate infographic --orientation landscape
notebooklm download infographic ./output/infographic.png

# 슬라이드 덱
notebooklm generate slide-deck
notebooklm download slide-deck ./output/slides.pdf

# 마인드맵
notebooklm generate mind-map

# 퀴즈 / 플래시카드
notebooklm generate quiz --difficulty medium
notebooklm generate flashcards
```

## 통합 워크플로우 예시

"AI 디자인" 관련 YouTube 영상을 모아서 분석하고 인포그래픽을 생성하는 전체 과정:

```bash
# 1. YouTube 검색
python scripts/yt_search.py -q "AI design workflow" -n 10 -o results.json

# 2. 노트북 생성
notebooklm create "AI 디자인 리서치"

# 3. 소스 추가 (검색 결과의 URL을 하나씩)
notebooklm source add "https://www.youtube.com/watch?v=abc123"
notebooklm source add "https://www.youtube.com/watch?v=def456"
# ...

# 4. 분석
notebooklm ask "핵심 주제와 실무 적용 방법을 정리해줘"

# 5. 결과물 생성 및 다운로드
notebooklm generate infographic --orientation landscape
notebooklm download infographic ./output/ai-design-infographic.png
```

## 기타 명령어

```bash
# 노트북 목록
notebooklm list

# 노트북 선택
notebooklm use <notebook_id>

# 소스 목록
notebooklm source list

# 노트북 삭제
notebooklm delete <notebook_id>
```

## 주의사항

- `notebooklm-py`는 비공식 API 기반입니다. 프로토타입/리서치 용도로 사용하세요.
- 소스 추가 시 2-3초 간격을 두세요 (rate limit).
- 노트북당 소스는 최대 약 50개입니다.
- 인증 쿠키는 1-2주마다 갱신이 필요합니다 (`notebooklm login`).
- `output/` 폴더의 생성된 파일은 `.gitignore`에 포함되어 있습니다.
