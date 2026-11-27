"""
Episode 13B — "Mâncarea e caldă" (Lecția 13 "În vizită la prieteni", memory-first, part 2)

Six items: mâncare, farfurie, pahar, lingură, cald, rece — the book's
exercise 2 ("Spuneți cum este: … apa, ciorba, mâncarea — cald, rece") and the
text's "Dan aduce tacâmurile: farfurii, pahare, linguri".

Hot changes for a feminine thing (ceaiul e cald, mâncarea e caldă) — heard
side by side, then built. Cold doesn't change at all, which the learner can
use at once (apa e rece, ceaiul e rece). The plurals are heard with a number,
one at a time (două farfurii, două pahare, două linguri), never as a list;
the definite plurals are left for later.

12F's acela/aceea was still mixed up with acesta ("Acesta" for that one, twice),
so "paharul acela" and "farfuria aceea" are asked here as ordinary use.
13A's spoken layer (Mersi, la fel!) is ordinary speech in the dialogue.

Scene: an hour before the guests come, Dana and Radu lay the table — so
plates, glasses and spoons are counted out for four, and the food and water
are checked.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["mâncare", "farfurie", "pahar", "lingură", "cald", "rece"]
GLUE = {"te rog": "please — to a friend; vă rog is the polite one"}

ep = Episode(number=13, lesson=13, part="b", title="Mâncarea e caldă",
             source="Limba care ne unește, nivelul I — Lecția 13 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Oaspeții vin la ora șapte. Am nevoie de ajutor."),
    ("radu", "Aduc patru farfurii și patru pahare."),
    ("dana", "Mersi! Și patru linguri, te rog."),
    ("radu", "Mâncarea e caldă?"),
    ("dana", "Da, e caldă. Și apa e rece."),
    ("radu", "Paharul acela e pentru oaspeți?"),
    ("dana", "Nu, acela e pentru bunica."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("An hour before the guests come, the table has to be laid.",
        pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("farfurie", "a plate", "o farfurie", "m",
            teach_ro="O farfurie pentru oaspete.", teach_en="A plate for the guest.")
ep.new_item("cald", "warm, hot", "cald", "f",
            teach_ro="Ceaiul e cald.", teach_en="The tea is hot.")
ep.new_item("pahar", "a glass", "un pahar", "m",
            teach_ro="Un pahar de apă.", teach_en="A glass of water.")
ep.new_item("mâncare", "food", "mâncare", "f",
            teach_ro="Bunica face mâncare.", teach_en="Grandma is cooking.")
ep.new_item("rece", "cold", "rece", "m",
            teach_ro="Apa e rece.", teach_en="The water is cold.")
ep.new_item("lingură", "a spoon", "o lingură", "f",
            teach_ro="O lingură pentru fiecare.", teach_en="A spoon for everyone.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("a spoon", "o lingură", "m"), ("cold", "rece", "f"),
                    ("a plate", "o farfurie", "m"), ("food", "mâncare", "f"),
                    ("a glass", "un pahar", "m"), ("warm, hot", "cald", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Hot and cold ═════════════════════════════════════════════════════════
ep.narr("Hot changes for a feminine thing, like interesting did. Listen to "
        "both:", pause=800, chapter="Hot and cold")
ep.ro("Ceaiul e cald. Mâncarea e caldă.", "f", SLOW, 2400)
ep.drill("The food is hot.", "Mâncarea e caldă.", "m")
ep.drill("hot tea", "un ceai cald", "f")
ep.drill("warm water", "apă caldă", "m")
ep.narr("Cold doesn't change at all. Build these.", pause=P_SHORT)
ep.drill("cold water", "apă rece", "f")
ep.drill("The tea is cold.", "Ceaiul e rece.", "m")
ep.drill("The evening is cold.", "Seara e rece.", "f")
for cue, ans, v in [("The water is cold.", "Apa e rece.", "m"),
                    ("The tea is hot.", "Ceaiul e cald.", "f"),
                    ("The food is cold.", "Mâncarea e rece.", "m"),
                    ("hot food", "mâncare caldă", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Plates, glasses, spoons — two of each ════════════════════════════════
ep.narr("Two plates — listen:", pause=800, chapter="Two of each")
ep.ro("Două farfurii.", "m", SLOW, 1700)
ep.drill("two plates", "două farfurii", "f")
ep.drill("four plates", "patru farfurii", "m")
ep.narr("Two glasses — listen:", pause=P_SHORT)
ep.ro("Două pahare.", "f", SLOW, 1700)
ep.drill("two glasses", "două pahare", "m")
ep.drill("four glasses", "patru pahare", "f")
ep.narr("Two spoons — listen:", pause=P_SHORT)
ep.ro("Două linguri.", "m", SLOW, 1700)
ep.drill("two spoons", "două linguri", "f")
ep.narr("Mixed.", pause=800)
for cue, ans, v in [("four glasses", "patru pahare", "m"), ("a spoon", "o lingură", "f"),
                    ("two plates", "două farfurii", "m"), ("a glass", "un pahar", "f"),
                    ("four spoons", "patru linguri", "m")]:
    ep.drill(cue, ans, v)

# ═══ 4. That one ═════════════════════════════════════════════════════════════
ep.narr("That one, from last time, on the table.", pause=800, chapter="That one")
ep.drill("that glass", "paharul acela", "f")
ep.drill("that plate", "farfuria aceea", "m")
ep.drill("this glass", "paharul acesta", "f")
ep.drill("Is that glass for the guests?", "Paharul acela e pentru oaspeți?", "m")

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("The guests are coming at seven.", "Oaspeții vin la ora șapte.", "f",
     {"accept": ["Oaspeții vin la șapte."]}),
    ("I need help.", "Am nevoie de ajutor.", "m", {}),
    ("I'm bringing four plates.", "Aduc patru farfurii.", "f", {}),
    ("A glass of water, please. To a friend.", "Un pahar de apă, te rog.", "m", {}),
    ("Is the food hot?", "Mâncarea e caldă?", "f", {}),
    ("The water is cold.", "Apa e rece.", "m", {}),
    ("Grandma is cooking.", "Bunica face mâncare.", "f", {}),
    ("A plate for the guest.", "O farfurie pentru oaspete.", "m", {}),
    ("Thanks! To a friend.", "Mersi!", "f", {"accept": ["Mulțumesc!"]}),
    ("Enjoy your meal! — Thanks, you too!", "Poftă bună! — Mersi, la fel!", "m",
     {"accept": ["Poftă bună! — Mulțumesc, la fel!"]}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 6. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. When the food is ready, people call everyone "
        "to the table like this. Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Hai la masă!", "f", SLOW, 1500)
ep.narr("And the everyday way to say I'm hungry. Listen:", pause=P_SHORT)
ep.ro("Mi-e foame.", "m", SLOW, 1500)
ep.narr("Just to recognise for now.", pause=P_SECTION)

# ═══ 7. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("Laying the table again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("Plates, glasses, spoons — hot food and cold water.",
        pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("13", []))
