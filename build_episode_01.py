"""
Episode 01 — "Bună dimineața!" (Lecția 1, Limba care ne unește I)

Rewritten against the lesson-audio-script skill. The differences from the
first draft, in order of how much they matter:

  * The scene is a roll call on the first day of a course. Dana has a list and
    asks everyone the same two questions, so "Sunteți din...?" is heard three
    times and sounds like a person doing her job rather than a drill.
  * Dialogue drops subject pronouns, the way Romanian actually works, and the
    narrator turns that into the episode's second teaching point.
  * Coverage of the chapter's word list is asserted, not hoped for.
  * Glue items are declared explicitly and taught as whole chunks.

Emits episode_01.json.
"""
import json
import pathlib
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "episodes"
SPOKEN = json.loads((ROOT / "data" / "spoken.json").read_text(encoding="utf-8"))

# ── the chapter's vocabulary, from the textbook's own glossary ───────────────
REQUIRED = [
    "băiat", "fată", "bărbat", "femeie",
    "domn", "doamnă", "domnișoară",
    "bulgar", "francez", "găgăuz", "moldovean", "român", "rus", "ucrainean",
    "englez", "moldoveancă", "ucraineancă",
    "dumneata", "dumneavoastră",
    "sunt", "ești", "este", "suntem", "sunteți",
    "în", "din", "iar", "dar", "da", "nu",
]

# Items outside the chapter, spoken as fixed chunks with no grammar attached.
# The skill allows three or four; these are the four.
GLUE = {
    "domnul / doamna / domnișoara": "the -ul and -a endings mean 'the'",
    "scuzați": "sorry, excuse me",
    "Bălți": "a city in northern Moldova",
    "Ivanova": "a surname",
}

VOICE = {"nar": "en_narrator", "m": "ro_male", "f": "ro_female",
         "dana": "ro_dana", "radu": "ro_radu", "elena": "ro_elena"}

SLOW, NORMAL = 0.80, 1.0
P_REPEAT, P_SHORT, P_RECALL, P_SECTION = 1400, 400, 3500, 1000

seg: list[dict] = []
_n = 0


def add(type_, text, lang="en", voice="nar", rate=NORMAL, pause=P_SHORT, chapter=None):
    global _n
    _n += 1
    s = {"id": f"s{_n:03d}", "type": type_, "lang": lang, "voice": VOICE[voice],
         "text": text, "rate": rate, "pause_after_ms": pause}
    if chapter:
        s["chapter"] = chapter
    seg.append(s)


def narr(text, pause=P_SHORT, chapter=None):
    add("narration", text, "en", "nar", NORMAL, pause, chapter)


def ro(text, voice="m", rate=NORMAL, pause=P_REPEAT, type_="target"):
    add(type_, text, "ro", voice, rate, pause)


def teach(romanian, english, voice="m"):
    ro(romanian, voice, NORMAL, P_REPEAT)
    add("gloss", english, "en", "nar", NORMAL, P_SHORT)
    ro(romanian, voice, SLOW, P_REPEAT)


def drill(cue, romanian, voice="m"):
    add("prompt", cue, "en", "nar", NORMAL, P_RECALL)
    add("answer", romanian, "ro", voice, NORMAL, P_REPEAT)


# ── the dialogue ─────────────────────────────────────────────────────────────
# First morning of a language course. Dana works down a register. The scene
# was chosen because a register makes repetition of one question structure
# completely natural — the pedagogical repetition is the realism.
DIALOGUE = [
    ("dana",  "Bună dimineața! Eu sunt Dana."),
    ("dana",  "Domnul Radu Bărbulescu?"),
    ("radu",  "Da, eu sunt. Bună dimineața!"),
    ("dana",  "Sunteți din Chișinău?"),
    ("radu",  "Nu. Sunt din Bălți. Sunt moldovean."),
    ("dana",  "Doamna Elena Ivanova?"),
    ("elena", "Nu sunt doamnă! Sunt domnișoară."),
    ("dana",  "Ah, scuzați! Domnișoara Elena. Dumneavoastră sunteți din Chișinău?"),
    ("elena", "Da. Dar nu sunt moldoveancă. Sunt ucraineancă."),
    ("dana",  "Iar eu sunt din Chișinău. Sunt moldoveancă."),
    ("dana",  "La revedere! Pe curând!"),
    ("radu",  "La revedere!"),
]


def play_dialogue():
    for who, line in DIALOGUE:
        ro(line, who, NORMAL, 650, type_=f"line_{who}")


# ═══ 0. Cold open ════════════════════════════════════════════════════════════
add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
play_dialogue()
narr("Three people and a register, first morning of a language course. You "
     "caught a name or two — that is the right amount on a first listen. "
     "We come back to it at the end.", pause=P_SECTION)

# ═══ 1. Sounds ═══════════════════════════════════════════════════════════════
narr("Four letters first. Only the four that turned up in what you just heard.",
     pause=800, chapter="Sounds")

narr("Ă, an A wearing a little bowl. A dull vowel, the -er at the end of "
     "'water'. In bărbat, a man.")
ro("bărbat", "m", SLOW); ro("bărbat", "m")
narr("In doamnă, a lady.")
ro("doamnă", "f", SLOW); ro("doamnă", "f", pause=P_SECTION)

narr("Ș, an S with a comma under it. Just 'sh'. In domnișoară, miss.")
ro("domnișoară", "f", SLOW); ro("domnișoară", "f", pause=P_SECTION)

narr("Ț, a T with a comma under it. 'ts', as at the end of 'cats'. "
     "In dimineața, morning.")
ro("dimineața", "f", SLOW); ro("dimineața", "f")
narr("So: bună dimineața. Good morning.")
ro("Bună dimineața!", "f", SLOW); ro("Bună dimineața!", "f", pause=P_SECTION)

narr("And Î or Â — one sound, two spellings. Nothing like it in English: say "
     "'ee' with your tongue pulled back. In în, meaning in.")
ro("în", "m", SLOW); ro("în", "m")
narr("And in român, a Romanian.")
ro("român", "m", SLOW); ro("român", "m", pause=P_SECTION)

# ═══ 2. Vocabulary ═══════════════════════════════════════════════════════════
narr("Now the words, each one inside a phrase. Say every phrase out loud in "
     "the gap. Out loud — thinking it does not count.", pause=800,
     chapter="Vocabulary")

narr("Four kinds of person.")
for r, e, v in [("El este băiat.", "He is a boy.", "m"),
                ("Ea este fată.", "She is a girl.", "f"),
                ("El este bărbat.", "He is a man.", "m"),
                ("Ea este femeie.", "She is a woman.", "f")]:
    teach(r, e, v)

narr("Three ways to address someone. You heard all three during the roll call.")
teach("Bună ziua, domn!", "Good afternoon, sir.", "m")
teach("Bună ziua, doamnă!", "Good afternoon, madam.", "f")
teach("Bună seara, domnișoară!", "Good evening, miss.", "f")
narr("And when a title comes before a name, it grows an ending: domnul Radu, "
     "doamna Elena, domnișoara Elena. That ending is Romanian's word for "
     "'the', and it attaches to the back of the word instead of standing in "
     "front of it. Take it as a whole phrase for now.", pause=P_SECTION)

narr("Nationalities. Listen for the pattern rather than memorising ten "
     "separate words.", pause=600)
for r, e, v in [("Eu sunt moldovean.", "I am Moldovan — said by a man.", "m"),
                ("Eu sunt moldoveancă.", "I am Moldovan — said by a woman.", "f"),
                ("El este rus.", "He is Russian.", "m"),
                ("El este ucrainean.", "He is Ukrainian.", "m"),
                ("Ea este ucraineancă.", "She is Ukrainian.", "f"),
                ("El este bulgar.", "He is Bulgarian.", "m"),
                ("El este găgăuz.", "He is Gagauz.", "m"),
                ("El este român.", "He is Romanian.", "m"),
                ("El este francez.", "He is French.", "m"),
                ("El este englez.", "He is English.", "m")]:
    teach(r, e, v)
narr("There it is: the men's form ends in nothing in particular, the women's "
     "adds -că. Moldovean, moldoveancă. Ucrainean, ucraineancă. That one rule "
     "covers most of the list.", pause=P_SECTION)

narr("Two very small words that people mix up forever.")
teach("Sunt din Moldova.", "I am from Moldova.", "m")
teach("Sunt în Moldova.", "I am in Moldova.", "m")
narr("Din is from. În is in. Once more, slowly.")
ro("din", "m", SLOW); ro("în", "m", SLOW, pause=P_SECTION)

narr("And four connecting words.")
teach("Da.", "Yes.", "f")
teach("Nu.", "No.", "f")
teach("El este din Moldova, iar ea este din Ucraina.",
      "He is from Moldova, and she is from Ukraine.", "m")
teach("Sunt rus, dar el este român.", "I am Russian, but he is Romanian.", "m")

# ═══ 3. Grammar ══════════════════════════════════════════════════════════════
narr("Everything in this episode runs on one verb: a fi, to be. Six forms.",
     pause=800, chapter="The verb a fi")
for r, e in [("eu sunt", "I am"), ("tu ești", "you are"),
             ("el este", "he is"), ("ea este", "she is"),
             ("noi suntem", "we are"), ("voi sunteți", "you are, more than one"),
             ("ei sunt", "they are, men"), ("ele sunt", "they are, women")]:
    ro(r, "m", NORMAL, P_SHORT)
    add("gloss", e, "en", "nar", NORMAL, P_REPEAT)

narr("For the negative, put nu in front and change nothing else.", pause=600)
teach("Nu sunt rus.", "I am not Russian.", "m")
teach("Ea nu este din Rusia.", "She is not from Russia.", "f")

# ── the pro-drop moment ──────────────────────────────────────────────────────
narr("Now something worth stopping for. Listen to what Radu actually said when "
     "Dana asked where he was from.", pause=600, chapter="Dropping the pronoun")
ro("Nu. Sunt din Bălți. Sunt moldovean.", "radu", NORMAL, P_SECTION)
narr("Not eu sunt din Bălți. Just sunt din Bălți. Romanian usually leaves the "
     "pronoun out, because the verb ending already tells you who is speaking. "
     "Sunt can only mean I am.", pause=600)
narr("The pronoun comes back when you are pointing at someone in particular. "
     "Dana reads a name, and Radu answers:")
ro("Da, eu sunt.", "radu", NORMAL, P_REPEAT)
narr("Yes, that is me. There the eu is the whole point.", pause=600)
narr("So: drop it for plain statements, keep it for contrast. The drill below "
     "uses full forms because those need practice. In speech, let them go.",
     pause=P_SECTION)

# ═══ 4. Greetings ════════════════════════════════════════════════════════════
narr("Six phrases for arriving and leaving.", pause=600, chapter="Greetings")
for r, e in [("Bună dimineața!", "Good morning."),
             ("Bună ziua!", "Good afternoon."),
             ("Bună seara!", "Good evening."),
             ("Salut!", "Hi. Informal — for friends."),
             ("La revedere!", "Goodbye."),
             ("Pe curând!", "See you soon.")]:
    teach(r, e, "f")

narr("One more pair. Dumneavoastră is the respectful you — Dana used it with "
     "everyone on her list. Dumneata is a middle setting, polite but warmer.",
     pause=600)
teach("Dumneavoastră sunteți din Rusia?", "Are you from Russia?", "m")
teach("Dumneata ești din Ucraina?", "Are you from Ukraine?", "f")
narr("Note that dumneavoastră takes sunteți, the plural form, even for one "
     "person — the same move French makes with vous.", pause=P_SECTION)

# ═══ 4b. How people actually say it ══════════════════════════════════════════
# The textbook is from Chișinău, 2003. This block is where the episode admits
# that, and hands over the Bucharest spoken forms alongside the book's.
narr("Last section, and it is not from the textbook. That book was written in "
     "Chișinău in 2003. It teaches correct Romanian, not always spoken "
     "Romanian. So: what a Bucharest mouth actually produces.",
     pause=800, chapter="How people really say it")

narr("The book says el este, ea este. Correct, always. But listen:")
ro("El e bărbat.", "m", NORMAL, P_REPEAT)
ro("Ea e femeie.", "f", NORMAL, P_REPEAT)
narr("Just e. The commonest gap between written and spoken Romanian. Keep "
     "drilling este — the book builds on it — but expect e.", pause=600)

narr("We taught domnul Radu. In speech that final L falls off.")
ro("domnu' Radu", "m", SLOW, P_REPEAT)
ro("domnu' Radu", "m", NORMAL, P_REPEAT)
narr("Domnu', not domnul. Ordinary neutral speech, not sloppiness. Feminine "
     "doamna keeps its ending.", pause=600)

narr("Now the phrase our roll call should have had. On being introduced:")
teach("Îmi pare bine.", "Nice to meet you.", "f")
narr("Grammar far beyond this lesson. Take it whole.", pause=600)

narr("And two ways to stall while you think.")
teach("Păi...", "Well... — exactly like Russian ну.", "m")
narr("It opens a hesitant answer.")
ro("Păi, nu sunt din Chișinău.", "m", NORMAL, P_REPEAT)
narr("And deci — officially therefore, in speech just like English 'so'. "
     "Stretch it as long as you need.")
ro("Deci... eu sunt din Bălți.", "m", NORMAL, P_REPEAT)
narr("Both neutral. Safe with a colleague, in a shop, with a stranger.",
     pause=P_SECTION)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
narr("This is the part that does the work. I say it in English, you say it in "
     "Romanian out loud, then you hear it. Answer before you are sure — "
     "guessing and being corrected is what makes it stick.",
     pause=P_SECTION, chapter="Drill")

for cue, ans, v in [
    ("I am Moldovan — you are a man.", "Eu sunt moldovean.", "m"),
    ("I am Moldovan — you are a woman.", "Eu sunt moldoveancă.", "f"),
    ("She is Ukrainian.", "Ea este ucraineancă.", "f"),
    ("He is Bulgarian.", "El este bulgar.", "m"),
    ("He is from Russia.", "El este din Rusia.", "m"),
    ("We are from Moldova.", "Noi suntem din Moldova.", "m"),
    ("You are from Bulgaria — speaking to several people.",
     "Voi sunteți din Bulgaria.", "m"),
    ("They are from Moldova — a group of men.", "Ei sunt din Moldova.", "m"),
    ("You are a girl.", "Tu ești fată.", "f"),
    ("I am not French.", "Eu nu sunt francez.", "m"),
    ("She is not from Chișinău.", "Ea nu este din Chișinău.", "f"),
    ("He is not English, he is Gagauz.", "El nu este englez, el este găgăuz.", "m"),
    ("Are you from Ukraine? Politely, to one person.",
     "Dumneata ești din Ucraina?", "f"),
    ("Are you Russian? Respectfully.", "Dumneavoastră sunteți rus?", "m"),
    ("Good morning, madam!", "Bună dimineața, doamnă!", "f"),
    ("Good evening, miss!", "Bună seara, domnișoară!", "f"),
    ("Yes, I am from Moldova.", "Da, eu sunt din Moldova.", "m"),
    ("No, I am not Romanian.", "Nu, eu nu sunt român.", "m"),
    ("He is a man, she is a woman.", "El este bărbat, ea este femeie.", "m"),
    ("He is from Moldova, and she is from Ukraine.",
     "El este din Moldova, iar ea este din Ucraina.", "m"),
    ("I am in Moldova.", "Eu sunt în Moldova.", "m"),
    ("See you soon!", "Pe curând!", "f"),
    ("He is a man — the way you would actually say it.", "El e bărbat.", "m"),
    ("Nice to meet you.", "Îmi pare bine.", "f"),
    ("Well... I am not from Chișinău.", "Păi, nu sunt din Chișinău.", "m"),
]:
    drill(cue, ans, v)

# ═══ 6. Text from the book ═══════════════════════════════════════════════════
narr("Here is the reading passage from the lesson itself. Slowly first.",
     pause=800, chapter="Text")
BOOK_TEXT = [
    "Eu sunt Ion. Sunt din Moldova.",
    "Și el este din Moldova, iar ea este din Ucraina.",
    "Tu ești din Chișinău. Noi suntem din Bulgaria.",
    "Voi sunteți din Rusia. Dar ei? Ei sunt din America.",
    "El este Radu, iar ea este Dana.",
    "El este bărbat, ea este femeie. Noi suntem din Moldova.",
]
for line in BOOK_TEXT:
    ro(line, "m", SLOW, 900)
narr("And at normal speed.", pause=600)
for line in BOOK_TEXT:
    ro(line, "m", NORMAL, 300)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
narr("Back to the roll call. Same recording, same speed. Nothing about it has "
     "changed.", pause=P_SECTION, chapter="Cold open again")
play_dialogue()
narr("Every word of that was built from this one lesson. Twenty-four words and "
     "one verb.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
narr("One thing before the next episode. Say your own line out loud — where "
     "you are from, what you are. Start with sunt, and leave the eu off. "
     "Pe curând!", pause=1500, chapter="Close")


# ── emit ─────────────────────────────────────────────────────────────────────
episode = {
    "episode": 1, "lesson": 1,
    "title": "Bună dimineața!",
    "source": "Limba care ne unește, nivelul I — Lecția 1",
    "l1": "en", "l2": "ro", "level": "A1",
    "glue": GLUE,
    "spoken_layer": SPOKEN.get("1", []),
    "voices": {
        "en_narrator": {"provider": "azure", "lang": "en-US",
                        "voice_id": "en-US-AndrewNeural"},
        "ro_male":     {"provider": "azure", "lang": "ro-RO",
                        "voice_id": "ro-RO-EmilNeural", "rate_scale": 0.90},
        "ro_female":   {"provider": "azure", "lang": "ro-RO",
                        "voice_id": "ro-RO-AlinaNeural"},
        # Three characters, two native Romanian voices. Elena borrows Alina at
        # a raised pitch so she does not sound like Dana.
        "ro_dana":     {"provider": "azure", "lang": "ro-RO",
                        "voice_id": "ro-RO-AlinaNeural"},
        "ro_radu":     {"provider": "azure", "lang": "ro-RO",
                        "voice_id": "ro-RO-EmilNeural", "rate_scale": 0.92},
        "ro_elena":    {"provider": "azure", "lang": "ro-RO",
                        "voice_id": "ro-RO-AlinaNeural", "pitch": "+12%"},
    },
    "segments": seg,
}

OUT.mkdir(exist_ok=True)
script_path = OUT / f"episode_{episode['episode']:02d}.json"
with open(script_path, "w", encoding="utf-8") as f:
    json.dump(episode, f, ensure_ascii=False, indent=1)


# ── checks the skill asks for ────────────────────────────────────────────────
def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn")


ro_text = fold(" ".join(s["text"] for s in seg if s["lang"] == "ro"))
missing = [w for w in REQUIRED if fold(w) not in ro_text]

chars = {"ro": 0, "en": 0}
for s in seg:
    chars[s["lang"]] += len(s["text"])
silence = sum(s["pause_after_ms"] for s in seg) / 1000
speech = sum(len(s["text"].split()) for s in seg) / 2.3
runtime = speech + silence

print(f"wrote           : {script_path}")
print(f"segments        : {len(seg)}")
print(f"coverage        : {len(REQUIRED) - len(missing)}/{len(REQUIRED)}"
      + (f"  MISSING: {missing}" if missing else "  ✓"))
print(f"glue items      : {len(GLUE)} ({', '.join(GLUE)})")
print(f"L1 share        : {100 * chars['en'] / sum(chars.values()):.0f}%")
print(f"silence         : {100 * silence / runtime:.0f}% of runtime")
print(f"estimated run   : {runtime / 60:.1f} min")
print(f"characters      : {sum(chars.values())} (all Azure)")
if missing:
    raise SystemExit("coverage check failed")
