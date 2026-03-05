#!/usr/bin/env python3
"""Search YouTube using yt-dlp and extract video metadata."""

import argparse
import json
import subprocess
import sys


def parse_args():
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
    """Convert YYYYMMDD to YYYY-MM-DD. Return original string on failure."""
    if raw_date and len(raw_date) == 8 and raw_date.isdigit():
        return f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
    return raw_date


def search_youtube(query, count):
    """Run yt-dlp search and return a list of video metadata dicts."""
    search_url = f"ytsearch{count}:{query}"
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--flat-playlist",
        "--no-warnings",
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

    videos = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

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
    """Return a human-readable string for the list of videos."""
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
        desc = v["description"] or ""
        short_desc = desc[:120].replace("\n", " ")
        if len(desc) > 120:
            short_desc += "..."
        lines.append(f"    Desc     : {short_desc}")
        lines.append("")

    return "\n".join(lines)


def render_json(videos, query):
    """Return a JSON string with video list and summary."""
    output = {
        "summary": {
            "query": query,
            "total_results": len(videos),
        },
        "videos": videos,
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def main():
    args = parse_args()

    videos = search_youtube(args.query, args.count)

    if not videos:
        print("No results found.", file=sys.stderr)
        sys.exit(0)

    if args.format == "text":
        content = render_text(videos, args.query)
    else:
        content = render_json(videos, args.query)

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
