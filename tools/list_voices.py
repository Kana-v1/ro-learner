"""
List every voice in your Azure region that can speak Romanian.

    python tools/list_voices.py

Beyond the two dedicated ro-RO voices, Azure's multilingual and HD voices
(names containing MultilingualNeural or DragonHD) speak the auto-detected
language of the input, so they are usable as extra Romanian speakers — with
the caveat that they carry a trace of their home locale's accent.
"""
import json, os, sys, urllib.request

region = os.environ.get("AZURE_SPEECH_REGION", "westeurope")
key = os.environ.get("AZURE_SPEECH_KEY")
if not key:
    sys.exit("AZURE_SPEECH_KEY is not set")

req = urllib.request.Request(
    f"https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list",
    headers={"Ocp-Apim-Subscription-Key": key})
voices = json.load(urllib.request.urlopen(req, timeout=60))

native = [v for v in voices if v["Locale"] == "ro-RO"]
multi = [v for v in voices
         if any(t in v["ShortName"] for t in ("Multilingual", "DragonHD"))]

print(f"region {region}: {len(voices)} voices total\n")
print(f"── native Romanian ({len(native)}) ──")
for v in native:
    print(f"  {v['ShortName']:44} {v['Gender']:7} {v.get('Status','')}")

print(f"\n── multilingual / HD, can speak Romanian ({len(multi)}) ──")
for v in sorted(multi, key=lambda v: (v["Gender"], v["ShortName"])):
    print(f"  {v['ShortName']:44} {v['Gender']:7} {v.get('Status','')}")
