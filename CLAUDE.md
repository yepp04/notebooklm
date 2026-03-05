# NotebookLM Research Automation

YouTube 영상 검색 → NotebookLM 소스 업로드 → 분석 → 결과물 생성 자동화 프로젝트

## 프로젝트 구조

```
notebooklm/
├── .claude/skills/
│   ├── yt-search.md              # YouTube 검색 스킬
│   └── notebooklm-research.md    # NotebookLM 리서치 스킬
├── scripts/
│   └── yt_search.py              # YouTube 검색 스크립트 (yt-dlp 기반)
├── output/                        # 생성된 결과물 저장 폴더
├── CLAUDE.md                      # 이 파일
└── README.md
```

## 필수 도구

- **yt-dlp**: YouTube 검색 및 메타데이터 추출
- **notebooklm-py**: NotebookLM API 클라이언트 (비공식)
- **Python 3.10+**

## 워크플로우

### 통합 리서치 워크플로우

1. `python scripts/yt_search.py -q "검색어" -n 10 -o results.json` → YouTube 검색
2. `notebooklm create "노트북 이름"` → 노트북 생성
3. `notebooklm source add "URL"` → 소스 추가 (반복)
4. `notebooklm ask "질문"` → 분석
5. `notebooklm generate <type>` → 결과물 생성 (infographic, audio, slide-deck, mind-map, quiz, flashcards)
6. `notebooklm download <type> ./output/파일명` → 다운로드

### 개별 명령어 참조

YouTube 검색 상세: `.claude/skills/yt-search.md`
NotebookLM 명령어 상세: `.claude/skills/notebooklm-research.md`

## 인증

- NotebookLM 인증: `notebooklm login` (Google 계정)
- 인증 확인: `notebooklm auth check --test`
- 인증 정보 위치: `~/.notebooklm/storage_state.json`
- WSL 환경에서는 Windows 측에서 로그인 후 storage_state.json 복사

## 주의사항

- notebooklm-py는 비공식 API를 사용 (프로토타입/리서치용)
- Rate limit 주의: 소스 추가 시 2-3초 간격 권장
- 인증 쿠키는 1-2주마다 갱신 필요
- output/ 폴더에 생성된 파일은 git에 포함하지 않을 것
