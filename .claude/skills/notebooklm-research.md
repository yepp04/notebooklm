# NotebookLM Research Skill

## Trigger

이 스킬은 다음과 같은 요청에서 활성화됩니다:
- NotebookLM을 사용한 리서치/분석 요청
- "NotebookLM으로 분석해줘", "노트북 만들어서 정리해줘"
- 인포그래픽, 팟캐스트, 슬라이드, 마인드맵, 퀴즈 생성 요청
- YouTube 영상 분석 + 결과물 생성 통합 워크플로우

## 사전 조건

- `notebooklm-py` 패키지 설치 (`pip install "notebooklm-py[browser]"`)
- `playwright install chromium` 실행 완료
- `notebooklm login`으로 Google 인증 완료
- 인증 상태 확인: `notebooklm auth check --test`

## 핵심 명령어

### 노트북 관리

```bash
# 노트북 생성
notebooklm create "노트북 이름"

# 노트북 목록
notebooklm list

# 노트북 선택 (이후 명령에서 사용)
notebooklm use <notebook_id>

# 노트북 삭제
notebooklm delete <notebook_id>
```

### 소스 관리

```bash
# YouTube URL 소스 추가
notebooklm source add "https://www.youtube.com/watch?v=VIDEO_ID"

# 웹 URL 소스 추가
notebooklm source add "https://example.com/article"

# 텍스트 소스 추가
notebooklm source add --text "분석할 텍스트 내용"

# 파일 소스 추가
notebooklm source add --file ./document.pdf

# 소스 목록 확인
notebooklm source list
```

### 질문 및 분석

```bash
# 노트북에 질문하기
notebooklm ask "이 영상들에서 가장 많이 언급되는 주제는?"

# 노트 생성
notebooklm note "핵심 내용 요약"
```

### 결과물 생성

```bash
# 오디오 오버뷰 (팟캐스트 스타일)
notebooklm generate audio "핵심 내용을 요약해줘" --wait

# 인포그래픽
notebooklm generate infographic --orientation landscape

# 슬라이드 덱
notebooklm generate slide-deck

# 마인드맵
notebooklm generate mind-map

# 퀴즈
notebooklm generate quiz --difficulty medium

# 플래시카드
notebooklm generate flashcards
```

### 다운로드

```bash
# 오디오 다운로드
notebooklm download audio ./output/podcast.mp3

# 인포그래픽 다운로드
notebooklm download infographic ./output/infographic.png

# 슬라이드 다운로드
notebooklm download slide-deck ./output/slides.pdf
```

## 통합 워크플로우 (YouTube → NotebookLM → 결과물)

사용자가 "YouTube 영상을 검색해서 NotebookLM으로 분석해줘" 같은 통합 요청을 하면 다음 순서로 진행합니다:

### Step 1: YouTube 검색
```bash
python scripts/yt_search.py -q "검색어" -n 10 -o /tmp/yt_results.json
```

### Step 2: NotebookLM 노트북 생성
```bash
notebooklm create "리서치 주제명"
```

### Step 3: 검색된 영상 URL을 소스로 추가
```bash
# JSON 결과에서 URL을 추출하여 하나씩 추가
notebooklm source add "https://www.youtube.com/watch?v=VIDEO_ID_1"
notebooklm source add "https://www.youtube.com/watch?v=VIDEO_ID_2"
# ... 반복
```

### Step 4: 분석 질문
```bash
notebooklm ask "이 영상들의 핵심 주제와 공통 패턴을 분석해줘"
```

### Step 5: 결과물 생성
```bash
# 사용자가 요청한 형식으로 생성
notebooklm generate infographic --orientation landscape
notebooklm generate audio "주요 발견사항을 요약해줘" --wait
```

### Step 6: 다운로드
```bash
notebooklm download infographic ./output/infographic.png
notebooklm download audio ./output/podcast.mp3
```

## 주의사항

1. **Rate Limit**: 소스 추가 시 너무 빠르게 연속 요청하지 말 것 (2-3초 간격 권장)
2. **소스 제한**: 노트북당 최대 소스 수 제한이 있을 수 있음 (보통 50개)
3. **생성 시간**: audio, infographic 등은 생성에 시간이 걸림 (`--wait` 플래그 사용)
4. **인증 만료**: 쿠키가 만료되면 `notebooklm login`으로 재인증 필요
5. **WSL 환경**: 브라우저 기반 로그인이 안 될 수 있음 → Windows에서 로그인 후 `storage_state.json` 복사

## 에러 처리

```bash
# 인증 상태 확인
notebooklm auth check --test

# 인증 실패 시 재로그인
notebooklm login

# 노트북 ID를 모를 때
notebooklm list
```
