"""
Episode 09A — "Prima zi la serviciu" (Lecția 9 "O zi la serviciu", memory-first, part 1)

Lecția 9's grammar is the -ez verbs ("Prezentul indicativ al verbelor de
conjugarea I cu sufix"): lucrez, lucrezi, lucrează, lucrăm, lucrați,
lucrează. Six items — lucrez, completez, semnez (three -ez verbs from the
chapter list), formular, serviciu, zi.

This is also the model for explaining a rule by ear, rewritten after the
learner called 08D's rules section "rather bad" (too long and abstract,
unclear, and the narrator trying to say endings). Here the Romanian voice
says every form, always as a whole word; the pattern is heard first and named
in one short sentence; each point is followed at once by the learner building
an unheard form; and what can't be worked out is said plainly — you can't
tell an -ez verb from its look, so each verb is learnt by its I-form.

Also two confusions the results keep showing: larg for lung (7 misses), and
multe for mult after a verb.

Scene: a new employee's first day — the secretary hands over forms to fill
in and sign, so fill in and sign come round again and again.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["lucrez", "completez", "semnez", "formular", "serviciu", "zi"]
GLUE = {"prima": "first — in 'prima mea zi'"}

ep = Episode(number=9, lesson=9, part="a", title="Prima zi la serviciu",
             source="Limba care ne unește, nivelul I — Lecția 9 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Bună ziua! Lucrați aici de azi?"),
    ("radu", "Da, e prima mea zi."),
    ("dana", "Completați formularul, vă rog."),
    ("radu", "Și semnez aici?"),
    ("dana", "Da, semnați aici. Și aici. Și aici."),
    ("radu", "Ce zi lungă!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A first day at work, and a lot of forms. Lesson 9: work.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("lucrez", "I work", "lucrez", "m",
            teach_ro="Lucrez la birou.", teach_en="I work at the office.")
ep.new_item("serviciu", "work — the job, the place", "serviciu", "f",
            teach_ro="Sunt la serviciu.", teach_en="I'm at work.")
ep.new_item("zi", "a day", "o zi", "m",
            teach_ro="O zi lungă.", teach_en="A long day.")
ep.new_item("formular", "a form — to fill in", "un formular", "f",
            teach_ro="un formular, două formulare", teach_en="one form, two forms")
ep.new_item("completez", "I fill in", "completez", "m",
            teach_ro="Completez formularul.", teach_en="I fill in the form.")
ep.new_item("semnez", "I sign", "semnez", "f",
            teach_ro="Semnez aici.", teach_en="I sign here.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I sign", "semnez", "m"), ("a day", "o zi", "f"), ("I work", "lucrez", "m"),
                    ("a form", "un formular", "f"), ("I fill in", "completez", "m"),
                    ("work, the place", "serviciu", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Two kinds of verb ════════════════════════════════════════════════════
ep.narr("Listen to I, you and she — work:", pause=800, chapter="Two kinds of verb")
ep.ro("lucrez, lucrezi, lucrează", "m", SLOW, 1800)
ep.narr("And the same three for listen, from last lesson:", pause=P_SHORT)
ep.ro("ascult, asculți, ascultă", "m", SLOW, 1800)
ep.narr("Work has an extra piece before its ending; listen has none. You can't "
        "tell from a verb which kind it is — so each one is learnt by its I-form.",
        pause=800)
ep.narr("Sign and fill in are like work. You build them.", pause=P_SHORT)
for cue, ans, v in [("you work — to a friend", "lucrezi", "f"), ("she works", "lucrează", "m"),
                    ("you sign — to a friend", "semnezi", "f"), ("he fills in", "completează", "m")]:
    ep.drill(cue, ans, v)

ep.narr("For we and you all, the extra piece drops. Both kinds end alike. Listen:",
        pause=800)
ep.ro("lucrăm, lucrați — ascultăm, ascultați", "f", SLOW, 2200)
for cue, ans, v in [("we work", "lucrăm", "m"), ("you all sign", "semnați", "f"),
                    ("we fill in", "completăm", "m")]:
    ep.drill(cue, ans, v)

ep.narr("And they sounds like she, as always. Listen:", pause=P_SHORT)
ep.ro("ea lucrează, ei lucrează", "m", SLOW, 1800)
for cue, ans, v in [("they sign", "ei semnează", "f"), ("they work", "ei lucrează", "m")]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I work at the office.", "Lucrez la birou.", "m", {}),
    ("Where do you work? To a friend.", "Unde lucrezi?", "f", {}),
    ("My wife works at a school.", "Soția mea lucrează la o școală.", "m", {}),
    ("Please fill in the form. Politely.", "Completați formularul, vă rog.", "f", {}),
    ("Do I sign here?", "Semnez aici?", "m", {}),
    ("Yes, sign here. Politely.", "Da, semnați aici.", "f", {}),
    ("We work a lot.", "Lucrăm mult.", "m", {}),
    ("Today I'm at work.", "Azi sunt la serviciu.", "f", {"accept": ["Sunt la serviciu azi."]}),
    ("What a long day!", "Ce zi lungă!", "m", {}),
    ("They fill in the forms.", "Ei completează formularele.", "f", {}),
    ("Do you all work here?", "Voi lucrați aici?", "m", {}),
    ("My brother is at work.", "Fratele meu e la serviciu.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Two you mix up ═══════════════════════════════════════════════════════
ep.narr("Two pairs your results keep mixing. Long and loose:", pause=800,
        chapter="Two you mix up")
ep.ro("lung, larg", "m", SLOW, 1600)
ep.narr("And a lot after a verb, against many before a word:", pause=P_SHORT)
ep.ro("Învață mult. Multe zile.", "f", SLOW, 1800)
for cue, ans, v in [("long", "lung", "m"), ("loose", "larg", "f"), ("a long day", "o zi lungă", "m"),
                    ("loose trousers", "pantaloni largi", "f"), ("She studies a lot.", "Ea învață mult.", "m"),
                    ("many days", "multe zile", "f")]:
    ep.drill(cue, ans, v)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. On someone's first day, people say welcome. "
        "Listen:", pause=800, chapter="How people really say it")
ep.ro("Bine ați venit!", "f", SLOW, 1600)
ep.narr("And for at work, many people in Bucharest just say this — listen:",
        pause=P_SHORT)
ep.ro("Sunt la muncă. Sunt la job.", "m", SLOW, 1800)
ep.narr("The second borrows the English word. You'll hear all three.", pause=P_SECTION)

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The first day again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("Work, sign, fill in — and the verbs with the extra piece.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("9", []))
