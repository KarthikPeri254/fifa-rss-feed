import json
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path

BASE_URL = "https://github.com/KarthikPeri254/fifa-rss-feed"
INPUT_FILE = Path("results.json")
OUTPUT_FILE = Path("rss.xml")


def parse_time(value: str) -> datetime:
    if not value:
        return datetime.now(timezone.utc)

    # Supports format like 2026-06-11T22:30:00Z
    value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)


def build_item(match: dict) -> str:
    pub_dt = parse_time(match.get("publishedTime", ""))
    pub_date = format_datetime(pub_dt)

    title = "|".join([
        "FIFA_RESULT",
        str(match["matchId"]),
        str(match["teamA"]),
        str(match["teamB"]),
        str(match["teamAScore"]),
        str(match["teamBScore"]),
        str(match["winner"]),
        str(match["scoreText"]),
        str(match["matchStatus"])
    ])

    guid = f"{match['matchId']}-final"

    description = (
        f"MatchID: {match['matchId']} | "
        f"Match: {match['teamA']} vs {match['teamB']} | "
        f"Score: {match['scoreText']} | "
        f"Winner: {match['winner']} | "
        f"Status: {match['matchStatus']}"
    )

    return f"""
    <item>
      <title>{escape(title)}</title>
      <link>{escape(match["sourceLink"])}</link>
      <guid isPermaLink="false">{escape(guid)}</guid>
      <pubDate>{escape(pub_date)}</pubDate>
      <description>{escape(description)}</description>
    </item>
"""


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("results.json not found")

    matches = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    items = "\n".join(build_item(match) for match in matches)

    now = format_datetime(datetime.now(timezone.utc))

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>FIFA Match Results Feed</title>
    <link>{BASE_URL}/rss.xml</link>
    <description>Controlled RSS feed for FIFA match results</description>
    <language>en-us</language>
    <lastBuildDate>{now}</lastBuildDate>
    {items}
  </channel>
</rss>
"""

    OUTPUT_FILE.write_text(rss, encoding="utf-8")
    print("rss.xml generated successfully")


if __name__ == "__main__":
    main()
