"""
Render the same Romanian test phrase in several voices, side by side, so you
can pick by ear instead of by name.

    python tools/sample_voices.py ro-RO-EmilNeural ro-RO-AlinaNeural en-US-AndrewMultilingualNeural
    python tools/sample_voices.py --rate 0.9 ro-RO-EmilNeural

Writes samples/<voice>__<rate>.mp3. Costs about 200 characters per voice.
"""
import argparse, os, pathlib, sys, urllib.request
from xml.sax.saxutils import escape

PHRASE = ("Bună ziua! Eu sunt Radu. Dumneavoastră sunteți din Moldova? "
          "Nu, eu sunt din Chișinău. Sunt moldovean. "
          "bărbat, doamnă, ești, dimineața, în, român.")

ap = argparse.ArgumentParser()
ap.add_argument("voices", nargs="+")
ap.add_argument("--rate", type=float, default=1.0)
ap.add_argument("--text", default=PHRASE)
args = ap.parse_args()

key = os.environ.get("AZURE_SPEECH_KEY")
if not key:
    sys.exit("AZURE_SPEECH_KEY is not set")
region = os.environ.get("AZURE_SPEECH_REGION", "westeurope")
out = pathlib.Path("samples")
out.mkdir(exist_ok=True)

for voice in args.voices:
    inner = escape(args.text)
    if abs(args.rate - 1.0) > 0.01:
        inner = f'<prosody rate="{args.rate:.2f}">{inner}</prosody>'
    ssml = ('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xml:lang="ro-RO"><voice name="{voice}">{inner}</voice></speak>')
    req = urllib.request.Request(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        data=ssml.encode("utf-8"),
        headers={"Ocp-Apim-Subscription-Key": key,
                 "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": "audio-24khz-160kbitrate-mono-mp3",
                 "User-Agent": "romanian-podcast"})
    path = out / f"{voice}__{args.rate:.2f}.mp3"
    path.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    print(f"  {path}")
