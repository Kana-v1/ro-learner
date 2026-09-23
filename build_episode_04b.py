"""
Episode 04B — "Sunt acasă (B)" (Lecția 4, second half)

The second half of Lecția 4: the furniture and things inside the rooms, the
prepositions sub (under), după (behind) and pentru (for), and the chapter's big
grammar point — the plural. One chair becomes some chairs: un/o gives way to
niște, the noun ending shifts, and acesta/aceasta become aceștia/acestea.

Scene: the apartment tour continues, now into what is in each room — "in the
bedroom there are some nightstands, on them some magazines." Listing what fills
a room is exactly where plurals come out naturally, so the repetition of niște
is a host describing her rooms, not an exercise. The chapter's own synthesis
text does precisely this and closes the episode; by now every word in it has
been taught across 4A and 4B.

Continuity: 4A's rooms and the politeness pronouns are ordinary speech now.
Dropped -l (frigideru', dulapu') and the earlier spoken forms continue.
"""
from episode_kit import Episode, load, P_SECTION, NORMAL, SLOW

# The furniture-and-objects half of Lecția 4's VOCABULAR block, plus the
# prepositions this half is built on. The plural (niște, aceștia/acestea) is
# grammar taught here, not a vocab-list item, so it is not in REQUIRED.
REQUIRED = [
    "mobilă", "canapea", "fotoliu", "dulap", "noptieră", "frigider",
    "oglindă", "chiuvetă", "cadă", "robinet", "cuier", "raft",
    "revistă", "ziar",
    "sub", "după", "pentru",
]

GLUE = {
    "familie": "family",
    "mare": "big",
    "frumos": "nice",
    "Sanda / Radu": "names",
}

ep = Episode(number=4, lesson=4, part="b", title="Sunt acasă (B)",
             source="Limba care ne unește, nivelul I — Lecția 4 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Deci, în dormitor e un dulap și niște noptiere."),
    ("radu",  "Ce e pe noptiere?"),
    ("dana",  "Pe noptiere sunt niște reviste și niște ziare."),
    ("radu",  "Dar în salon? Ce e acolo?"),
    ("dana",  "În salon sunt o canapea, niște fotolii și un covor."),
    ("radu",  "Frumos. Și în bucătărie?"),
    ("dana",  "Un frigider, o chiuvetă și mobilă de bucătărie."),
    ("radu",  "Ce e sub raft?"),
    ("dana",  "Sub raft e un fotoliu. Iar după ușă e un cuier."),
    ("radu",  "Dar oglinda? E în baie?"),
    ("dana",  "Da, oglinda e în baie, lângă cadă. Acolo e și un robinet."),
    ("radu",  "Un apartament pentru o familie mare!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The tour again, now into the rooms — the wardrobe and the nightstands, "
        "the sofa and the armchairs. Notice how often one thing becomes several: "
        "niște, some. That is this episode's grammar, and it is everywhere.",
        pause=P_SECTION)

# ═══ 1. Vocabulary — the furniture ═══════════════════════════════════════════
ep.narr("What fills the rooms, each inside a sentence.", pause=800,
        chapter="The furniture")
for r, e, v in [
    ("Aceasta e o canapea.", "This is a sofa.", "f"),
    ("Acesta e un fotoliu.", "This is an armchair.", "m"),
    ("Acesta e un dulap.", "This is a wardrobe.", "m"),
    ("Aceasta e o noptieră.", "This is a nightstand.", "f"),
    ("Acesta e un frigider.", "This is a fridge.", "m"),
    ("Aceasta e o oglindă.", "This is a mirror.", "f"),
    ("Aceasta e o chiuvetă.", "This is a sink.", "f"),
    ("Aceasta e o cadă.", "This is a bathtub.", "f"),
    ("Acesta e un robinet.", "This is a tap.", "m"),
    ("Acesta e un cuier.", "This is a coat rack.", "m"),
    ("Acesta e un raft.", "This is a shelf.", "m"),
    ("Aceasta e o revistă.", "This is a magazine.", "f"),
    ("Acesta e un ziar.", "This is a newspaper.", "m"),
    ("Aceasta e mobilă de bucătărie.", "This is kitchen furniture.", "f"),
]:
    ep.teach(r, e, v)

# ═══ 2. Under, behind, for ═══════════════════════════════════════════════════
ep.narr("Three more placing words, on top of pe and lângă from last time. Sub "
        "— under. După — behind. Pentru — for.", pause=800,
        chapter="sub, după, pentru")
for r, e in [("Sub masă e un covor.", "Under the table there is a carpet."),
             ("După ușă e un cuier.", "Behind the door there is a coat rack."),
             ("Pe raft e o revistă.", "On the shelf there is a magazine."),
             ("Un ziar pentru domnu' Radu.", "A newspaper for Mr Radu.")]:
    ep.teach(r, e, "m")

# ═══ 3. Grammar — the plural ═════════════════════════════════════════════════
ep.narr("Now the big one. One becomes many. Un and o give way to niște — some "
        "— and the end of the word changes with the gender.", pause=800,
        chapter="The plural")

ep.narr("Masculine adds -i.")
for r, e in [("un cursant, niște cursanți", "a student, some students"),
             ("un profesor, niște profesori", "a teacher, some teachers")]:
    ep.teach(r, e, "m")
ep.narr("Feminine goes to -e, or sometimes -i.")
for r, e in [("o revistă, niște reviste", "a magazine, some magazines"),
             ("o canapea, niște canapele", "a sofa, some sofas"),
             ("o oglindă, niște oglinzi", "a mirror, some mirrors")]:
    ep.teach(r, e, "f")
ep.narr("Neuter adds -uri or -e.")
for r, e in [("un ziar, niște ziare", "a newspaper, some newspapers"),
             ("un fotoliu, niște fotolii", "an armchair, some armchairs"),
             ("un dulap, niște dulapuri", "a wardrobe, some wardrobes")]:
    ep.teach(r, e, "m")
ep.narr("The vowel sometimes shifts inside the word too — masă becomes mese, "
        "sală becomes săli. Do not memorise a table; you will catch these by "
        "ear. What matters now: niște means some, and the ending moves.",
        pause=600)

ep.narr("And this from earlier becomes plural to match. Acesta and aceasta "
        "turn into aceștia and acestea.", pause=600)
for r, e in [("Acesta e un fotoliu. Acestea sunt niște fotolii.",
              "This is an armchair. These are some armchairs."),
             ("Aceasta e o revistă. Acestea sunt niște reviste.",
              "This is a magazine. These are some magazines."),
             ("Acesta e un cursant. Aceștia sunt niște cursanți.",
              "This is a student. These are some students.")]:
    ep.teach(r, e, "m")
ep.narr("Aceștia only for a group of men. Acestea for feminine and for neuter "
        "— for things, in other words. So chairs and magazines are always "
        "acestea.", pause=P_SECTION)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("The dropped L once more, now on this chapter's things. The book "
        "writes frigiderul, dulapul, robinetul, ziarul. What you hear is:",
        pause=800, chapter="How people really say it")
for r in ["frigideru'", "dulapu'", "robinetu'", "ziaru'"]:
    ep.ro(r, "m", SLOW, 1000)
ep.narr("Feminine keeps its ending — oglinda, canapeaua, not clipped. Same rule "
        "as always, more rooms to use it in.", pause=P_SECTION)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work, and the plural runs all through it. A whole sentence out "
        "loud each time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v in [
    ("This is a sofa.", "Aceasta e o canapea.", "f"),
    ("This is an armchair.", "Acesta e un fotoliu.", "m"),
    ("This is a wardrobe, and this is a fridge.",
     "Acesta e un dulap, iar acesta e un frigider.", "m"),
    ("This is a nightstand.", "Aceasta e o noptieră.", "f"),
    ("This is a mirror.", "Aceasta e o oglindă.", "f"),
    ("This is a sink, and this is a bathtub.",
     "Aceasta e o chiuvetă, iar aceasta e o cadă.", "f"),
    ("This is a tap.", "Acesta e un robinet.", "m"),
    ("This is a shelf, and this is a coat rack.",
     "Acesta e un raft, iar acesta e un cuier.", "m"),
    ("This is a magazine, and this is a newspaper.",
     "Aceasta e o revistă, iar acesta e un ziar.", "f"),
    ("These are some magazines.", "Acestea sunt niște reviste.", "f"),
    ("These are some armchairs.", "Acestea sunt niște fotolii.", "m"),
    ("These are some newspapers.", "Acestea sunt niște ziare.", "m"),
    ("In the bedroom there are some nightstands.",
     "În dormitor sunt niște noptiere.", "f"),
    ("On the shelf there are some magazines and newspapers.",
     "Pe raft sunt niște reviste și niște ziare.", "f"),
    ("Under the table there is a carpet.", "Sub masă e un covor.", "m"),
    ("Behind the door there is a coat rack.", "După ușă e un cuier.", "m"),
    ("A shelf for books.", "Un raft pentru cărți.", "m"),
    ("This is kitchen furniture.", "Aceasta e mobilă de bucătărie.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 6. Review of episode 3 and 4A ═══════════════════════════════════════════
ep.review([
    ("This is a house.", "Aceasta e o casă.", "f"),
    ("He is at home. — respectfully.", "Dumnealui e acasă.", "m"),
    ("The apartment is near, the house is far.",
     "Apartamentul e aproape, casa e departe.", "m"),
    ("On the wall there is a picture.", "Pe perete e un tablou.", "m"),
    ("What is this? — A dictionary.", "Ce e acesta? Un dicționar.", "m"),
    ("Where do you live?", "Unde locuiești?", "f"),
])

# ═══ 7. Text — the chapter's own passage ═════════════════════════════════════
ep.narr("Now the chapter's own text, whole. Every word in it you have across "
        "both halves. Slowly first.", pause=800, chapter="Text")
BOOK_TEXT = [
    "Sunt acasă. În apartament sunt: un antreu, o bucătărie, un dormitor, "
    "un salon și o baie.",
    "În antreu este un cuier. Lângă cuier este o oglindă.",
    "În bucătărie sunt o masă, niște scaune, un frigider, o chiuvetă "
    "și mobilă de bucătărie.",
    "În dormitor sunt un dulap și niște noptiere.",
    "Pe noptiere sunt niște reviste și niște ziare. Pe perete este un tablou.",
    "În salon sunt o canapea, niște fotolii, o masă și niște scaune.",
    "În baie sunt o cadă, o chiuvetă, o oglindă.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The rooms again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That closes Lecția 4. You can furnish a room and say how many of "
        "everything there are.", pause=600)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("Before next time: name what is in one room of your home, and count it "
        "up — un fotoliu, niște fotolii. Pe curând!", pause=1500,
        chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("4", []))
