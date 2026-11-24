"""
Episode 12D — "Aduc cartea înapoi" (Lecția 12 "La teatru", memory-first, part 4)

Six items: spun, scriu, aduc, duc, înapoi, înainte. The chapter's own pairs:
"Înțelegi ce spune profesorul?", "Cine aduce apă?", "Când duci băiatul la
școală?", "El cere cartea înapoi?", and exercise 4's antonyms (înainte /
înapoi). Scrie gets the book's own table (scriu, scrii, scrie).

Bring and take are one sound apart (aduc / duc) and go exactly like go, so
the learner builds their forms; the narrator gives the difference once —
bring comes here, take goes there — and the two are heard side by side, the
limit. Say drops a sound to a friend like stay from 12B (spun → spui): heard
first. Write to a friend has a doubled ending (scrii): heard first.

12C's spoken layer (Poftim?, Puteți repeta, vă rog?) is ordinary speech in
the dialogue; 12C's ask-for comes back in "Cere cartea înapoi".

Scene: a library desk. Elena brings a book back and takes a new one home;
Dana writes her name down and doesn't catch it — so bring, take, write and
say come round naturally.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["spun", "scriu", "aduc", "duc", "înapoi", "înainte"]
GLUE = {"Popa": "a surname"}

ep = Episode(number=12, lesson=12, part="d", title="Aduc cartea înapoi",
             source="Limba care ne unește, nivelul I — Lecția 12 (partea D)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("elena", "Bună ziua! Aduc cartea înapoi."),
    ("dana", "Mulțumesc. Scriu numele dumneavoastră."),
    ("elena", "Elena Popa."),
    ("dana", "Poftim? Puteți repeta, vă rog?"),
    ("elena", "Elena Popa. Și duc acasă o carte nouă."),
    ("dana", "Ce spuneți? O carte nouă?"),
    ("elena", "Aceasta. Fiecare spune că e interesantă."),
    ("dana", "Bine. La revedere!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A library desk: one book comes back, another goes home.",
        pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("aduc", "I bring", "aduc", "m",
            teach_ro="Aduc apă.", teach_en="I'm bringing water.")
ep.new_item("înapoi", "back — returning", "înapoi", "f",
            teach_ro="Aduc cartea înapoi.", teach_en="I'm bringing the book back.")
ep.new_item("scriu", "I write", "scriu", "m",
            teach_ro="Scriu în caiet.", teach_en="I write in the notebook.")
ep.new_item("duc", "I take — somewhere", "duc", "f",
            teach_ro="Duc copiii la școală.", teach_en="I take the children to school.")
ep.new_item("spun", "I say", "spun", "m",
            teach_ro="Spun bună ziua.", teach_en="I say hello.")
ep.new_item("înainte", "forward, straight on", "înainte", "f",
            teach_ro="Merg înainte.", teach_en="I go straight on.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I write", "scriu", "f"), ("back — returning", "înapoi", "m"),
                    ("I say", "spun", "f"), ("I bring", "aduc", "m"),
                    ("straight on", "înainte", "f"), ("I take — somewhere", "duc", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Bring and take ═══════════════════════════════════════════════════════
ep.narr("Bring comes here; take goes there. One sound apart — listen to both:",
        pause=800, chapter="Bring and take")
ep.ro("Aduc. Duc.", "m", SLOW, 1900)
ep.narr("Both go like go. You haven't heard these — build them.", pause=P_SHORT)
ep.drill("you bring — to a friend", "aduci", "f")
ep.drill("Who brings water?", "Cine aduce apă?", "m")
ep.drill("you take — to a friend", "duci", "f")
ep.drill("When do you take the boy to school? To a friend.",
         "Când duci băiatul la școală?", "m")
ep.drill("she takes", "duce", "f")
for cue, ans, v in [("I take", "duc", "m"), ("I bring", "aduc", "f"),
                    ("he brings", "aduce", "m"), ("you take — to a friend", "duci", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Say — a sound drops ══════════════════════════════════════════════════
ep.narr("Say goes like stay: to a friend, a sound drops off. Listen:", pause=800,
        chapter="Say, by ear")
ep.ro("Ce spui?", "f", SLOW, 1700)
ep.drill("you say — to a friend", "spui", "m")
ep.drill("I don't understand what you're saying. To a friend.",
         "Nu înțeleg ce spui.", "f")
ep.narr("She says is plain. Build it.", pause=P_SHORT)
ep.drill("he says", "spune", "m")
ep.drill("What is the teacher saying?", "Ce spune profesorul?", "f")
for cue, ans, v in [("I say", "spun", "m"), ("you say — to a friend", "spui", "f"),
                    ("she says", "spune", "m")]:
    ep.drill(cue, ans, v)

# ═══ 4. Write ════════════════════════════════════════════════════════════════
ep.narr("Write, to a friend, ends in a long sound. Listen:", pause=800,
        chapter="Write")
ep.ro("Ce scrii?", "m", SLOW, 1700)
ep.drill("you write — to a friend", "scrii", "f")
ep.drill("she writes", "scrie", "m")
ep.drill("The pupil writes on the board.", "Elevul scrie la tablă.", "f")
ep.drill("you write — politely", "scrieți", "m")

# ═══ 5. Back, straight on ════════════════════════════════════════════════════
ep.narr("Back and straight on are opposites. Listen to both:", pause=800,
        chapter="Back, straight on")
ep.ro("Merg înainte. Merg înapoi.", "f", SLOW, 2200)
ep.drill("Go straight on! Politely.", "Mergeți înainte!", "m")
ep.drill("I'm bringing the book back.", "Aduc cartea înapoi.", "f")
ep.drill("He's asking for the book back.", "Cere cartea înapoi.", "m")

# ═══ 6. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I'm bringing the book back.", "Aduc cartea înapoi.", "f", {}),
    ("I'm writing your name. Politely.", "Scriu numele dumneavoastră.", "m", {}),
    ("Pardon? Can you repeat, please?", "Poftim? Puteți repeta, vă rog?", "f", {}),
    ("I'm taking a new book home.", "Duc acasă o carte nouă.", "m",
     {"accept": ["Duc o carte nouă acasă."]}),
    ("What do you say? Politely.", "Ce spuneți?", "f", {}),
    ("Everyone says it's interesting.", "Fiecare spune că e interesantă.", "m", {}),
    ("What are you writing? To a friend.", "Ce scrii?", "f", {}),
    ("I take the children to school.", "Duc copiii la școală.", "m", {}),
    ("I don't understand what you're saying. To a friend.", "Nu înțeleg ce spui.", "f", {}),
    ("Who's answering the phone?", "Cine răspunde la telefon?", "m", {}),
    ("Go straight on! Politely.", "Mergeți înainte!", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 7. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Between friends, what do you say — what do you "
        "think? — is usually another word. Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Ce zici?", "f", SLOW, 1400)
ep.narr("And when someone promises to message you later: I'll write to you. "
        "Listen:", pause=P_SHORT)
ep.ro("Îți scriu.", "m", SLOW, 1500)
ep.narr("Just to recognise for now.", pause=P_SECTION)

# ═══ 8. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 9. Cold open again ══════════════════════════════════════════════════════
ep.narr("The library again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 10. Close ═══════════════════════════════════════════════════════════════
ep.narr("Bring it back, take one home — and say it again, please.",
        pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("12", []))
