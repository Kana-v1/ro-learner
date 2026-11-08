"""
Episode 11A — "Vedeți vârful?" (Lecția 11 "La munte", memory-first, part 1)

Lecția 11 is 46 new items, 14 of them verbs, so it runs to eight parts:
  11A  see — văd, munte, vârf, copac, nor, soare
  11B  drink and eat, fast and slowly — beau, mănânc, apă, lapte, repede, încet
  11C  can, booking a trip — pot, rezerv, loc, pat, agenție, călătorie
  11D  leaving by coach — plec, urc, valiză, autocar, portbagaj, încap
  11E  the hotel desk, "Se poate?" — recepție, cheie, înregistrez, cazare, stațiune, se poate
  11F  the weather on the mountain — apar, dispar, lună, aer, curat, fermecător
  11G  worn out after the walk — cad, tac, oboseală, somn, adânc, plimbare
  11H  when, why, abroad, the text — când, de ce, străin, limbă, traseu, aranjez, balnear
(cameră and masă are already known; lapte and încet come from the chapter's
own drink list and its "Cum?" section rather than its VOCABULAR.)

The chapter's grammar is the second group of verbs — văd, vezi, vede, vedem,
vedeți, văd — whose sound changes from person to person. After 10R the
learner asked "how am I supposed to learn all these forms when they're spelled
one after another", so a changing verb is never heard as a run: one form, in a
short sentence, recalled bare, used in a sentence — then the next. This part
teaches I, you, she, polite-you and they; the we-form comes in 11B. Forms are
then drilled out of order, never as a table.

Results through 10S also show sentences over four or five words collapsing,
so the drill sentences here stay short.

Scene: a guide on a lookout, pointing things out to tourists — "Do you see
the peak?" is the guide's job, so see comes round again and again.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["văd", "munte", "vârf", "copac", "nor", "soare"]
GLUE = {"turiștii": "the tourists — the book's word"}

ep = Episode(number=11, lesson=11, part="a", title="Vedeți vârful?",
             source="Limba care ne unește, nivelul I — Lecția 11 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Iată muntele! Vedeți vârful?"),
    ("radu", "Da, văd vârful."),
    ("dana", "Și copacii? Vedeți copacii?"),
    ("radu", "Nu, nu văd copacii."),
    ("dana", "Sunt acolo, lângă vârf. Dar e un nor mare."),
    ("radu", "Și soarele? Nu văd soarele."),
    ("dana", "Azi nu e soare."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A guide and a tourist, up in the mountains. Lesson 11 is a trip to "
        "the mountains — and the verb see.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("munte", "a mountain", "un munte", "f",
            teach_ro="Iată muntele!", teach_en="There's the mountain!")
ep.new_item("vârf", "a peak — the top of a mountain", "un vârf", "m",
            teach_ro="Vârful e înalt.", teach_en="The peak is high.")
ep.new_item("copac", "a tree", "un copac", "f",
            teach_ro="Un copac verde.", teach_en="A green tree.")
ep.new_item("nor", "a cloud", "un nor", "m",
            teach_ro="Un nor mare.", teach_en="A big cloud.")
ep.new_item("soare", "the sun", "soarele", "f",
            teach_ro="Soarele e frumos.", teach_en="The sun is lovely.")
ep.new_item("văd", "I see", "văd", "m",
            teach_ro="Văd muntele.", teach_en="I see the mountain.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("a tree", "un copac", "m"), ("I see", "văd", "f"), ("a cloud", "un nor", "m"),
                    ("a mountain", "un munte", "f"), ("the sun", "soarele", "m"),
                    ("a peak", "un vârf", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. The mountain, the peak ═══════════════════════════════════════════════
ep.narr("For the, mountain goes like brother. Listen:", pause=800,
        chapter="The mountain, the peak")
ep.ro("fratele — muntele", "m", SLOW, 1800)
ep.narr("And peak goes like the coat. Listen:", pause=P_SHORT)
ep.ro("paltonul — vârful", "f", SLOW, 1800)
ep.narr("Tree and cloud go like peak. Build them.", pause=P_SHORT)
for cue, ans, v in [("the tree", "copacul", "m"), ("the mountain", "muntele", "f"),
                    ("the cloud", "norul", "m"), ("the peak", "vârful", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. See — one form at a time ═════════════════════════════════════════════
ep.narr("See changes its sound from person to person, so take it one form at a "
        "time, each used straight away. To a friend: do you see? Listen:",
        pause=800, chapter="See, one form at a time")
ep.ro("Vezi muntele?", "f", SLOW, 1800)
ep.drill("you see — to a friend", "vezi", "m")
ep.drill("Do you see the tree? To a friend.", "Vezi copacul?", "f")

ep.narr("She sees, he sees. Listen:", pause=800)
ep.ro("Ea vede soarele.", "m", SLOW, 1800)
ep.drill("she sees", "vede", "f")
ep.drill("He sees the cloud.", "Vede norul.", "m")

ep.narr("Politely, or to a group — the guide's word. Listen:", pause=800)
ep.ro("Vedeți vârful?", "f", SLOW, 1800)
ep.drill("you see — politely", "vedeți", "m")
ep.drill("Do you see the mountain? Politely.", "Vedeți muntele?", "f")

ep.narr("And they sounds like I — as with take and give. Listen:", pause=800)
ep.ro("Turiștii văd muntele.", "m", SLOW, 1800)
ep.drill("they see", "ei văd", "f")
ep.drill("The tourists see the peak.", "Turiștii văd vârful.", "m")

ep.narr("Now mixed, and not in order.", pause=800)
for cue, ans, v in [("she sees", "vede", "f"), ("I see", "văd", "m"),
                    ("you see — politely", "vedeți", "f"), ("you see — to a friend", "vezi", "m"),
                    ("they see", "ei văd", "f"), ("he sees", "vede", "m")]:
    ep.drill(cue, ans, v)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences now — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I see the mountain.", "Văd muntele.", "m", {}),
    ("I don't see the sun.", "Nu văd soarele.", "f", {}),
    ("There's the mountain!", "Iată muntele!", "m", {}),
    ("Do you see the peak? Politely.", "Vedeți vârful?", "f", {}),
    ("Yes, I see the peak.", "Da, văd vârful.", "m", {}),
    ("The peak is high.", "Vârful e înalt.", "f", {}),
    ("It's sunny today.", "Azi e soare.", "m", {"accept": ["E soare azi."]}),
    ("There's a big cloud.", "E un nor mare.", "f", {}),
    ("Do you see the cloud? To a friend.", "Vezi norul?", "m", {}),
    ("She doesn't see the trees.", "Ea nu vede copacii.", "f", {}),
    ("The trees are next to the peak.", "Copacii sunt lângă vârf.", "m", {}),
    ("The sun is lovely.", "Soarele e frumos.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. See turns up in two everyday chunks. Saying "
        "goodbye to a friend — listen:", pause=800, chapter="How people really say it")
ep.ro("Ne vedem!", "f", SLOW, 1500)
ep.narr("See you! And when someone doesn't want to promise anything — listen:",
        pause=P_SHORT)
ep.ro("Vedem.", "m", SLOW, 1500)
ep.narr("We'll see. Just to recognise for now.", pause=P_SECTION)

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The guide again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("The mountain, the peak — and see, one form at a time.", pause=P_SHORT,
        chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("11", []))
