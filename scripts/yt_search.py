#!/usr/bin/env python3
"""yt-dlp를 사용하여 YouTube 영상을 검색하고 메타데이터를 추출하는 스크립트.

NotebookLM 리서치 자동화 워크플로우의 첫 단계로,
검색된 영상의 URL을 NotebookLM 소스로 추가하는 데 활용된다.

사용 예시:
    # JSON 형식으로 10개 검색 (기본값)
    python scripts/yt_search.py -q "AI 에이전트"

    # 텍스트 형식으로 5개 검색
    python scripts/yt_search.py -q "AI 에이전트" -n 5 -f text

    # 파일로 저장
    python scripts/yt_search.py -q "AI 에이전트" -n 20 -o results.json

필수 의존성:
    pip install yt-dlp
"""

import argparse
import json
import subprocess
import sys


def parse_args():
    """커맨드라인 인자를 파싱한다.

    Returns:
        argparse.Namespace: 파싱된 인자 객체
            - query (str): 검색어 (필수)
            - count (int): 결과 수 (기본값: 10)
            - output (str | None): 출력 파일 경로 (None이면 stdout)
            - format (str): 출력 형식 ("json" 또는 "text", 기본값: "json")
    """
    parser = argparse.ArgumentParser(
        description="Search YouTube and extract video metadata using yt-dlp."
    )
    parser.add_argument(
        "--query", "-q",
        required=True,
        help="Search query string",
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=10,
        help="Number of results (default: 10)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (optional, prints to stdout if not provided)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "text"],
        default="json",
        help="Output format: json or text (default: json)",
    )
    return parser.parse_args()


def format_date(raw_date):
    """yt-dlp의 날짜 형식(YYYYMMDD)을 사람이 읽기 쉬운 형식(YYYY-MM-DD)으로 변환한다.

    Args:
        raw_date (str | None): yt-dlp가 반환하는 날짜 문자열. 예: "20250115"

    Returns:
        str | None: 변환된 날짜 문자열. 예: "2025-01-15"
                    변환 불가능한 형식이면 원본 문자열을 그대로 반환한다.
    """
    if raw_date and len(raw_date) == 8 and raw_date.isdigit():
        return f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
    return raw_date


def search_youtube(query, count):
    """yt-dlp의 ytsearch 기능으로 YouTube를 검색하고 영상 메타데이터를 추출한다.

    yt-dlp를 서브프로세스로 실행하며, --dump-json --flat-playlist 옵션을 사용하여
    실제 영상을 다운로드하지 않고 메타데이터만 가져온다.

    Args:
        query (str): YouTube 검색어
        count (int): 가져올 검색 결과 수

    Returns:
        list[dict]: 영상 메타데이터 딕셔너리 리스트. 각 딕셔너리의 키:
            - title (str): 영상 제목
            - url (str): 영상 URL
            - channel (str): 채널명
            - channel_url (str): 채널 URL
            - view_count (int): 조회수
            - upload_date (str): 업로드 날짜 (YYYY-MM-DD 형식)
            - duration (int): 영상 길이 (초)
            - duration_string (str): 영상 길이 (사람이 읽는 형식, 예: "10:30")
            - description (str): 영상 설명
            - thumbnail (str): 썸네일 이미지 URL
            - like_count (int): 좋아요 수

    Raises:
        SystemExit: yt-dlp가 설치되지 않았거나, 실행 중 오류 발생 시 프로그램 종료
    """
    # yt-dlp의 ytsearch 프로토콜: "ytsearch{개수}:{검색어}" 형식
    search_url = f"ytsearch{count}:{query}"
    cmd = [
        "yt-dlp",
        "--dump-json",       # 메타데이터를 JSON으로 출력 (다운로드하지 않음)
        "--flat-playlist",   # 플레이리스트를 펼쳐서 개별 영상 정보만 추출
        "--no-warnings",     # 경고 메시지 숨김
        search_url,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError:
        # yt-dlp가 PATH에 없는 경우
        print("Error: yt-dlp is not installed or not found in PATH.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running yt-dlp: {e}", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        err = result.stderr.strip()
        print(f"Error: yt-dlp exited with code {result.returncode}.", file=sys.stderr)
        if err:
            print(err, file=sys.stderr)
        sys.exit(1)

    # yt-dlp는 각 영상의 JSON을 한 줄씩 출력한다 (JSONL 형식)
    videos = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            # 파싱 불가능한 줄은 건너뛴다
            continue

        # yt-dlp 버전에 따라 필드명이 다를 수 있으므로 fallback 처리
        video = {
            "title": data.get("title"),
            "url": data.get("url") or data.get("webpage_url"),
            "channel": data.get("channel") or data.get("uploader"),
            "channel_url": data.get("channel_url") or data.get("uploader_url"),
            "view_count": data.get("view_count"),
            "upload_date": format_date(data.get("upload_date")),
            "duration": data.get("duration"),
            "duration_string": data.get("duration_string"),
            "description": data.get("description"),
            "thumbnail": data.get("thumbnail"),
            "like_count": data.get("like_count"),
        }
        videos.append(video)

    return videos


def render_text(videos, query):
    """영상 목록을 터미널에서 읽기 좋은 텍스트 형식으로 변환한다.

    Args:
        videos (list[dict]): search_youtube()가 반환한 영상 메타데이터 리스트
        query (str): 원본 검색어 (헤더에 표시용)

    Returns:
        str: 포맷팅된 텍스트 문자열
    """
    lines = []
    lines.append(f"Search query : {query}")
    lines.append(f"Total results: {len(videos)}")
    lines.append("")

    for idx, v in enumerate(videos, start=1):
        lines.append(f"[{idx}] {v['title']}")
        lines.append(f"    URL      : {v['url']}")
        lines.append(f"    Channel  : {v['channel']} ({v['channel_url']})")
        lines.append(f"    Duration : {v['duration_string']} ({v['duration']}s)")
        lines.append(f"    Views    : {v['view_count']}")
        lines.append(f"    Likes    : {v['like_count']}")
        lines.append(f"    Uploaded : {v['upload_date']}")
        lines.append(f"    Thumbnail: {v['thumbnail']}")
        # 설명은 120자까지만 표시 (줄바꿈은 공백으로 치환)
        desc = v["description"] or ""
        short_desc = desc[:120].replace("\n", " ")
        if len(desc) > 120:
            short_desc += "..."
        lines.append(f"    Desc     : {short_desc}")
        lines.append("")

    return "\n".join(lines)


def render_json(videos, query):
    """영상 목록을 JSON 형식으로 변환한다.

    출력 구조:
        {
            "summary": { "query": "...", "total_results": N },
            "videos": [ ... ]
        }

    Args:
        videos (list[dict]): search_youtube()가 반환한 영상 메타데이터 리스트
        query (str): 원본 검색어

    Returns:
        str: JSON 문자열 (ensure_ascii=False로 한글 등 유니코드 보존)
    """
    output = {
        "summary": {
            "query": query,
            "total_results": len(videos),
        },
        "videos": videos,
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def main():
    """메인 실행 함수.

    1. 커맨드라인 인자 파싱
    2. YouTube 검색 실행
    3. 지정된 형식(json/text)으로 변환
    4. 파일 또는 stdout으로 출력
    """
    args = parse_args()

    videos = search_youtube(args.query, args.count)

    if not videos:
        print("No results found.", file=sys.stderr)
        sys.exit(0)

    # 지정된 형식으로 렌더링
    if args.format == "text":
        content = render_text(videos, args.query)
    else:
        content = render_json(videos, args.query)

    # 출력: 파일 경로가 지정되면 파일로, 아니면 stdout으로
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(content)
                if not content.endswith("\n"):
                    fh.write("\n")
            print(f"Results written to {args.output}", file=sys.stderr)
        except OSError as e:
            print(f"Error writing to {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(content)


if __name__ == "__main__":
    main()
