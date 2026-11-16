"""
Episode 11G — "Cad de oboseală" (Lecția 11 "La munte", memory-first, part 7)

Six items: plimbare, cad, oboseală, tac, somn, adânc — the evening of the
book's text: "După o plimbare lungă ei cad de oboseală. La aer curat somnul
este adânc." Cad de oboseală (I'm dead tired, literally I fall from
tiredness) is taught as one chunk.

Fall changes its sound like see (11A): cad, cazi, cade, cad. One form at a
time, each used at once, then out of order. Keep quiet (tac, tace, tac) goes
the same way; its friend-form taci waits for "De ce taci?" in 11H.

Two old words come back as words: podea and tavan. They only ever lived in
4A's nine-word "Aceasta e o podea, iar acesta e un tavan.", missed six times,
and the learner's note says why: "after 6 times it's obvious I don't
remember floor and ceiling". relearn() teaches each as a word (falling on the
floor fits cad), then the halves, then the old sentence — outside the new-item
cap, and back on the spacing schedule from here.

Agreement again with the chapter's words: o plimbare lungă, plimbarea e lungă;
somn adânc against apă adâncă, like 11F's aer curat, apă curată.

11F's spoken layer (Uite! / Ce frumos!) comes back as ordinary speech.

Scene: parents back at the hotel after a long walk — everyone is dead tired,
and the children are suspiciously quiet, so fall and keep quiet come round
for each person.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["plimbare", "cad", "oboseală", "tac", "somn", "adânc"]
GLUE = {"Ce plimbare lungă!": "What a long walk! — a chunk, like Ce frumos!"}

ep = Episode(number=11, lesson=11, part="g", title="Cad de oboseală",
             source="Limba care ne unește, nivelul I — Lecția 11 (partea G)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Ce plimbare lungă! Cad de oboseală."),
    ("radu", "Și eu cad de oboseală."),
    ("dana", "Și copiii? Uite, copiii tac!"),
    ("radu", "Tac? Cad de oboseală!"),
    ("dana", "Da. La aer curat somnul e adânc."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Two parents back at the hotel after a long walk. Everyone is worn "
        "out — and the children are very quiet.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("plimbare", "a walk", "o plimbare", "f",
            teach_ro="O plimbare lungă.", teach_en="A long walk.")
ep.new_item("cad", "I fall", "cad", "m",
            teach_ro="Nu cad.", teach_en="I don't fall.")
ep.new_item("oboseală", "tiredness", "oboseală", "f",
            teach_ro="Cad de oboseală.",
            teach_en="I'm dead tired — I fall from tiredness.")
ep.drill("I'm dead tired.", "Cad de oboseală.", "m")
ep.new_item("tac", "I keep quiet, I say nothing", "tac", "f",
            teach_ro="Eu tac.", teach_en="I keep quiet.")
ep.new_item("somn", "sleep", "somn", "m",
            teach_ro="Un somn lung.", teach_en="A long sleep.")
ep.new_item("adânc", "deep — of sleep, of water", "adânc", "f",
            teach_ro="Somnul e adânc.", teach_en="Sleep is deep.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("sleep", "somn", "m"), ("I fall", "cad", "f"), ("a walk", "o plimbare", "m"),
                    ("deep", "adânc", "f"), ("tiredness", "oboseală", "m"),
                    ("I keep quiet", "tac", "f"), ("I'm dead tired.", "Cad de oboseală.", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Fall — one form at a time ════════════════════════════════════════════
ep.narr("Fall changes its sound, like see. One form at a time. It falls — the "
        "suitcase, from a hand. Listen:", pause=800, chapter="Fall, one form at a time")
ep.ro("Valiza cade.", "f", SLOW, 1800)
ep.drill("it falls", "cade", "m")
ep.drill("The suitcase falls from my hand.", "Valiza cade din mână.", "f")

ep.narr("To a friend — are you dead tired? Listen:", pause=800)
ep.ro("Cazi de oboseală?", "m", SLOW, 1800)
ep.drill("you fall — to a friend", "cazi", "f")
ep.drill("Are you dead tired? To a friend.", "Cazi de oboseală?", "m")

ep.narr("And they sounds like I, as with see. Listen:", pause=800)
ep.ro("Copiii cad de oboseală.", "f", SLOW, 1800)
ep.drill("they fall", "ei cad", "m")
ep.drill("The tourists are dead tired.", "Turiștii cad de oboseală.", "f")

ep.narr("Mixed, and not in order.", pause=800)
for cue, ans, v in [("you fall — to a friend", "cazi", "m"), ("it falls", "cade", "f"),
                    ("I fall", "cad", "m"), ("they fall", "ei cad", "f"),
                    ("she falls", "cade", "m")]:
    ep.drill(cue, ans, v)

# ═══ 3. Keep quiet ═══════════════════════════════════════════════════════════
ep.narr("Keep quiet goes the same way. The child keeps quiet. Listen:", pause=800,
        chapter="Keep quiet")
ep.ro("Copilul tace.", "m", SLOW, 1800)
ep.drill("he keeps quiet", "tace", "f")
ep.narr("They — like I. Build it.", pause=P_SHORT)
ep.drill("they keep quiet", "ei tac", "m")
ep.drill("The children are quiet.", "Copiii tac.", "f")
for cue, ans, v in [("I keep quiet", "tac", "m"), ("she keeps quiet", "tace", "f"),
                    ("they keep quiet", "ei tac", "m")]:
    ep.drill(cue, ans, v)

# ═══ 4. Two old words, as words ══════════════════════════════════════════════
ep.narr("Two old words that keep slipping: floor and ceiling. You met them "
        "once, inside one long sentence. Here they are on their own.",
        pause=800, chapter="Floor and ceiling")
ep.relearn("podea", "a floor", "o podea", "f",
           teach_ro="Valiza cade pe podea.", teach_en="The suitcase falls on the floor.")
ep.relearn("tavan", "a ceiling", "un tavan", "m",
           teach_ro="Un tavan înalt.", teach_en="A high ceiling.")
for cue, ans, v in [("a ceiling", "un tavan", "f"), ("a floor", "o podea", "m"),
                    ("The suitcase falls on the floor.", "Valiza cade pe podea.", "f"),
                    ("The ceiling is high.", "Tavanul e înalt.", "m"),
                    ("This is a floor.", "Aceasta e o podea.", "f"),
                    ("This is a ceiling.", "Acesta e un tavan.", "m")]:
    ep.drill(cue, ans, v)
ep.narr("Now both halves together — the old sentence.", pause=P_SHORT)
ep.drill("This is a floor, and this is a ceiling.",
         "Aceasta e o podea, iar acesta e un tavan.", "f",
         accept=["Aceasta e o podea și acesta e un tavan."])

# ═══ 5. A long walk, a deep sleep ════════════════════════════════════════════
ep.narr("Walk is a her-word, so long follows it. Listen:", pause=800,
        chapter="A long walk, a deep sleep")
ep.ro("o plimbare lungă", "f", SLOW, 1800)
ep.drill("a long walk", "o plimbare lungă", "m")
ep.narr("The walk just gains a sound, like the resort. Listen:", pause=P_SHORT)
ep.ro("stațiunea — plimbarea", "f", SLOW, 1800)
ep.drill("The walk is long.", "Plimbarea e lungă.", "m")
ep.narr("Deep goes like clean: sleep is a his-word, water a her-word. Listen:",
        pause=800)
ep.ro("Aer curat. Apă adâncă.", "m", SLOW, 2000)
for cue, ans, v in [("deep water", "apă adâncă", "f"), ("a deep sleep", "un somn adânc", "m"),
                    ("The water is deep.", "Apa e adâncă.", "f"),
                    ("Sleep is deep.", "Somnul e adânc.", "m")]:
    ep.drill(cue, ans, v)

# ═══ 6. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("What a long walk!", "Ce plimbare lungă!", "m", {}),
    ("I'm dead tired.", "Cad de oboseală.", "f", {}),
    ("Are you dead tired? To a friend.", "Cazi de oboseală?", "m", {}),
    ("Look, the children are quiet!", "Uite, copiii tac!", "f", {}),
    ("The child keeps quiet.", "Copilul tace.", "m", {}),
    ("We're going for a walk.", "Plecăm la plimbare.", "f", {}),
    ("The tourists go for a walk.", "Turiștii pleacă la plimbare.", "m", {}),
    ("In fresh air, sleep is deep.", "La aer curat somnul e adânc.", "f",
     {"accept": ["Somnul e adânc la aer curat."]}),
    ("The suitcase falls on the floor.", "Valiza cade pe podea.", "m", {}),
    ("How lovely!", "Ce frumos!", "f", {}),
    ("The walk is long.", "Plimbarea e lungă.", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 7. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Dead tired is the book's way, and people do say "
        "it. But most of the time they just say I'm tired. A man — listen:",
        pause=800, chapter="How people really say it")
ep.ro("Sunt obosit.", "m", SLOW, 1500)
ep.narr("A woman:", pause=P_SHORT)
ep.ro("Sunt obosită.", "f", SLOW, 1500)
ep.narr("And late at night, among family — I'm dying for sleep. Listen:",
        pause=P_SHORT)
ep.ro("Mor de somn.", "f", SLOW, 1500)
ep.narr("Just to recognise for now.", pause=P_SECTION)

# ═══ 8. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 9. Cold open again ══════════════════════════════════════════════════════
ep.narr("The parents again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 10. Close ═══════════════════════════════════════════════════════════════
ep.narr("A long walk, a deep sleep — and the floor and the ceiling, as words "
        "this time.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("11", []))
