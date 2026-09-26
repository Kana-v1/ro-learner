"""
The app's guide voice: a few short English phrases rendered once with a natural
Azure voice and bundled into the app as app/RoLearner/Coach/<key>.mp3. The app
plays them for its prompts and verdicts instead of iOS's built-in speech, which
sounds robotic and reports "finished" before the audio actually ends (so the
episode talked over it). A bundled clip has an exact length.

    export AZURE_SPEECH_KEY=... AZURE_SPEECH_REGION=westeurope
    python3 tools/make_coach_voice.py                            # default voice
    python3 tools/make_coach_voice.py --voice en-US-AndrewMultilingualNeural

The keys must match Coach.Line in app/RoLearner/Coach.swift; the texts are what
the app falls back to saying with the system voice while a clip is missing.
Re-running re-renders only phrases whose clip is missing (--force for all).
"""
import argparse
import os
import sys
from pathlib import Path

import render

ROOT = Path(__file__).resolve().parent.parent   # the project root
OUT = ROOT / "app" / "RoLearner" / "Coach"

# A voice distinct from the episodes' narrator (en-US-AndrewNeural), so the app
# guiding you never sounds like the lesson itself.
DEFAULT_VOICE = "en-US-AvaMultilingualNeural"

PHRASES = {
    "right_1": "Right.",
    "right_2": "That's it.",
    "right_3": "Good.",
    "almost": "Almost.",
    "not_quite": "Not quite.",
    "no_answer": "I didn't catch that.",
    "once_more_miss": "Not quite. Once more.",
    "once_more_silence": "I didn't catch that. Try once more.",
    "second_chance": "Second chance. Let's go over the ones you missed.",
    "episode_done": "That's the episode. Nice work.",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default=DEFAULT_VOICE, help=f"Azure voice (default {DEFAULT_VOICE})")
    ap.add_argument("--force", action="store_true", help="re-render every phrase")
    args = ap.parse_args()
    if not os.environ.get("AZURE_SPEECH_KEY"):
        sys.exit("AZURE_SPEECH_KEY is not set")

    OUT.mkdir(parents=True, exist_ok=True)
    todo = [k for k in PHRASES if args.force or not (OUT / f"{k}.mp3").exists()]
    print(f"{len(todo)} phrase(s) to render with {args.voice}")
    for k in todo:
        audio = render.synth_azure(PHRASES[k], args.voice, 1.0, "en-US")
        (OUT / f"{k}.mp3").write_bytes(audio)
        print(f"  {k:18} {PHRASES[k]}")
    print(f"done: {OUT}")


if __name__ == "__main__":
    main()
