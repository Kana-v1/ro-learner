# Romanian audio course

Generating a 40-episode audio course from the textbook *Limba care ne unește,
nivelul I* (Chișinău, 2003) so I can actually retain vocabulary. Claude writes
the episode scripts, Azure Speech renders them, the result goes out as a
private podcast feed.

I am on chapter 31 of the book but starting the audio from chapter 1, to
consolidate what I half-know.

## Layout

```
prep_book.py           raw pdftotext output  ->  data/
build_episode_NN.py    one per episode, content only  ->  episodes/
episode_kit.py         shared builder machinery + the checks
render.py              episodes/*.json  ->  out/*.mp3 + .srt
make_feed.py           out/*.mp3  ->  out/feed.xml
list_voices.py         which Azure voices speak Romanian
sample_voices.py       A/B a phrase across voices before committing
make_review_sheet.py   data/spoken.json -> markdown for a native speaker
make_lesson_pack.py    episodes + cached clips -> packs/*.rolesson for the app
ingest_results.py      app results -> state.json "struggles" + a note back to the app
app/                   Vorbește, the iOS drill player (Swift, built on GitHub Actions)

data/       book_fixed.txt, lessons.json, glossary.json, spoken.json
episodes/   generated scripts
out/        rendered audio, subtitles, feed        (gitignored)
.cache/     synthesised segments keyed by content hash (gitignored)
.build/     ffmpeg scratch                          (gitignored)
```

## Commands

```bash
python3 prep_book.py ~/path/rom_book_parsed.txt
python3 build_episode_02.py
python3 render.py episodes/episode_02.json          # --only 0:13 for a cheap trial
python3 make_feed.py --base-url https://.../ro-a7f3c1
```

## Environment

```bash
export AZURE_SPEECH_KEY=...
export AZURE_SPEECH_REGION=westeurope
```

No ElevenLabs key — the account would not issue one, and Azure covers
everything. `render.py` still supports ElevenLabs per voice if that changes.

## Decisions already made

**Memory-first, not coverage-first (the 2026-09 rebuild).** The original design
sized each episode to a textbook chapter — sixteen-plus new items in one sitting
— and retention was near zero: a word heard once inside a pile of similar words
cannot be produced. The rule now is at most ~6 new items per episode (the build
fails above 8), with the majority of every episode spent on retrieval, not new
material. Episode size is set by memory load, not by the chapter. This overturns
three earlier decisions below (chapter-coupled splitting, whole-sentence-only
drills) — they are kept, struck through in spirit, only as history. Episodes 1–4
predate the rebuild and are left as rendered; their vocabulary is seeded into
`state.json` so the spacing engine spirals it back into episodes 5+ without
re-rendering them. Backfilling 1–4 into memory-first episodes is optional and
not yet done.

**Pedagogy lives in the `lesson-audio-script` skill.** Read it before writing
an episode. It covers scene design, drill construction, length budgets, L1
share and spacing. The single most important rule: choose a scene where
repetition of the target structure is *realistic* (a roll call, a registration
desk, someone being shown round an office), so the pedagogical repetition
sounds like a person doing their job.

**Target variety is Bucharest Romanian, polite-neutral register.** Colleagues,
shops, strangers. Exclude Moldovan and Transylvanian regionalisms (`no` as a
filler, `servus`) and anything below neutral (`bă`, `mă`, `mișto`, `gen`).
This matters because the textbook itself is Moldovan.

**L1 is English.** The book's own back glossary is trilingual
(Romanian–Russian–English), so English glosses come from the book rather than
from a fresh translation. `data/glossary.json` carries both.

**Every episode carries a spoken-register layer.** The book is 25 years old and
teaches correct rather than spoken Romanian. Each episode ends with a section
contrasting the two: `este` vs `e`, dropped final `-l` (`domnu'`, `birou'`),
fillers (`păi`, `deci`), and phrases the book omits entirely (`Îmi pare bine`,
`Mulțumesc`, `Cu ce vă ocupați?`). Items live in `data/spoken.json`, keyed by
lesson, each with a confidence flag.

**The spoken layer of episode N becomes ordinary speech in the dialogue of
episode N+1.** Not re-taught, just used. Episode 2's dialogue already does this
with `domnu'`, `e`, `deci` and `Îmi pare bine`.

**Colloquial usage is the least reliable part of this project.** A grammar slip
is forgivable; a misused register marker is not. Everything in `spoken.json`
goes to a native speaker for review in one batch at the end, via
`make_review_sheet.py`. Do not treat these items as settled.

**Dialogue uses pro-drop, drills use full forms.** Romanian drops subject
pronouns; the textbook spells them all out to make them visible. Dialogue
models real speech, drill practises the full paradigm, and the narrator points
out the difference.

**Glue budget: at most four items per episode** from outside the chapter's word
list, delivered as whole chunks with no grammatical analysis. The build fails
if this is exceeded.

**Grade the recall; reach whole sentences, don't start there.** *(Revised in the
rebuild — supersedes the old "drill every new word inside whole sentences"
rule.)* Asking for a full sentence on an item's first retrieval fails when the
word itself is not yet retrievable, and rehearsing that failure is what the old
episodes did. Instead: introduce an item, retrieve the bare word from an English
cue seconds later (`ep.new_item()` does both, plus registers it for review),
and only once the words are held ask for them assembled into whole sentences.
Each new item still ends up in several whole sentences across different frames;
it just is not the first thing asked. Lengthen with more retrieval, never new
material.

**A recap episode after every five lessons.** A generalization episode with no
new vocabulary — pure retrieval across the block, organised by grammar thread
and communicative function, mirroring the textbook's own RECAPITULARE section.
It weaves the block into one cold-open dialogue and a closing self-introduction.
Named with `part="r"` (`episode_05r`, `episode_10r`, …) so it sorts after the
block's last episode; `REQUIRED` is a spread of anchor items, a few per lesson,
so the coverage check proves it touched all five. Follow `build_episode_05r.py`.
"Every five lessons" tracks the book, not the raw episode count (lessons split
into one or two episodes each).

**Recall pauses are proportional to the answer.** `recall_pause()` in
`episode_kit.py` sizes the production silence from the answer's word count —
~2.5 s for one word up to a 9 s ceiling — because a flat pause is always wrong
for one length or the other, and the learner is producing aloud on the move.
`drill()` uses it by default; pass an explicit pause only for a deliberate
exception. Retune via the formula's constants, then re-build and re-render — the
pause lives in silence clips, so the audio cache is untouched and only the gaps
change. `build_episode_01.py` carries its own inline constants and is left as-is
(see Known inconsistency); episodes 5A–5E predate the proportional pause and
will pick it up on their next rebuild+render at no cache cost.

**The English narrator never speaks Romanian.** A learner cannot parse Romanian
in an English accent, so every Romanian word or phrase heard comes from a
Romanian voice. Grammar and paradigms are set up in English then spoken by the
Romanian voice via `ep.example(setup_en, romanian, voice)`; never quote Romanian
inside a `narr()` segment. The sign-off (`Pe curând!`) is a Romanian-voice
segment, not narrator text. The build warns and fails on diacritic-bearing
Romanian left in an English-voice segment — a backstop, not a substitute for
writing it right (it cannot catch diacritic-free Romanian like `am un frate`).

**No between-episodes tasks.** Episodes end on a short sign-off, not homework —
the learner listens on the move and will not do a "before next time" exercise.
All producing happens inside the drills. (Episodes 1–5 still carry the old
closing tasks; harmless, replaced on rebuild.)

**Spaced review is now an engine, not hand-picking (`data/state.json`).** Each
episode registers its new items on emit; `ep.review_auto()` pulls whatever is
due on the +1/+3/+7/+16 schedule, oldest gap first, capped ~7. Due-ness is a
pure function of the `sequence` list and intervals, so builds only read the
schedule and append their own items — build episodes in `sequence` order so an
item is registered before the episode that reviews it. Prior episodes 1–4 were
seeded from their own validated drill answers. The old hand-picked `ep.review([
…])` still exists for one-offs but new episodes use `review_auto()`.

## The Vorbește app and the results loop

`app/` is an iOS app that plays an episode, stops as each drill cue ends,
listens (Apple's on-device Romanian recognition), grades the words
(`Grader.swift`: diacritics folded, dropped pronouns allowed, `e` = `este`),
gives an immediate second try, speaks the verdict, then plays the episode's own
answer. Misses come back once more at the end. It works from a pocket: a
chime for "your turn", spoken verdicts, headphone next/previous = next/previous
drill. It resumes where it stopped.

- **Episodes for the app** are `.rolesson` files from `make_lesson_pack.py`
  (sample-exact audio + the prompt/answer marks from the episode JSON). Pack
  after rendering: `python3 make_lesson_pack.py episodes/episode_06c.json`.
- **Drive folder.** The app links one folder (normally Google Drive via the
  Files app) with `lessons/` (episodes in), `results/` (one JSON per finished
  session out) and `notes/` (Claude's notes in). With Google Drive for desktop
  in "Mirror files" mode, set `VORBESTE_DRIVE` to that folder as seen from WSL
  (e.g. `/mnt/c/Users/<you>/My Drive/Vorbește`) and the pack script writes
  straight into `lessons/`. Episode audio is too big for the Drive connector.
- **When the user says "Read my Romanian results from Google Drive":** run
  `python3 ingest_results.py` (reads `$VORBESTE_DRIVE/results`; without the
  mirror, fetch the small JSON files with the Google Drive connector into a
  folder and pass `--results-dir`). It archives sessions under `data/results/`
  (gitignored: transcripts of the user's speech), writes the drills still wrong
  into `state.json` `struggles`, and prints a summary. Analyse it — patterns
  (endings, agreement, a word that never sticks) matter more than single misses
  — then send a short plain-English report back with
  `python3 ingest_results.py --note "…"`; it lands in `notes/` (or `packs/`
  without the mirror) and the app shows it and marks those sessions analysed.
- **`review_auto()` puts struggles first** (up to 4, most missed first, only
  from episodes before the one being built), then the +1/+3/+7/+16 schedule.
  So building the next episodes after an ingest is what adapts the course.
- **Building the app:** pushing changes under `app/` triggers
  `.github/workflows/ios.yml` on a GitHub macOS runner; the unsigned `.ipa` is
  the `RoLearner-ipa` artifact (`gh run download`). The user installs it with
  Sideloadly (free Apple ID, refresh every 7 days). No Mac here, so the CI build
  is the compiler: read its log with `gh run view --log-failed`. The bundle id
  stays `io.github.kanav1.rolearner` so installs update in place. Swift 5
  language mode on purpose.
- **Repo is public** (Kana-v1/ro-learner). The book's raw files, rendered audio,
  packs and results are gitignored; the builders do quote the book. Push only
  when the user says so.

## Constraints

**Azure free tier F0**: 500k characters a month, which covers the whole course,
but only ~20 requests a minute. `render.py` throttles to 3.2s between calls and
backs off 15s+ on a 429. A full episode takes ~15 minutes of wall time. The
character budget is not the binding constraint; the request rate is.

**Romanian has exactly two Azure neural voices**, `ro-RO-AlinaNeural` and
`ro-RO-EmilNeural`. Emil runs words together at full speed, so he carries
`rate_scale: 0.90`. A third character borrows Alina at `pitch: +12%`.

**The cache is keyed by provider, voice, rate and pitch.** Editing one line
re-synthesises one segment. Do not delete `.cache/` casually — it costs
characters and wall time to rebuild.

## Source text quirks

The PDF used a legacy Romanian font and `pdftotext` mapped the glyphs onto
unrelated Latin-1 codepoints: `ã`→`ă`, `þ`→`ț`, `º`→`ș`, plus cedilla forms
that need normalising to comma forms. `prep_book.py` repairs ~20k characters.
Always work from `data/book_fixed.txt`, never the raw file.

Two parsers are incomplete and worth fixing before generating in bulk:

- lesson splitting finds 18 of 40 chapters (running headers are inconsistent)
- the glossary parser recovers ~85% of entries; two-column bleed loses the rest
  and occasionally assigns an entry to the wrong lesson

Because of that, take each chapter's vocabulary from the chapter's own
`VOCABULAR` block in `book_fixed.txt` and use the glossary only for glosses.

A chapter is now cut into as many episodes as its item count needs at ~6 new
items each, not one or two — a 30-item chapter is roughly five episodes. Take
the count from the chapter's own VOCABULAR block (the glossary parser's count is
unreliable; it flagged 2, 8, 9, 11, 14, 21, 27 but missed others — chapter 3 is
32 items, chapter 4 is 36). Episodes run short (10–14 min); that is intended.

**Splitting a chapter (memory-first).** Pass `part="a"`/`"b"`/`"c"`… to
`Episode` — the letter only changes the output filename (`episode_05c.json`) and
rides along in the JSON as `part`; `number` stays the lesson integer. `render.py`
and `make_feed.py` read `part` to name outputs and keep feed guids unique. Cut
along memory load first (~6 items a part), grouping items that share a grammar
point where it falls out naturally — Lecția 5's article and clothes spread
across 5A–5E rather than the old two grammar-halves. Give the concluding part
the book's synthesis text and proverb, by which point all the chapter's words
are taught. (History: Lecția 3 was split 3A/3B along grammar points under the
old coverage-first rule; those episodes are left as they are.)

## Known inconsistency

`build_episode_01.py` predates `episode_kit.py` and carries its own copy of the
helpers and checks inline. It works and is left alone deliberately. Every
builder from episode 2 onwards imports the kit — follow `build_episode_02.py`,
not episode 1, when writing a new one. Episode 1 is still useful to read for
its content and pacing.

## Status

- Episode 1 (Lecția 1, nationalities and `a fi`) — done, rendered, listened to
- Episode 2 (Lecția 2, professions, `un`/`o`, `în`/`la`, `ba da`) — script done,
  not yet rendered
- Episode 3 (Lecția 3, classroom, demonstratives, `pe`/`lângă`) — split into 3A
  and 3B; both built and rendered, 3A listened to and approved
- Episode 4 (Lecția 4, home/rooms, politeness pronouns, plurals) — split into 4A
  (rooms + `dumnealui`/`dumneaei`) and 4B (furniture + the plural); both built,
  not yet rendered
- Episode 5 (Lecția 5, clothing, definite article, adjective agreement) —
  **being re-cut memory-first** into 5A–5E (~6 items each) + recap. 5A rebuilt
  (`Unde e paltonul?` — 4 garments + `unde`/`iată` + masc. article `-ul`),
  built, awaiting render + a listen to confirm the new feel. 5B–5E and the recap
  not yet rebuilt — the old 5A/5B builders' content is the source pool.
- Recap 1–5 (`episode_05r`, Recapitulare) — old version built; to be re-cut once
  5B–5E exist so it recaps the memory-first block.
- Episodes 6–40 — not started
- Hosting and RSS — `make_feed.py` written and tested (handles A/B…E), nothing
  uploaded yet
- Spacing engine (`data/state.json` + `episode_kit.review_auto()`) — built and
  working; seeded from episodes 1–4's validated drills.

## Next

1. Render the rebuilt 05A and listen — confirm ~6 items + heavy recall actually
   sticks before re-cutting 5B–5E and the recap the same way
2. Re-cut 5B–5E + `05r` memory-first; then Lecția 6 onwards, ~6 items/episode
3. Fix the lesson splitter and glossary parser
4. (done) `state.json` spaced review; consider tuning intervals after listening
5. Optionally backfill episodes 1–4 into memory-first episodes
6. Upload `out/` to Cloudflare R2 under an unguessable path and subscribe in
   Pocket Casts

## Conventions

- Comments explain why, not what
- Content stays in plain Python lists in the builders; never hand-write the JSON
- Every build runs the checks in `episode_kit.py` and fails loudly
- Do not commit `.cache/`, `.build/` or `out/`
