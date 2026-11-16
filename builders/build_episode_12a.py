"""
Episode 12A — "Cu ce mergi acasă?" (Lecția 12 "La teatru", memory-first, part 1)

Lecția 12 is about 36 items, 15 of them verbs, so it runs to six parts:
  12A  going home — merg, cu ce, pe jos, ajung, devreme, târziu
  12B  plans for the evening — fac, încep, rămân, astă seară, spectacol, fiecare
  12C  at the box office — cer, înțeleg, răspund, informație, spectator, interesant
  12D  saying and writing — spun, scriu, aduc, duc, înapoi, înainte
  12E  knowing the city — cunosc, trec, aplaudă, decor, amator, prieten
  12F  that one there, the text — acela/aceea, propunere, lucru, până la, ziua
(12C onward are built after the next results, so they can use them; items may
move between parts.)

The chapter's grammar is the third group of verbs — merg, mergi, merge,
mergem, mergeți, merg. By ear they go like see from 11A: they sounds like
I, and the friend-form softens its last sound (merg → mergi, ajung →
ajungi). One form at a time, as in 11A: heard alone in a short sentence,
recalled bare, used — then the next. Go gets I, friend, she, polite and they;
arrive is then built by the learner from go.

Târziu (late) is set beside întârzii (I'm late, 8C), which the learner still
misses ("întârzie", "Nu întârzii" both in struggles) — two forms side by side.

11H's spoken layer (De ce nu? / Nu știu) comes back as ordinary drills.

Scene: the end of the working day, a colleague asking the others how they get
home and when they arrive — so go and arrive come round for each person.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["merg", "cu ce", "pe jos", "ajung", "devreme", "târziu"]
GLUE = {"cu autobuzul": "by bus — a chunk"}

ep = Episode(number=12, lesson=12, part="a", title="Cu ce mergi acasă?",
             source="Limba care ne unește, nivelul I — Lecția 12 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("elena", "Dana, cu ce mergi acasă?"),
    ("dana", "Merg pe jos. E aproape."),
    ("elena", "Și tu, Radu?"),
    ("radu", "Eu merg cu trenul. Ajung acasă târziu."),
    ("dana", "Iar eu ajung devreme!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The end of the working day: how is everyone getting home? Lesson 12 "
        "goes to the theatre — but first, going places.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("merg", "I go", "merg", "m",
            teach_ro="Merg acasă.", teach_en="I'm going home.")
ep.new_item("pe jos", "on foot", "pe jos", "f",
            teach_ro="Merg pe jos.", teach_en="I walk — I go on foot.")
ep.new_item("cu ce", "by what? — asking how someone travels", "cu ce", "m",
            teach_ro="Cu ce mergi?", teach_en="How are you getting there? By what?")
ep.new_item("ajung", "I arrive, I get there", "ajung", "f",
            teach_ro="Ajung acasă.", teach_en="I get home.")
ep.new_item("devreme", "early", "devreme", "m",
            teach_ro="Ajung devreme.", teach_en="I get there early.")
ep.new_item("târziu", "late", "târziu", "f",
            teach_ro="Ajung târziu.", teach_en="I get there late.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("late", "târziu", "m"), ("I go", "merg", "f"), ("on foot", "pe jos", "m"),
                    ("early", "devreme", "f"), ("I arrive", "ajung", "m"),
                    ("by what?", "cu ce", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Go — one form at a time ══════════════════════════════════════════════
ep.narr("Go works like see: one form at a time. To a friend, the end of the "
        "word softens. Listen:", pause=800, chapter="Go, one form at a time")
ep.ro("Mergi acasă?", "f", SLOW, 1800)
ep.drill("you go — to a friend", "mergi", "m")
ep.drill("How are you getting home? To a friend.", "Cu ce mergi acasă?", "f")

ep.narr("She goes, he goes. Listen:", pause=800)
ep.ro("Ea merge pe jos.", "m", SLOW, 1800)
ep.drill("she goes", "merge", "f")
ep.drill("He goes by train.", "Merge cu trenul.", "m")

ep.narr("Politely — listen:", pause=800)
ep.ro("Cu ce mergeți?", "f", SLOW, 1800)
ep.drill("you go — politely", "mergeți", "m")
ep.drill("How are you getting there? Politely.", "Cu ce mergeți?", "f")

ep.narr("And they sounds like I — as with see. Listen:", pause=800)
ep.ro("Ei merg cu autobuzul.", "m", SLOW, 1800)
ep.drill("they go", "ei merg", "f")
ep.drill("The children go on foot.", "Copiii merg pe jos.", "m")

ep.narr("Mixed, and not in order.", pause=800)
for cue, ans, v in [("she goes", "merge", "f"), ("you go — politely", "mergeți", "m"),
                    ("I go", "merg", "f"), ("you go — to a friend", "mergi", "m"),
                    ("they go", "ei merg", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Arrive goes like go ══════════════════════════════════════════════════
ep.narr("Arrive goes exactly like go. You haven't heard these — build them.",
        pause=800, chapter="Arrive goes like go")
ep.drill("you arrive — to a friend", "ajungi", "f")
ep.drill("she arrives", "ajunge", "m")
ep.drill("they arrive", "ei ajung", "f")
ep.drill("When do you get home? To a friend.", "Când ajungi acasă?", "m")
ep.drill("The train arrives late.", "Trenul ajunge târziu.", "f")
for cue, ans, v in [("I arrive", "ajung", "m"), ("he arrives", "ajunge", "f"),
                    ("you arrive — to a friend", "ajungi", "m")]:
    ep.drill(cue, ans, v)

# ═══ 4. Early, late — and I'm late ═══════════════════════════════════════════
ep.narr("Early and late are opposites. And late sits inside a word you know, "
        "I'm late. Listen to both:", pause=800, chapter="Early, late")
ep.ro("Ajung târziu. Întârzii.", "m", SLOW, 2200)
ep.narr("I get there late — and, I'm late. Say them.", pause=P_SHORT)
for cue, ans, v in [("I'm late.", "Întârzii.", "f"),
                    ("I get there late.", "Ajung târziu.", "m"),
                    ("I'm not late.", "Nu întârzii.", "f"),
                    ("she's late", "întârzie", "m"),
                    ("I get home early.", "Ajung acasă devreme.", "f")]:
    ep.drill(cue, ans, v, accept=["Ajung devreme acasă."] if "early" in cue else None)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I'm going home.", "Merg acasă.", "m", {}),
    ("How are you getting home? To a friend.", "Cu ce mergi acasă?", "f", {}),
    ("I walk. It's close.", "Merg pe jos. E aproape.", "m", {}),
    ("I go by train.", "Merg cu trenul.", "f", {}),
    ("She goes by bus.", "Merge cu autobuzul.", "m", {}),
    ("I get home late.", "Ajung acasă târziu.", "f", {"accept": ["Ajung târziu acasă."]}),
    ("When do you get home? To a friend.", "Când ajungi acasă?", "m", {}),
    ("And I get there early!", "Iar eu ajung devreme!", "f",
     {"accept": ["Și eu ajung devreme!"]}),
    ("Why are you late? To a friend.", "De ce întârzii?", "m", {}),
    ("I don't know.", "Nu știu.", "f", {}),
    ("Shall we go? — Why not?", "Plecăm? — De ce nu?", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 6. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The book is set in a city with trolleybuses. In "
        "Bucharest most people cross town by metro — listen:", pause=800,
        chapter="How people really say it")
ep.ro("Merg cu metroul.", "m", SLOW, 1500)
ep.narr("And the message everyone sends when running to meet someone: I'll be "
        "there in ten minutes. Listen:", pause=P_SHORT)
ep.ro("Ajung în zece minute.", "f", SLOW, 1700)
ep.narr("Just to recognise for now.", pause=P_SECTION)

# ═══ 7. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The office again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("Go and arrive — on foot or by train, early or late.", pause=P_SHORT,
        chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("12", []))
