# YouTube Search Skill

## Trigger

이 스킬은 다음과 같은 요청에서 활성화됩니다:
- YouTube 영상 검색 요청
- "YouTube에서 ~~ 찾아줘", "유튜브 검색"
- 영상 리서치, 트렌드 분석을 위한 영상 수집

## 사전 조건

- `yt-dlp` 패키지 설치 필요 (`pip install yt-dlp`)
- Python 3.10+

## 사용법

### 기본 검색

```bash
python scripts/yt_search.py --query "검색어" --count 10
```

### 옵션

| 옵션 | 단축 | 설명 | 기본값 |
|------|------|------|--------|
| `--query` | `-q` | 검색어 (필수) | - |
| `--count` | `-n` | 결과 수 | 10 |
| `--output` | `-o` | 출력 파일 경로 | stdout |
| `--format` | `-f` | 출력 형식 (json/text) | json |

### 예시

```bash
# JSON 형식으로 10개 검색
python scripts/yt_search.py -q "claude code skills" -n 10

# 텍스트 형식으로 출력
python scripts/yt_search.py -q "AI 자동화" -n 5 -f text

# 파일로 저장
python scripts/yt_search.py -q "notebooklm tutorial" -n 20 -o results.json
```

## 출력 형식 (JSON)

```json
{
  "query": "검색어",
  "count": 10,
  "results": [
    {
      "title": "영상 제목",
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "channel": "채널명",
      "channel_url": "https://www.youtube.com/channel/CHANNEL_ID",
      "view_count": 12345,
      "upload_date": "2025-01-15",
      "duration": 600,
      "duration_string": "10:00",
      "description": "영상 설명",
      "thumbnail": "https://...",
      "like_count": 100
    }
  ]
}
```

## NotebookLM 연동

검색 결과의 URL을 NotebookLM에 소스로 추가할 수 있습니다:

```bash
# 1. 검색 결과를 파일로 저장
python scripts/yt_search.py -q "claude code" -n 10 -o results.json

# 2. 결과에서 URL 추출 후 NotebookLM에 추가
notebooklm source add "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 워크플로우 통합

이 스킬은 `notebooklm-research` 스킬과 함께 사용됩니다:
1. YouTube 검색으로 영상 목록 수집
2. NotebookLM 노트북 생성
3. 검색된 영상 URL을 소스로 추가
4. 분석 및 결과물 생성
