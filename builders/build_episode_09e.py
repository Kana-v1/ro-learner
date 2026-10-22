"""
Episode 09E — "De unde ești?" (Lecția 9 "O zi la serviciu", memory-first, part 5)

The last of Lecția 9. Six items: the chapter's de unde and de la — its
communicative intention "Cum spunem unde se desfășoară o acțiune", with the
book's own "De unde ai paltonul acesta elegant? — De la supermarket" — and
parter, muncitor, binevoitor, desenez. "Where" against "where from" is the
rule point (din, from Lecția 1, answers "De unde ești?").

Then the chapter together: -ez and plain verbs mixed, the synthesis text
"O zi la serviciu" (excerpt; redacție and oficiu are glue — oficiu is the
book's Moldovan word for an office, said in the spoken layer: in Bucharest
it's birou), and the proverb "Cine primăvara nu lucrează, în lipsă iernează."

Scene: a new colleague's first morning — where are you from, the office is on
the ground floor, who drew that picture.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["de unde", "de la", "parter", "muncitor", "binevoitor", "desenez"]
GLUE = {"redacție": "a newsroom — in the book's text",
        "oficiu": "an office — the book's word, in its text",
        "șeful": "the boss",
        "Iași": "a city in north-east Romania"}

ep = Episode(number=9, lesson=9, part="e", title="De unde ești?",
             source="Limba care ne unește, nivelul I — Lecția 9 (partea E)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Bine ai venit! De unde ești?"),
    ("radu", "Din Iași. Dar acum stau aici, aproape."),
    ("dana", "Biroul nostru e la parter."),
    ("radu", "Ce tablou frumos! De la cine e?"),
    ("dana", "De la Mihai. Desenează mult. E un coleg binevoitor."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A new colleague's first morning: where are you from, and where things "
        "come from. Then the whole of Lesson 9.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("de unde", "where from", "de unde", "m",
            teach_ro="De unde ești?", teach_en="Where are you from?")
ep.new_item("de la", "from — a place or a person", "de la", "f",
            teach_ro="Tabloul e de la Mihai.", teach_en="The picture is from Mihai.")
ep.new_item("parter", "the ground floor", "parter", "m",
            teach_ro="Biroul e la parter.", teach_en="The office is on the ground floor.")
ep.new_item("muncitor", "a worker — manual work", "un muncitor", "f",
            teach_ro="Fratele meu e muncitor.", teach_en="My brother is a worker.")
ep.new_item("binevoitor", "kind, helpful", "binevoitor", "m",
            teach_ro="Colegul meu e binevoitor.", teach_en="My colleague is kind.")
ep.new_item("desenez", "I draw", "desenez", "f",
            teach_ro="Desenez un tablou.", teach_en="I'm drawing a picture.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("the ground floor", "parter", "m"), ("I draw", "desenez", "f"),
                    ("where from", "de unde", "m"), ("a worker", "un muncitor", "f"),
                    ("from, a place or a person", "de la", "m"), ("kind, helpful", "binevoitor", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Where, and where from ════════════════════════════════════════════════
ep.narr("Where, and where from. Listen to both questions, with their answers:",
        pause=800, chapter="Where and where from")
ep.ro("Unde lucrezi? La birou. — De unde ești? Din Moldova.", "m", SLOW, 2600)
ep.narr("Where you come from takes the word from Lesson 1. Where a thing comes "
        "from — a shop, a person — takes the new one. Listen:", pause=P_SHORT)
ep.ro("De unde ai paltonul? De la magazin.", "f", SLOW, 2200)
for cue, ans, v in [("Where are you from? To a friend.", "De unde ești?", "m"),
                    ("Where do you work? To a friend.", "Unde lucrezi?", "f"),
                    ("I'm from Romania.", "Sunt din România.", "m"),
                    ("The coat is from the shop.", "Paltonul e de la magazin.", "f"),
                    ("The picture is from Mihai.", "Tabloul e de la Mihai.", "m")]:
    ep.drill(cue, ans, v)

ep.narr("Kind agrees like the others, and draw is an extra-piece verb. Listen:",
        pause=800)
ep.ro("binevoitor, binevoitoare — desenez, desenează", "m", SLOW, 2200)
for cue, ans, v in [("She is kind.", "Ea e binevoitoare.", "f"), ("he draws", "el desenează", "m"),
                    ("we draw", "noi desenăm", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences, from across the lesson.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("Where is the office? — On the ground floor.", "Unde e biroul? — La parter.", "m", {}),
    ("Where is your colleague from? To a friend.", "De unde e colegul tău?", "f", {}),
    ("My brother is a worker.", "Fratele meu e muncitor.", "m", {}),
    ("Where does your friend work? To a friend.", "Unde lucrează prietenul tău?", "f", {}),
    ("My wife is a doctor.", "Soția mea e medic.", "m", {}),
    ("The boss is demanding, but kind.", "Șeful e exigent, dar binevoitor.", "f", {}),
    ("Today we organise a competition for a vacant post.", "Azi organizăm un concurs pentru un post vacant.", "m", {}),
    ("The secretary writes down their names.", "Secretara notează numele lor.", "f", {}),
    ("We have a meeting at ten. We're punctual.", "Avem ședință la zece. Suntem punctuali.", "m", {}),
    ("Who draws here? — Mihai.", "Cine desenează aici? — Mihai.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The book's text calls the office by a Moldovan "
        "word. In Bucharest an office is the word you already know. Listen — "
        "the book's, then Bucharest's:", pause=800, chapter="How people really say it")
ep.ro("oficiu — birou", "f", SLOW, 1600)
ep.narr("You'll meet the first in names, like the post office, but not for the "
        "place you work.", pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 6. Text — the chapter's own ═════════════════════════════════════════════
ep.narr("Now the chapter's own text: a day at work in a newsroom. Two words are "
        "new and clear from the story — a newsroom, and the book's word for an "
        "office. Slowly first.", pause=800, chapter="Text")
BOOK_TEXT = [
    "Prenumele meu e Dan. Lucrez la o redacție. Sunt ziarist.",
    "La ora nouă suntem la oficiu. Oficiul nostru e la parter.",
    "În biroul nostru sunt trei mese și trei scaune. Pe mese avem calculatoare.",
    "Azi organizăm un concurs pentru un post vacant.",
    "Șeful examinează actele. Secretara notează în agendă numele și prenumele lor.",
    "Azi avem ședință la ora zece. Noi suntem punctuali.",
    "După ședință, șeful angajează un coleg nou. El este elegant și binevoitor.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

ep.narr("And the chapter's proverb. Listen:", pause=800, chapter="Proverb")
ep.ro("Cine primăvara nu lucrează, în lipsă iernează.", "f", SLOW, 1800)
ep.narr("Whoever doesn't work in spring spends the winter in want. Once more:",
        pause=P_SHORT)
ep.ro("Cine primăvara nu lucrează, în lipsă iernează.", "f", NORMAL, 1400)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The first morning again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That closes Lesson 9: work, the verbs with the extra piece, and where "
        "things come from.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's the whole of Lesson 9.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("9", []))
