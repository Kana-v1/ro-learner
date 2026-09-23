"""
Build a podcast RSS feed from the rendered episodes.

    python make_feed.py --base-url https://pub-xxxx.r2.dev/ro-a7f3c1

Scans out/ for episode_NN.mp3, reads the matching script in episodes/ for the
title and chapter list, and writes out/feed.xml. Upload everything in out/ to
one folder on any static host, then subscribe to <base-url>/feed.xml in
Pocket Casts or AntennaPod.

Put a random string in the path. The feed is not listed anywhere, but the URL
is the only thing keeping it private, so make it unguessable.
"""
import argparse, json, re, subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"
PODCAST = "https://podcastindex.org/namespace/1.0"


def probe(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True)
    return float(out.stdout.strip())


def hms(seconds: float) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{s:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True,
                    help="folder URL the mp3s will live at, no trailing slash")
    ap.add_argument("--title", default="Limba care ne unește — audio")
    ap.add_argument("--dir", default=None, help="directory of rendered mp3s")
    ap.add_argument("--scripts", default=None, help="directory of episode JSON")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    base = args.base_url.rstrip("/")
    root = Path(args.dir) if args.dir else here / "out"
    scripts = Path(args.scripts) if args.scripts else here / "episodes"
    files = sorted(root.glob("episode_[0-9][0-9]*.mp3"))
    if not files:
        raise SystemExit(f"no episode_NN.mp3 found in {root}")

    # Episode 1 gets the oldest date so players order the course correctly and
    # "play oldest first" does the right thing out of the box.
    start = datetime.now(timezone.utc) - timedelta(days=len(files))

    items = []
    for i, mp3 in enumerate(files):
        # Filenames are episode_NN.mp3, or episode_NNa / episode_NNb when a
        # chapter is split across two episodes. label is the human lesson tag
        # (3a, 3b, or plain 4); part is "" for unsplit chapters.
        m = re.match(r"episode_(\d+)([a-z]?)", mp3.stem)
        num, part = int(m.group(1)), m.group(2)
        label = f"{num}{part}"
        meta_path = scripts / f"{mp3.stem}.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        title = meta.get("title", mp3.stem)
        chapters = [s["chapter"] for s in meta.get("segments", []) if "chapter" in s]
        desc = meta.get("source", "")
        if chapters:
            desc += "\n\n" + " · ".join(chapters)
        pub = (start + timedelta(days=i)).strftime("%a, %d %b %Y %H:%M:%S +0000")
        url = f"{base}/{mp3.name}"
        # itunes:episode must be a unique integer, so use the running position
        # rather than the lesson number — 3a and 3b would both be 3 and players
        # merge or hide duplicate numbers. The lesson tag stays in the title,
        # and pubDate (also positional) is what drives play order.
        items.append(f"""  <item>
   <title>{label}. {escape(title)}</title>
   <description>{escape(desc)}</description>
   <itunes:episode>{i + 1}</itunes:episode>
   <itunes:duration>{hms(probe(mp3))}</itunes:duration>
   <enclosure url="{escape(url)}" length="{mp3.stat().st_size}" type="audio/mpeg"/>
   <guid isPermaLink="false">romanian-lesson-{num:02d}{part}</guid>
   <pubDate>{pub}</pubDate>
  </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="{ITUNES}" xmlns:podcast="{PODCAST}">
 <channel>
  <title>{escape(args.title)}</title>
  <link>{escape(base)}/feed.xml</link>
  <description>Personal study audio generated from a Romanian A1 textbook.</description>
  <language>ro</language>
  <itunes:author>private</itunes:author>
  <itunes:explicit>false</itunes:explicit>
  <itunes:block>Yes</itunes:block>
  <podcast:locked>yes</podcast:locked>
{chr(10).join(items)}
 </channel>
</rss>
"""
    out = root / "feed.xml"
    out.write_text(feed, encoding="utf-8")
    print(f"{out}  {len(files)} episodes")
    print(f"subscribe to: {base}/feed.xml")


if __name__ == "__main__":
    main()
