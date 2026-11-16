"""
Episode 12B — "Ce faci astă seară?" (Lecția 12 "La teatru", memory-first, part 2)

Six items: fac, rămân, încep, astă seară, spectacol, fiecare (as "în fiecare
seară", "în fiecare zi" — the chapter's "Cum indicăm timpul": "Da, sunt acasă
în fiecare seară"). În fiecare dimineață is left out: next to dimineața, which
the learner knows, it would be a near-miss to trip on.

Do and begin go like go from 12A, so the learner builds their forms (faceți,
fac, începe) after hearing one each. Stay can't be worked out: the friend-form
drops a sound (rămân → rămâi) — the narrator says so plainly and it is learnt
by ear; she-form rămâne is then built like merge.

Astă seară (this evening) against seara (in the evening, any evening) — the
learner met seara in 11F. Spoken layer: everyday speech says diseară, and
"Ce faci?" between friends is first of all "how are you?".

12A's spoken layer (Merg cu metroul / Ajung în zece minute) comes back as
ordinary drills.

Scene: Dana has theatre tickets and rings friends one after another — "Ce faci
astă seară?" is what she asks each, so do and stay come round naturally.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["fac", "rămân", "încep", "astă seară", "spectacol", "fiecare"]
GLUE = {"Alo": "hello — answering or making a phone call"}

ep = Episode(number=12, lesson=12, part="b", title="Ce faci astă seară?",
             source="Limba care ne unește, nivelul I — Lecția 12 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Alo, Radu? Ce faci astă seară?"),
    ("radu", "Rămân acasă. De ce?"),
    ("dana", "E un spectacol la teatru. Începe la ora șapte."),
    ("radu", "De ce nu? Merg!"),
    ("dana", "Alo, Elena? Ce faci astă seară?"),
    ("elena", "În fiecare seară rămân acasă."),
    ("dana", "Nu astă seară! Hai la teatru!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Dana has theatre tickets, and rings her friends one after another.",
        pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("fac", "I do, I make", "fac", "m",
            teach_ro="Ce fac acum?", teach_en="What do I do now?")
ep.new_item("astă seară", "this evening, tonight", "astă seară", "f",
            teach_ro="Astă seară sunt acasă.", teach_en="This evening I'm at home.")
ep.new_item("rămân", "I stay", "rămân", "m",
            teach_ro="Rămân acasă.", teach_en="I'm staying home.")
ep.new_item("spectacol", "a show, a performance", "un spectacol", "f",
            teach_ro="Un spectacol la teatru.", teach_en="A show at the theatre.")
ep.new_item("încep", "I begin, I start", "încep", "m",
            teach_ro="Încep devreme.", teach_en="I start early.")
ep.new_item("fiecare", "every evening", "în fiecare seară", "f",
            teach_ro="În fiecare seară.", teach_en="Every evening.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I stay", "rămân", "m"), ("a show", "un spectacol", "f"),
                    ("I do", "fac", "m"), ("every evening", "în fiecare seară", "f"),
                    ("this evening", "astă seară", "m"), ("I begin", "încep", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Do — like go ═════════════════════════════════════════════════════════
ep.narr("Do goes like go: to a friend, the end softens. Listen:", pause=800,
        chapter="Do, like go")
ep.ro("Ce faci astă seară?", "f", SLOW, 1800)
ep.drill("you do — to a friend", "faci", "m")
ep.drill("What are you doing this evening? To a friend.", "Ce faci astă seară?", "f",
         accept=["Ce faci în seara asta?"])
ep.narr("She does. Listen:", pause=800)
ep.ro("Ce face Elena?", "m", SLOW, 1800)
ep.drill("she does", "face", "f")
ep.narr("Polite, and they — you haven't heard them. Build them like go.",
        pause=P_SHORT)
ep.drill("you do — politely", "faceți", "m")
ep.drill("they do", "ei fac", "f")
ep.drill("What are you doing this evening? Politely.", "Ce faceți astă seară?", "m",
         accept=["Ce faceți în seara asta?"])
for cue, ans, v in [("I do", "fac", "f"), ("you do — to a friend", "faci", "m"),
                    ("he does", "face", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Stay — learn it by ear ═══════════════════════════════════════════════
ep.narr("Stay you can't work out. To a friend, a sound drops off the end — "
        "learn it as it is. Listen:", pause=800, chapter="Stay, by ear")
ep.ro("Rămâi acasă?", "m", SLOW, 1800)
ep.drill("you stay — to a friend", "rămâi", "f")
ep.drill("Are you staying home? To a friend.", "Rămâi acasă?", "m")
ep.narr("But she stays goes like she goes. Build it.", pause=P_SHORT)
ep.drill("she stays", "rămâne", "f")
ep.drill("Elena stays home.", "Elena rămâne acasă.", "m")
for cue, ans, v in [("I stay", "rămân", "f"), ("she stays", "rămâne", "m"),
                    ("you stay — to a friend", "rămâi", "f")]:
    ep.drill(cue, ans, v)

# ═══ 4. The show begins ══════════════════════════════════════════════════════
ep.narr("Begin goes like go too. The show — like the coat. Listen:", pause=800,
        chapter="The show begins")
ep.ro("Spectacolul începe la ora șapte.", "f", SLOW, 2200)
ep.drill("it begins", "începe", "m")
ep.drill("the show", "spectacolul", "f")
ep.drill("When does the show begin?", "Când începe spectacolul?", "m")
ep.drill("The show begins at eight.", "Spectacolul începe la ora opt.", "f")

# ═══ 5. This evening, every evening ══════════════════════════════════════════
ep.narr("This evening is one evening. Every evening is all of them. And every "
        "day goes the same way. Listen:", pause=800, chapter="Every evening")
ep.ro("În fiecare zi.", "m", SLOW, 1600)
for cue, ans, v, extra in [
    ("every day", "în fiecare zi", "f", {}),
    ("I'm at home every evening.", "Sunt acasă în fiecare seară.", "m",
     {"accept": ["În fiecare seară sunt acasă."]}),
    ("Every evening I stay home.", "În fiecare seară rămân acasă.", "f",
     {"accept": ["Rămân acasă în fiecare seară."]}),
    ("I go to work every day.", "Merg la serviciu în fiecare zi.", "m",
     {"accept": ["În fiecare zi merg la serviciu."]}),
    ("Not this evening!", "Nu astă seară!", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 6. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("What are you doing this evening? To a friend.", "Ce faci astă seară?", "m",
     {"accept": ["Ce faci în seara asta?"]}),
    ("I'm staying home. Why?", "Rămân acasă. De ce?", "f", {}),
    ("There's a show at the theatre.", "E un spectacol la teatru.", "m", {}),
    ("It begins at seven.", "Începe la ora șapte.", "f", {}),
    ("Come on, to the theatre!", "Hai la teatru!", "m", {}),
    ("What is Elena doing?", "Ce face Elena?", "f", {}),
    ("I start early.", "Încep devreme.", "m", {}),
    ("I go by metro.", "Merg cu metroul.", "f", {}),
    ("I'll be there in ten minutes.", "Ajung în zece minute.", "m", {}),
    ("How are you getting there? To a friend.", "Cu ce mergi?", "f", {}),
    ("Are you staying home? To a friend.", "Rămâi acasă?", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 7. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. This evening, in everyday speech, is one short "
        "word. Listen:", pause=800, chapter="How people really say it")
ep.ro("Ce faci diseară?", "f", SLOW, 1700)
ep.narr("And between friends, what are you doing is first of all just: how "
        "are you? The answer — fine, you? Listen:", pause=P_SHORT)
ep.ro("Ce faci? — Bine, tu?", "m", SLOW, 1800)
ep.narr("Just to recognise for now.", pause=P_SECTION)

# ═══ 8. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 9. Cold open again ══════════════════════════════════════════════════════
ep.narr("Dana on the phone again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 10. Close ═══════════════════════════════════════════════════════════════
ep.narr("This evening, every evening — and a show that begins at seven.",
        pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("12", []))
