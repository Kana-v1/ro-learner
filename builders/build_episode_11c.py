"""
Episode 11C — "Pot rezerva o cameră?" (Lecția 11 "La munte", memory-first, part 3)

Six items: agenție, călătorie, rezerv, pat, loc, pot. (Cameră is known from
04A.) The chapter's second grammar point, "a putea + infinitiv": pot, poți,
poate, putem, puteți, pot — each form on its own in the 11A way — and the
verb after it, taught by ear from verbs the learner already has: lucrez →
pot lucra, semnez → pot semna (the extra piece drops), rezerv → pot rezerva,
ascult → pot asculta. See does its own thing (pot vedea), said plainly.

Plurals in -uri, as the book's dialogue has them ("o cameră cu 3 paturi",
"locuri la hotel"): paturi, locuri — and două before them, as with two kilos
in 10D.

The spoken layer is the big one for this point: in speech "pot să" + the
I-form the learner already knows (pot să rezerv) is far more common than the
book's "pot rezerva". 11B's spoken layer (Poftă bună!, Bem o cafea?) comes
back as ordinary drills.

Scene: phoning a travel agency to book a room and seats — booking is the
agent's job, so can and book come round for every request.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["agenție", "călătorie", "rezerv", "pat", "loc", "pot"]
GLUE = {"de turism": "travel — in 'agenția de turism'",
        "Călătorie plăcută!": "Have a good trip! — a chunk"}

ep = Episode(number=11, lesson=11, part="c", title="Pot rezerva o cameră?",
             source="Limba care ne unește, nivelul I — Lecția 11 (partea C)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Agenția de turism, bună ziua!"),
    ("radu", "Bună ziua! Pot rezerva o cameră?"),
    ("dana", "Da. Cu câte paturi?"),
    ("radu", "Cu trei paturi. Și trei locuri în tren."),
    ("dana", "Bine. Călătorie plăcută!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A phone call to a travel agency: a room, beds, seats on the train. "
        "Today: can, and booking.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("agenție", "an agency", "o agenție", "f",
            teach_ro="Agenția de turism.", teach_en="The travel agency.")
ep.new_item("călătorie", "a trip, a journey", "o călătorie", "m",
            teach_ro="O călătorie lungă.", teach_en="A long journey.")
ep.new_item("rezerv", "I book, I reserve", "rezerv", "f",
            teach_ro="Rezerv o cameră.", teach_en="I book a room.")
ep.new_item("pat", "a bed", "un pat", "m",
            teach_ro="Un pat mare.", teach_en="A big bed.")
ep.new_item("loc", "a place — or a seat", "un loc", "f",
            teach_ro="Un loc în tren.", teach_en="A seat on the train.")
ep.new_item("pot", "I can", "pot", "m",
            teach_ro="Pot rezerva?", teach_en="Can I book?")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("a bed", "un pat", "f"), ("I can", "pot", "m"), ("an agency", "o agenție", "f"),
                    ("a seat", "un loc", "m"), ("I book", "rezerv", "f"),
                    ("a journey", "o călătorie", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Beds and seats ═══════════════════════════════════════════════════════
ep.narr("More than one bed. Listen:", pause=800, chapter="Beds and seats")
ep.ro("un pat, două paturi", "m", SLOW, 1800)
ep.narr("Seat goes the same way, and two is the her-form here — as with two "
        "kilos. Build them.", pause=P_SHORT)
for cue, ans, v in [("two seats", "două locuri", "f"), ("three beds", "trei paturi", "m"),
                    ("a seat", "un loc", "f"), ("four seats", "patru locuri", "m"),
                    ("two beds", "două paturi", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Can — and the verb after it ══════════════════════════════════════════
ep.narr("After can, the next verb changes. Listen — I work, then I can work:",
        pause=800, chapter="Can, and the verb after it")
ep.ro("Lucrez. Pot lucra.", "f", SLOW, 2000)
ep.narr("The extra piece drops. Sign and fill in go the same way. Build them.",
        pause=P_SHORT)
ep.drill("I can sign", "pot semna", "m")
ep.drill("I can fill in", "pot completa", "f")
ep.narr("Book has no extra piece; it only gains a sound at the end. Listen:", pause=800)
ep.ro("Rezerv. Pot rezerva.", "m", SLOW, 2000)
ep.drill("I can listen", "pot asculta", "f")
ep.drill("I can book", "pot rezerva", "m")
ep.narr("See does its own thing — you can't work it out, just hear it. Listen:",
        pause=800)
ep.ro("Pot vedea muntele.", "f", SLOW, 1800)
ep.drill("I can see the peak.", "Pot vedea vârful.", "m")

# ═══ 4. Can — one form at a time ═════════════════════════════════════════════
ep.narr("Can changes its sound too. One form at a time. To a friend: can you? "
        "Listen:", pause=800, chapter="Can, one form at a time")
ep.ro("Poți semna aici?", "m", SLOW, 1800)
ep.drill("you can — to a friend", "poți", "f")
ep.drill("Can you work at home? To a friend.", "Poți lucra acasă?", "m")

ep.narr("She can, he can. Listen:", pause=800)
ep.ro("Ea poate rezerva.", "f", SLOW, 1800)
ep.drill("she can", "poate", "m")
ep.drill("He can sign.", "Poate semna.", "f")

ep.narr("Politely, or to a group. Listen:", pause=800)
ep.ro("Puteți rezerva o cameră?", "m", SLOW, 2000)
ep.drill("you can — politely", "puteți", "f")
ep.drill("Can you sign here? Politely.", "Puteți semna aici?", "m")

ep.narr("We can. Listen:", pause=800)
ep.ro("Putem asculta.", "f", SLOW, 1600)
ep.drill("we can", "putem", "m")

ep.narr("And they sounds like I. Listen:", pause=800)
ep.ro("Ei pot lucra.", "m", SLOW, 1600)
ep.drill("they can", "ei pot", "f")

ep.narr("Now mixed, and not in order.", pause=800)
for cue, ans, v in [("she can", "poate", "m"), ("we can", "putem", "f"), ("I can", "pot", "m"),
                    ("you can — politely", "puteți", "f"), ("they can", "ei pot", "m"),
                    ("you can — to a friend", "poți", "f")]:
    ep.drill(cue, ans, v)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("Can I book a room?", "Pot rezerva o cameră?", "m", {}),
    ("A room with two beds.", "O cameră cu două paturi.", "f", {}),
    ("Three seats on the train.", "Trei locuri în tren.", "m", {}),
    ("I can't book today.", "Azi nu pot rezerva.", "f", {"accept": ["Nu pot rezerva azi."]}),
    ("Mum books two seats.", "Mama rezervă două locuri.", "m", {}),
    ("The agency is near.", "Agenția e aproape.", "f", {}),
    ("A long journey.", "O călătorie lungă.", "m", {}),
    ("She can work at home.", "Ea poate lucra acasă.", "f", {}),
    ("We can listen.", "Putem asculta.", "m", {}),
    ("I can't see the sun.", "Nu pot vedea soarele.", "f", {}),
    ("Shall we have a coffee?", "Bem o cafea?", "m", {}),
    ("Enjoy your meal!", "Poftă bună!", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 6. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. In speech, people more often put a small word "
        "after can — and then the I-form you already know. Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Pot să rezerv o cameră?", "f", SLOW, 1800)
ep.narr("Both are right; you'll hear this one more. And seeing someone off on "
        "a trip — listen:", pause=P_SHORT)
ep.ro("Călătorie plăcută!", "m", SLOW, 1600)
ep.narr("Have a good trip!", pause=P_SECTION)

# ═══ 7. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The phone call again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("Can, book, beds and seats.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("11", []))
