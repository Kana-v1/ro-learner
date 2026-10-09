"""
Episode 08A — "Învăț limba română" (Lecția 8 "La studii", memory-first, part 1)

The course's first regular verbs. Lecția 8's grammar is the present tense of
the first conjugation ("Prezentul indicativ al verbelor de conjugarea I fără
sufix"); its table is eu ascult / tu asculți / el ascultă, eu învăț / tu
înveți / el învață, eu repet / tu repeți / el repetă. This part takes three of
those verbs in the three singular persons — I, you, he/she — and three small
words the chapter uses with them: azi (today), mult (a lot), puțin (a little).
The plural persons come in 08B.

Each verb is first learnt as its I-form (învăț, like vreau in 07A): the form
a learner says most and the one a cue can ask for unambiguously.

Scene: an evening Romanian class — the learner's own situation. The teacher
goes round asking each student what they're learning and how, so "înveți?",
"asculți?", "repeți?" come up for every student in turn.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["învăț", "ascult", "repet", "azi", "mult", "puțin"]
GLUE = {"limba română": "Romanian, the language — a chunk",
        "muzică": "music — in 'ascult muzică'"}

ep = Episode(number=8, lesson=8, part="a", title="Învăț limba română",
             source="Limba care ne unește, nivelul I — Lecția 8 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Radu, ce înveți?"),
    ("radu", "Învăț limba română."),
    ("dana", "Și cum înveți?"),
    ("radu", "Ascult mult și repet."),
    ("dana", "Bine. Și Elena?"),
    ("radu", "Elena învață puțin. Ascultă muzică."),
    ("dana", "Azi repetăm lecția!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("An evening Romanian class — your own situation. Lesson 8 starts the "
        "verbs: doing things. Three verbs, and three small words.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The verbs first, the way you'd say them about yourself.", pause=800,
        chapter="Six words")
ep.new_item("învăț", "I learn, I study", "învăț", "m",
            teach_ro="Învăț limba română.", teach_en="I'm learning Romanian.")
ep.new_item("ascult", "I listen", "ascult", "f",
            teach_ro="Ascult lecția.", teach_en="I listen to the lesson.")
ep.new_item("repet", "I repeat, I go over", "repet", "m",
            teach_ro="Repet lecția acasă.", teach_en="I go over the lesson at home.")
ep.new_item("azi", "today", "azi", "f",
            teach_ro="Azi învăț mult.", teach_en="Today I'm studying a lot.")
ep.new_item("mult", "a lot", "mult", "m",
            teach_ro="Ascult mult.", teach_en="I listen a lot.")
ep.new_item("puțin", "a little", "puțin", "f",
            teach_ro="Repet puțin.", teach_en="I go over it a little.")

ep.narr("The six together, mixed. Just the word.", pause=800)
for cue, ans, v in [("I listen", "ascult", "m"), ("a little", "puțin", "f"), ("I learn", "învăț", "m"),
                    ("today", "azi", "f"), ("I repeat", "repet", "m"), ("a lot", "mult", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. You, he, she ═════════════════════════════════════════════════════════
ep.narr("Now about someone else. For you, the verb ends in an i sound; for he "
        "or she, in the short uh sound you know from the her-words. Listen — I, "
        "you, she:", pause=800, chapter="You, he, she")
ep.example(None, "ascult, asculți, ascultă", "m", 2000)
ep.example(None, "repet, repeți, repetă", "f", 2000)
ep.narr("Learn changes its middle a little. Listen:", pause=P_SHORT)
ep.example(None, "învăț, înveți, învață", "m", 2000)
for cue, ans, v in [
    ("you listen — to a friend", "asculți", "f"), ("she listens", "ascultă", "m"),
    ("you repeat — to a friend", "repeți", "f"), ("he repeats", "repetă", "m"),
    ("you learn — to a friend", "înveți", "f"), ("she learns", "învață", "m"),
]:
    ep.drill(cue, ans, v)
ep.narr("In pairs now — me, then someone else.", pause=800)
for cue, ans, v in [
    ("I listen, you listen. To a friend.", "Eu ascult, tu asculți.", "m"),
    ("I learn, she learns.", "Eu învăț, ea învață.", "f"),
    ("I repeat, he repeats.", "Eu repet, el repetă.", "m"),
    ("You learn a lot. To a friend.", "Tu înveți mult.", "f"),
    ("He doesn't listen.", "El nu ascultă.", "m"),
    ("Do you go over the lesson at home? To a friend.", "Repeți lecția acasă?", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I'm learning Romanian.", "Învăț limba română.", "m", {}),
    ("Are you learning Romanian? To a friend.", "Înveți limba română?", "f", {}),
    ("What are you learning? To a friend.", "Ce înveți?", "m", {}),
    ("I listen a lot and repeat.", "Ascult mult și repet.", "f", {}),
    ("She studies a lot.", "Ea învață mult.", "m", {}),
    ("He listens to music.", "El ascultă muzică.", "f", {}),
    ("Today I'm going over the lesson.", "Azi repet lecția.", "m", {"accept": ["Repet lecția azi."]}),
    ("My son studies at school.", "Fiul meu învață la școală.", "f", {}),
    ("Where do you study? To a friend.", "Unde înveți?", "m", {}),
    ("Do you listen a lot? — No, a little.", "Asculți mult? — Nu, puțin.", "f", {}),
    ("My sister listens to the lesson.", "Sora mea ascultă lecția.", "m", {}),
    ("Today she isn't studying.", "Azi nu învață.", "f", {"accept": ["Ea nu învață azi.", "Azi ea nu învață."]}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The book has two words for today, a long one and "
        "the short one you learnt. Listen to the long one:", pause=800,
        chapter="How people really say it")
ep.ro("astăzi", "f", SLOW, 1400)
ep.narr("Both are everyday; the short one is what you'll hear most in "
        "conversation. Just to recognise.", pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=10)

# ═══ 6. Cold open again ══════════════════════════════════════════════════════
ep.narr("The class again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 7. Close ════════════════════════════════════════════════════════════════
ep.narr("Your first verbs: I, you, she. Next time, we and they.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("8", []))
