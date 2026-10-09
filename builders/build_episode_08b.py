"""
Episode 08B — "Profesorul explică" (Lecția 8 "La studii", memory-first, part 2)

Three more verbs from the chapter's table — întreb, explic, rezolv — with
exercițiu, and the plural persons for every verb so far: noi -ăm, voi -ați,
ei like el ("Noi rezolvăm, voi rezolvați, ei rezolvă"). chimie and biologie
are the chapter's own subjects and nearly free for an English speaker; they
carry the book's dialogue ("Profesorul de chimie întreabă mult? — Nu,
dumnealui întreabă puțin. — Dar profesoara de biologie? — Dumneaei întreabă
mult.").

Also the polite you: it is the voi form, as with aveți and sunteți — which
gives the most useful sentence a learner can have, "Repetați, vă rog."

Scene: two students comparing their teachers — who asks a lot, who explains
well — so the he/she and we/you forms come round naturally.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["întreb", "explic", "rezolv", "exercițiu", "chimie", "biologie"]
GLUE = {"bine": "well — in 'explică bine'"}

ep = Episode(number=8, lesson=8, part="b", title="Profesorul explică",
             source="Limba care ne unește, nivelul I — Lecția 8 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu", "Profesorul de chimie întreabă mult?"),
    ("dana", "Nu, întreabă puțin. Dar explică bine."),
    ("radu", "Și profesoara de biologie?"),
    ("dana", "Ea întreabă mult. Noi rezolvăm exerciții și ea întreabă."),
    ("radu", "Voi rezolvați exerciții la biologie?"),
    ("dana", "Da, mult!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "radu", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Two students comparing their teachers. Three more verbs, and how to "
        "say we, you all and they.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("întreb", "I ask", "întreb", "m",
            teach_ro="Întreb profesorul.", teach_en="I ask the teacher.")
ep.new_item("explic", "I explain", "explic", "f",
            teach_ro="Explic lecția.", teach_en="I explain the lesson.")
ep.new_item("rezolv", "I solve, I do — an exercise", "rezolv", "m",
            teach_ro="Rezolv un exercițiu.", teach_en="I do an exercise.")
ep.new_item("exercițiu", "an exercise", "un exercițiu", "f",
            teach_ro="un exercițiu, două exerciții", teach_en="one exercise, two exercises")
ep.new_item("chimie", "chemistry", "chimie", "m",
            teach_ro="profesorul de chimie", teach_en="the chemistry teacher")
ep.new_item("biologie", "biology", "biologie", "f",
            teach_ro="profesoara de biologie", teach_en="the biology teacher")

ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I explain", "explic", "m"), ("biology", "biologie", "f"), ("I ask", "întreb", "m"),
                    ("an exercise", "un exercițiu", "f"), ("I solve", "rezolv", "m"),
                    ("chemistry", "chimie", "f"), ("I learn", "învăț", "m"), ("I listen", "ascult", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. He, she — and ask ════════════════════════════════════════════════════
ep.narr("He or she, as last time: the uh ending. Ask stretches its middle "
        "vowel. Listen:", pause=800, chapter="He and she")
ep.example(None, "explic, explică; rezolv, rezolvă", "m", 2000)
ep.example(None, "întreb, întreabă", "f", 1800)
for cue, ans, v in [("she explains", "explică", "m"), ("he asks", "întreabă", "f"),
                    ("she solves", "rezolvă", "m"), ("you ask — to a friend", "întrebi", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. We, you all, they ════════════════════════════════════════════════════
ep.narr("Now more than one. We ends in uhm; you all, in ats; they is the "
        "same as he. Listen:", pause=800, chapter="We, you all, they")
ep.example(None, "noi ascultăm, voi ascultați, ei ascultă", "m", 2400)
ep.example(None, "noi învățăm, voi învățați, ei învață", "f", 2400)
ep.example(None, "noi întrebăm, voi întrebați, ei întreabă", "m", 2400)
for cue, ans, v in [
    ("we listen", "noi ascultăm", "f"), ("you all listen", "voi ascultați", "m"),
    ("they listen", "ei ascultă", "f"), ("we learn", "noi învățăm", "m"),
    ("you all learn", "voi învățați", "f"), ("we ask", "noi întrebăm", "m"),
    ("they solve", "ei rezolvă", "f"), ("we repeat", "noi repetăm", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("The teacher explains the lesson.", "Profesorul explică lecția.", "m", {}),
    ("Does the chemistry teacher ask a lot?", "Profesorul de chimie întreabă mult?", "f", {}),
    ("No, he asks a little.", "Nu, întreabă puțin.", "m", {"accept": ["Nu, el întreabă puțin."]}),
    ("We do exercises.", "Noi rezolvăm exerciții.", "f", {}),
    ("Do you all study biology?", "Voi învățați biologie?", "m", {}),
    ("They ask, the teacher explains.", "Ei întreabă, profesorul explică.", "f", {}),
    ("I do an exercise at home.", "Rezolv un exercițiu acasă.", "m", {}),
    ("We go over the lesson.", "Noi repetăm lecția.", "f", {}),
    ("You all listen a lot.", "Voi ascultați mult.", "m", {}),
    ("The biology teacher explains well.", "Profesoara de biologie explică bine.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Polite you, and the sentence to keep ═════════════════════════════════
ep.narr("The polite you uses the you-all form — as with have and are. Which "
        "gives you the most useful sentence in a Romanian conversation. "
        "Listen:", pause=800, chapter="How people really say it")
ep.ro("Repetați, vă rog.", "f", SLOW, 1800)
ep.narr("Could you repeat that, please. And the other one, for when it's too "
        "fast — explain, please:", pause=P_SHORT)
ep.ro("Explicați, vă rog.", "m", SLOW, 1800)
for cue, ans, v in [("Could you repeat that, please? Politely.", "Repetați, vă rog.", "f"),
                    ("Could you explain, please? Politely.", "Explicați, vă rog.", "m")]:
    ep.drill(cue, ans, v)

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=9)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The two students again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("Every person of a verb, and the sentence to keep: repeat that, please.",
        pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("8", []))
