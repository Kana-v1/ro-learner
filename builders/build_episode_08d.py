"""
Episode 08D — "Unde stai?" (Lecția 8 "La studii", memory-first, part 4)

Two jobs. First, the rules — asked for in the learner's feedback after 8B
("endings of the verbs will be different for different verbs; the book
doesn't explain it in detail"), and visible in the 8A/8B results: "voi
învați" for voi învățați, "ei întreb" for ei întreabă, reaching for facem and
studiez (verbs from other groups). The book only shows the table for its six
verbs. Here the rule is said outright:

- Romanian verbs fall into groups by the ending of the dictionary form,
  a ...-a, -ea, -e, -i, -î. Each group has its own set of endings.
- The -a group (all of Lecția 8's verbs): drop the -a, add nothing, -i, -ă,
  -ăm, -ați, -ă. They is the same as he.
- Before the -i of you, t becomes ț (asculți, repeți).
- Some verbs also shift their middle vowel — învăț/înveți/învață,
  întreb/întreabă — learnt with the verb, not by rule.
- Many -a verbs add -ez instead (studiez, lucrez): Lecția 9.

Second, six new items: stau (the chapter's a sta, irregular: stau, stai, stă,
stăm, stați, stau), universitate, facultate, examen, sau, cu. a sta is "to
live" in "Unde stai?" — the everyday question; the book's own dialogue is
"Maria stă aproape? — Nu, Maria stă departe."

Scene: two new students meeting on the first day — where do you live, which
faculty, when's the exam.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["stau", "universitate", "facultate", "examen", "sau", "cu"]
GLUE = {"aproape": "near — from the book's 'stă aproape'",
        "un coleg": "a colleague, a classmate"}

ep = Episode(number=8, lesson=8, part="d", title="Unde stai?",
             source="Limba care ne unește, nivelul I — Lecția 8 (partea D)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Bună! Ești student aici?"),
    ("radu", "Da, la universitate. La Facultatea de Chimie."),
    ("dana", "Și eu! Unde stai?"),
    ("radu", "Stau aproape, cu fratele meu."),
    ("dana", "Ai examen azi?"),
    ("radu", "Da, la zece fix. Chimie sau biologie — repet cu un coleg."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Two new students on the first day. This time, the rules behind the "
        "verbs — the part the book leaves out — then six words.", pause=P_SECTION)

# ═══ 1. The rule for verbs ═══════════════════════════════════════════════════
ep.narr("Romanian verbs come in groups, and you can tell the group from the "
        "dictionary form — the to-form. It ends in an a, an e-a, an e, an i, or "
        "an i with a hat. Each group has its own endings. Every verb in this "
        "lesson is in the first group, the a-group. Listen to three of them in "
        "their dictionary form:", pause=800, chapter="The rule")
ep.example(None, "a asculta, a repeta, a explica", "m", 2200)
ep.narr("To use one: take off the final a. That's the stem. Then add the "
        "ending for the person. For I: nothing. Listen:", pause=P_SHORT)
ep.example(None, "eu ascult, eu repet, eu explic", "f", 2200)
ep.narr("For you: an i. For he or she: the short uh. Listen:", pause=P_SHORT)
ep.example(None, "tu asculți, el ascultă", "m", 2000)
ep.narr("For we: uhm. For you all: ats. And they is exactly the same as he. "
        "Listen:", pause=P_SHORT)
ep.example(None, "noi ascultăm, voi ascultați, ei ascultă", "f", 2400)
ep.narr("So six persons, five endings: nothing, i, uh, uhm, ats, uh. Two small "
        "things change the sound. Before the i of you, a t becomes ts. Listen:",
        pause=800)
ep.example(None, "ascult, asculți; repet, repeți", "m", 2200)
ep.narr("And some verbs shift their middle vowel too. That isn't a rule you "
        "can work out — learn it with the verb. Listen:", pause=P_SHORT)
ep.example(None, "învăț, înveți, învață; întreb, întreabă", "f", 2400)
ep.narr("One more thing for later. Many a-group verbs add an extra e-z before "
        "the ending — you used one yourself in the last episode. Listen:",
        pause=P_SHORT)
ep.example(None, "studiez, lucrez", "m", 1800)
ep.narr("I study, I work. That's next lesson. The other groups have endings of "
        "their own, and each comes with its own lesson.", pause=P_SECTION)

# ═══ 2. The rule, used ═══════════════════════════════════════════════════════
ep.narr("Now use the rule. The person and the verb; build the form.", pause=800,
        chapter="Using the rule")
for cue, ans, v in [
    ("you all learn", "voi învățați", "m"), ("they ask", "ei întreabă", "f"),
    ("we explain", "noi explicăm", "m"), ("you repeat — to a friend", "tu repeți", "f"),
    ("they listen", "ei ascultă", "m"), ("you all solve", "voi rezolvați", "f"),
    ("she learns", "ea învață", "m"), ("we ask", "noi întrebăm", "f"),
    ("you listen — to a friend", "tu asculți", "m"), ("he explains", "el explică", "f"),
]:
    ep.drill(cue, ans, v)

ep.narr("And three slips from your last session, side by side. Where, and what:",
        pause=P_SHORT)
ep.example(None, "Unde înveți? Ce înveți?", "m", 1800)
ep.narr("Where do you study, what do you study. And a lot, after a verb, never "
        "changes. Listen:", pause=P_SHORT)
ep.example(None, "Ea învață mult. Ei învață mult.", "f", 1800)
for cue, ans, v in [("Where do you study? To a friend.", "Unde înveți?", "m"),
                    ("What do you study? To a friend.", "Ce înveți?", "f"),
                    ("She studies a lot.", "Ea învață mult.", "m"),
                    ("They study a lot.", "Ei învață mult.", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six new words.", pause=800, chapter="Six words")
ep.new_item("stau", "I live — where I stay", "stau", "m",
            teach_ro="Stau aproape.", teach_en="I live nearby.")
ep.new_item("universitate", "a university", "o universitate", "f",
            teach_ro="Învăț la universitate.", teach_en="I study at the university.")
ep.new_item("facultate", "a faculty — a university department", "o facultate", "m",
            teach_ro="Facultatea de Chimie.", teach_en="The Faculty of Chemistry.")
ep.new_item("examen", "an exam", "un examen", "f",
            teach_ro="Am examen azi.", teach_en="I have an exam today.")
ep.new_item("sau", "or", "sau", "m",
            teach_ro="Chimie sau biologie?", teach_en="Chemistry or biology?")
ep.new_item("cu", "with", "cu", "f",
            teach_ro="Stau cu fratele meu.", teach_en="I live with my brother.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("an exam", "un examen", "m"), ("with", "cu", "f"), ("I live", "stau", "m"),
                    ("a university", "o universitate", "f"), ("or", "sau", "m"),
                    ("a faculty", "o facultate", "f")]:
    ep.recall_word(cue, ans, v)

ep.narr("Live is one of the few a-group verbs that doesn't follow the rule. "
        "Learn its six forms as they are. Listen:", pause=800)
ep.example(None, "eu stau, tu stai, el stă", "m", 2000)
ep.example(None, "noi stăm, voi stați, ei stau", "f", 2000)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("Where do you live? To a friend.", "Unde stai?", "m", {}),
    ("I live nearby, with my brother.", "Stau aproape, cu fratele meu.", "f", {}),
    ("We live with our parents.", "Stăm cu părinții.", "m", {"accept": ["Stăm cu părinții noștri."]}),
    ("Do you all live here?", "Voi stați aici?", "f", {}),
    ("I have an exam today.", "Am examen azi.", "m", {"accept": ["Azi am examen.", "Am un examen azi."]}),
    ("At the university or at school?", "La universitate sau la școală?", "f", {}),
    ("My sister studies at the Faculty of Biology.", "Sora mea învață la Facultatea de Biologie.", "m", {}),
    ("I go over it with a classmate.", "Repet cu un coleg.", "f", {}),
    ("The exam is at ten sharp.", "Examenul e la zece fix.", "m", {}),
    ("The university is old.", "Universitatea e veche.", "f", {}),
    ("Does she live nearby? — No.", "Stă aproape? — Nu.", "m", {"accept": ["Ea stă aproape? — Nu."]}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Where do you live is asked with this verb — "
        "where do you stay — far more often than with the verb for live. And "
        "to someone older, politely. Listen:", pause=800, chapter="How people really say it")
ep.ro("Unde stați?", "f", SLOW, 1600)
ep.drill("Where do you live? Politely.", "Unde stați?", "m")

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The first day again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("The rule for a-group verbs, and where you live.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("8", []))
