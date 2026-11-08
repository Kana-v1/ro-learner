"""
Episode 11E — "Se poate intra?" (Lecția 11 "La munte", memory-first, part 5)

Six items: recepție (as "la recepție"), cheie, înregistrez, cazare, stațiune,
and the chapter's "se poate + verb" ("Se poate intra? — Da, se poate. — Nu,
nu se poate."). The verb after se poate takes the same form as after pot
(11C); bea and mânca are heard, not built, since they can't be worked out.
Înregistrez is an -ez verb, built from the 9A pattern.

Her-words with "the": cheie → cheia and recepție → recepția go like rochie →
rochia; stațiune → stațiunea just gains a sound. Rochia e prea lungă is the
learner's third most-missed answer, so it is asked here as part of the
pattern. The describing word follows the small word, as answered in 11D
(Stațiunea e frumoasă).

(Balnear, planned for this part, moves to 11H, where the book's text uses it:
"o stațiune balneară".)

11D's spoken layer (Hai, plecăm! / Plecăm?) comes back as ordinary drills,
and 9A's Bine ați venit! as ordinary speech in the dialogue.

Scene: a hotel reception desk, guests arriving one after another — name,
documents, key — so register and key come round for each guest.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["recepție", "cheie", "înregistrez", "cazare", "stațiune", "se poate"]
GLUE = {"rezervată": "booked — in 'o cameră rezervată', a chunk"}

ep = Episode(number=11, lesson=11, part="e", title="Se poate intra?",
             source="Limba care ne unește, nivelul I — Lecția 11 (partea E)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Bună ziua! Bine ați venit!"),
    ("radu", "Bună ziua! Am o cameră rezervată."),
    ("dana", "Numele, vă rog?"),
    ("radu", "Ionescu. Poftiți actele."),
    ("dana", "Mulțumesc. Înregistrez actele... Poftiți cheia!"),
    ("radu", "Se poate intra acum?"),
    ("dana", "Da, se poate."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Arriving at the mountain resort: the reception desk, documents, a key. "
        "And how to ask if something is allowed.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("stațiune", "a resort", "o stațiune", "f",
            teach_ro="O stațiune la munte.", teach_en="A resort in the mountains.")
ep.new_item("recepție", "at reception — in a hotel", "la recepție", "m",
            teach_ro="Sunt la recepție.", teach_en="I'm at reception.")
ep.new_item("cheie", "a key", "o cheie", "f",
            teach_ro="Poftiți cheia!", teach_en="Here's the key!")
ep.new_item("înregistrez", "I register — documents, guests", "înregistrez", "m",
            teach_ro="Înregistrez actele.", teach_en="I register the documents.")
ep.new_item("cazare", "accommodation, a place to stay", "cazare", "f",
            teach_ro="Cazare și masă.", teach_en="Accommodation and meals.")
ep.new_item("se poate", "is it allowed? — can one?", "Se poate?", "m",
            teach_ro="Se poate intra?", teach_en="Is it all right to go in?")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("a key", "o cheie", "m"), ("is it allowed?", "Se poate?", "f"),
                    ("a resort", "o stațiune", "m"), ("I register", "înregistrez", "f"),
                    ("accommodation", "cazare", "m"), ("at reception", "la recepție", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Is it allowed? ═══════════════════════════════════════════════════════
ep.narr("Is it allowed takes a verb after it — the same form as after can. "
        "Listen:", pause=800, chapter="Is it allowed?")
ep.ro("Se poate intra?", "f", SLOW, 1600)
ep.drill("Is it all right to go in?", "Se poate intra?", "m")
ep.narr("Yes, it is. Listen:", pause=800)
ep.ro("Da, se poate.", "m", SLOW, 1500)
ep.drill("Yes, it's allowed.", "Da, se poate.", "f")
ep.narr("No, it isn't. Listen:", pause=800)
ep.ro("Nu, nu se poate.", "f", SLOW, 1600)
ep.drill("No, it isn't allowed.", "Nu, nu se poate.", "m")
ep.narr("Draw and sign go like go in. Build them.", pause=P_SHORT)
ep.drill("Is it all right to draw here?", "Se poate desena aici?", "f")
ep.drill("Is it all right to sign here?", "Se poate semna aici?", "m")
ep.narr("Drink and eat you can't work out — just hear them. Drink:", pause=800)
ep.ro("Se poate bea apa?", "m", SLOW, 1800)
ep.drill("Can you drink the water?", "Se poate bea apa?", "f")
ep.narr("Eat:", pause=P_SHORT)
ep.ro("Se poate mânca aici?", "f", SLOW, 1800)
ep.drill("Is it all right to eat here?", "Se poate mânca aici?", "m")

# ═══ 3. The key, the resort ══════════════════════════════════════════════════
ep.narr("Key is a her-word. For the, it goes like dress. Listen:", pause=800,
        chapter="The key, the resort")
ep.ro("rochia — cheia", "f", SLOW, 1800)
ep.narr("Reception goes the same way. Build it.", pause=P_SHORT)
ep.drill("the reception", "recepția", "m")
ep.drill("the key", "cheia", "f")
ep.narr("Resort just gains a sound. Listen:", pause=800)
ep.ro("stațiunea", "m", SLOW, 1500)
ep.drill("the resort", "stațiunea", "f")
ep.narr("And as last time, a her-word takes the her-form of a describing word.",
        pause=P_SHORT)
for cue, ans, v in [("The resort is lovely.", "Stațiunea e frumoasă.", "m"),
                    ("The key is small.", "Cheia e mică.", "f"),
                    ("The dress is too long.", "Rochia e prea lungă.", "m"),
                    ("The reception is big.", "Recepția e mare.", "f")]:
    ep.drill(cue, ans, v)

# ═══ 4. Register ═════════════════════════════════════════════════════════════
ep.narr("Register goes like work — with the extra piece. Build them.", pause=800,
        chapter="Register")
for cue, ans, v in [("she registers", "înregistrează", "f"), ("we register", "înregistrăm", "m"),
                    ("you register — politely", "înregistrați", "f"),
                    ("She registers the documents.", "Ea înregistrează actele.", "m")]:
    ep.drill(cue, ans, v)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I have a room booked.", "Am o cameră rezervată.", "m", {}),
    ("Your name, please?", "Numele, vă rog?", "f", {}),
    ("Here are the documents. Politely.", "Poftiți actele.", "m", {}),
    ("I register the documents.", "Înregistrez actele.", "f", {}),
    ("Here's the key! Politely.", "Poftiți cheia!", "m", {}),
    ("The key is at reception.", "Cheia e la recepție.", "f", {}),
    ("Is it all right to go in now?", "Se poate intra acum?", "m", {}),
    ("Accommodation and meals.", "Cazare și masă.", "f", {}),
    ("The resort is in the mountains.", "Stațiunea e la munte.", "m", {}),
    ("Is the accommodation expensive?", "Cazarea e scumpă?", "f", {}),
    ("Welcome! Politely.", "Bine ați venit!", "m", {}),
    ("Come on, we're off!", "Hai, plecăm!", "f", {}),
    ("Shall we go?", "Plecăm?", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 6. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. At a door, or pointing at a free chair, people "
        "just say — listen:", pause=800, chapter="How people really say it")
ep.ro("Se poate?", "f", SLOW, 1400)
ep.narr("May I? And no, it isn't allowed, said with feeling, means no way! "
        "Listen:", pause=P_SHORT)
ep.ro("Nu se poate!", "m", SLOW, 1500)
ep.narr("No way — you're joking! Just to recognise for now.", pause=P_SECTION)

# ═══ 7. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The reception desk again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("The key, the resort — and is it allowed.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("11", []))
