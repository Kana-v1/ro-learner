"""
Episode 11F — "Apare soarele" (Lecția 11 "La munte", memory-first, part 6)

Six items: apare, dispare, luna, curat, aer, fermecător. Apare and dispare
are taught as "it comes out", "it disappears" — the sun and the moon, as in
the book's dialogues ("De unde apare soarele? — Soarele apare de după
nori." / "Unde dispare soarele? — Soarele dispare după nori."). Their
they-form (apar, dispar) is heard once and built once; the I-forms, which
sound the same, aren't needed.

The book's own contrast, by ear: apare de după nori (comes out from behind)
against dispare după nori (goes behind) — one word less.

The 11D rule again with the chapter's minimal context "aer curat": fresh air,
clean water — aer curat, apă curată; and charming going like kind from 9E
(binevoitor, binevoitoare → fermecător, fermecătoare).

11E's spoken layer (Se poate? / Nu se poate!) comes back as ordinary drills.

Scene: two friends on a hotel balcony watching the weather on the mountain
— the sun comes out, goes behind a cloud, comes out again — so appear and
disappear repeat because the weather does.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["apare", "dispare", "luna", "curat", "aer", "fermecător"]
GLUE = {"Uite!": "look! — a chunk",
        "peisajul": "the view, the landscape — the book's word",
        "seara": "in the evening — as in Bună seara"}

ep = Episode(number=11, lesson=11, part="f", title="Apare soarele",
             source="Limba care ne unește, nivelul I — Lecția 11 (partea F)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Uite! Apare soarele!"),
    ("radu", "De unde apare?"),
    ("dana", "De după nori."),
    ("radu", "Și acum dispare după un nor."),
    ("dana", "Dar aerul e curat. Și peisajul e fermecător!"),
    ("radu", "Și seara apare luna."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Two friends on the hotel balcony, watching the weather on the "
        "mountain. The sun comes out, and goes again.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("apare", "it comes out, it appears — the sun, the moon", "apare", "f",
            teach_ro="Apare soarele.", teach_en="The sun comes out.")
ep.new_item("dispare", "it disappears", "dispare", "m",
            teach_ro="Soarele dispare.", teach_en="The sun disappears.")
ep.new_item("luna", "the moon", "luna", "f",
            teach_ro="Luna e mare.", teach_en="The moon is big.")
ep.new_item("curat", "clean — and, of air, fresh", "curat", "m",
            teach_ro="Un pat curat.", teach_en="A clean bed.")
ep.new_item("aer", "air", "aer", "f",
            teach_ro="Aer curat!", teach_en="Fresh air!")
ep.new_item("fermecător", "charming — of a view, a place", "fermecător", "m",
            teach_ro="Peisajul e fermecător.", teach_en="The view is charming.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("air", "aer", "m"), ("it disappears", "dispare", "f"), ("the moon", "luna", "m"),
                    ("charming", "fermecător", "f"), ("clean", "curat", "m"),
                    ("it comes out", "apare", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Comes out, disappears ════════════════════════════════════════════════
ep.narr("Comes out — from behind the clouds. Listen:", pause=800,
        chapter="Comes out, disappears")
ep.ro("Apare de după nori.", "f", SLOW, 1800)
ep.drill("It comes out from behind the clouds.", "Apare de după nori.", "m")
ep.narr("Disappears — behind the clouds. One small word less. Listen:", pause=800)
ep.ro("Dispare după nori.", "m", SLOW, 1800)
ep.drill("It disappears behind the clouds.", "Dispare după nori.", "f")
ep.narr("And more than one — the sun and the moon. Listen:", pause=800)
ep.ro("Soarele și luna apar.", "f", SLOW, 1800)
ep.drill("they come out", "apar", "m")
ep.narr("Disappear goes the same way. Build it.", pause=P_SHORT)
ep.drill("they disappear", "dispar", "f")
ep.drill("The clouds disappear.", "Norii dispar.", "m")
ep.narr("Mixed.", pause=800)
for cue, ans, v in [("it disappears", "dispare", "f"), ("they come out", "apar", "m"),
                    ("it comes out", "apare", "f"), ("they disappear", "dispar", "m"),
                    ("Where does the sun come out from?", "De unde apare soarele?", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Fresh air, clean water ═══════════════════════════════════════════════
ep.narr("Air is a his-word, water a her-word — so clean takes two forms. Listen:",
        pause=800, chapter="Fresh air, clean water")
ep.ro("Aer curat. Apă curată.", "m", SLOW, 2000)
for cue, ans, v in [("clean water", "apă curată", "f"), ("fresh air", "aer curat", "m"),
                    ("a clean room", "o cameră curată", "f"), ("a clean bed", "un pat curat", "m"),
                    ("The water is clean.", "Apa e curată.", "f")]:
    ep.drill(cue, ans, v)
ep.narr("Charming goes like kind, from the newsroom episode. Listen:", pause=800)
ep.ro("o stațiune fermecătoare", "f", SLOW, 1800)
ep.drill("a charming resort", "o stațiune fermecătoare", "m")
ep.drill("a charming view", "un peisaj fermecător", "f")

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("The sun comes out.", "Apare soarele.", "m", {"accept": ["Soarele apare."]}),
    ("The air is fresh.", "Aerul e curat.", "f", {}),
    ("In the mountains the air is fresh.", "La munte aerul e curat.", "m",
     {"accept": ["Aerul e curat la munte."]}),
    ("The view is charming.", "Peisajul e fermecător.", "f", {}),
    ("The sun disappears behind a cloud.", "Soarele dispare după un nor.", "m", {}),
    ("In the evening the moon comes out.", "Seara apare luna.", "f",
     {"accept": ["Luna apare seara."]}),
    ("Look! There's the moon!", "Uite luna!", "m", {}),
    ("Where does the moon come out from?", "De unde apare luna?", "f", {}),
    ("The resort is charming.", "Stațiunea e fermecătoare.", "m", {}),
    ("May I? At a door.", "Se poate?", "f", {}),
    ("No way!", "Nu se poate!", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The guide in this lesson pointed at the mountain "
        "the book's way. In everyday speech people point with look — listen:",
        pause=800, chapter="How people really say it")
ep.ro("Uite muntele!", "f", SLOW, 1500)
ep.narr("And at a view like this one — listen:", pause=P_SHORT)
ep.ro("Ce frumos!", "m", SLOW, 1400)
ep.narr("How lovely! Just to recognise for now.", pause=P_SECTION)

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The balcony again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("The sun comes out, the moon comes out — and the air is fresh.",
        pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("11", []))
