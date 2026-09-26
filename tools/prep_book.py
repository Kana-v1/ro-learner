"""
Prepare 'Limba care ne unește' (nivelul I) for the podcast pipeline.

1. Repairs legacy-font diacritics mangled by pdftotext.
2. Splits the book into lessons.
3. Parses the trilingual back glossary (RO - RU - EN) into JSON keyed by lesson.

Usage: python tools/prep_book.py rom_book_parsed.txt
"""
import json, pathlib, re, sys
from collections import Counter, defaultdict

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"

# --- 1. diacritic repair -----------------------------------------------------
# The PDF used a legacy Romanian font; pdftotext mapped the glyphs onto
# unrelated Latin-1 codepoints. Also normalises cedilla forms to comma forms,
# which is the correct modern Romanian encoding.
DIACRITICS = str.maketrans({
    'ã': 'ă', 'Ã': 'Ă',   # a-tilde      -> a-breve
    'þ': 'ț', 'Þ': 'Ț',   # thorn        -> t-comma
    'º': 'ș', 'ª': 'Ș',   # ordinal sign -> s-comma
    'ţ': 'ț', 'Ţ': 'Ț',   # t-cedilla    -> t-comma
    'ş': 'ș', 'Ş': 'Ș',   # s-cedilla    -> s-comma
})

def repair(text: str) -> str:
    text = text.translate(DIACRITICS)
    text = text.replace('○', '')          # decorative bullets from section heads
    return text

def count_repairs(text: str) -> int:
    return sum(text.count(c) for c in DIACRITICS_SRC)

DIACRITICS_SRC = 'ãÃþÞºªţŢşŞ'

# --- 2. lesson splitting -----------------------------------------------------
def split_lessons(text: str) -> dict[int, str]:
    """Body text per lesson. Skips front matter and the table of contents."""
    body = text[text.find('ALFABETUL'):]
    marks = [(int(m.group(1)), m.start())
             for m in re.finditer(r'^\s*\d*\s*[A-ZĂÂÎȘȚ ,\-]{4,40}\s+LECȚIA\s+(\d+)\s*$',
                                  body, re.M)]
    first = {}
    for num, pos in marks:
        if 1 <= num <= 40:
            first.setdefault(num, pos)
    nums = sorted(first)
    out = {}
    for i, num in enumerate(nums):
        end = first[nums[i + 1]] if i + 1 < len(nums) else len(body)
        out[num] = body[first[num]:end]
    return out

# --- 3. glossary parsing -----------------------------------------------------
CYRILLIC = re.compile(r'[а-яА-ЯёЁ]')

def parse_glossary(text: str) -> list[dict]:
    """The back glossary is two-column: 'word (-pl) pos. - russian - english, N'."""
    tail = text[int(len(text) * 0.88):]
    left, right = [], []
    for line in tail.split('\n'):
        parts = [p for p in re.split(r'\s{4,}', line.rstrip()) if p.strip()]
        if not parts:
            left.append(''); right.append(''); continue
        if len(parts) == 1:
            indent = len(line) - len(line.lstrip())
            (left if indent < 40 else right).append(parts[0])
        else:
            left.append(parts[0]); right.append(' '.join(parts[1:]))
    joined = ' \n'.join(left) + '\n' + ' \n'.join(right)
    # rejoin wrapped entries: a real entry starts with a word followed by ' - '
    joined = re.sub(r'\n(?![a-zA-ZăâîșțĂÂÎȘȚ][^\n]{0,40}–)', ' ', joined)

    # two glossary entries often land on one physical line; break after each
    # trailing lesson number when a new headword follows
    joined = re.sub(r'(,\s*\d{1,2})\s+(?=[a-zA-ZăâîșțĂÂÎȘȚ][^\n]{0,45}–)', r'\1\n', joined)

    pat = re.compile(r'([^\n]{2,70}?)\s*–\s*([^–\n]{1,70}?)\s*–\s*([^\n]{1,90}?),\s*(\d{1,2})\b')
    entries, seen = [], set()
    for ro, ru, en, lesson in pat.findall(joined):
        # trim column bleed: the real headword is whatever follows the last
        # Cyrillic character or lesson number left over from a previous entry
        cut = max([m.end() for m in CYRILLIC.finditer(ro)] +
                  [m.end() for m in re.finditer(r'\d', ro)] + [0])
        ro = ro[cut:]
        ro, ru, en = ro.strip(' .,'), ru.strip(' .,'), en.strip(' .,')
        en = re.split(r',\s*\d+\s', en)[0]
        if CYRILLIC.search(ro) or not CYRILLIC.search(ru):
            continue
        if len(ro) < 2 or ro[0].isdigit():
            continue
        headword = re.sub(r'\s*\([^)]*\)\s*', ' ', ro)
        headword = re.sub(r'\s+(m|f|n|adv|I{1,3}V?|IV)\.?$', '', headword).strip()
        key = (headword.lower(), int(lesson))
        if not headword or key in seen:
            continue
        seen.add(key)
        entries.append({
            'lesson': int(lesson),
            'headword': headword,
            'citation': ro,
            'ru': ru,
            'en': en,
        })
    return sorted(entries, key=lambda e: (e['lesson'], e['headword'].lower()))

# --- main --------------------------------------------------------------------
if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'rom_book_parsed.txt'
    raw = open(src, encoding='utf-8').read()
    fixed = repair(raw)

    DATA.mkdir(exist_ok=True)
    (DATA / 'book_fixed.txt').write_text(fixed, encoding='utf-8')

    lessons = split_lessons(fixed)
    json.dump({str(k): v for k, v in lessons.items()},
              open(DATA / 'lessons.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    gloss = parse_glossary(fixed)
    by_lesson = defaultdict(list)
    for e in gloss:
        by_lesson[e['lesson']].append(e)
    json.dump({str(k): v for k, v in sorted(by_lesson.items())},
              open(DATA / 'glossary.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    changed = count_repairs(raw)
    print(f'wrote to            : {DATA}')
    print(f'diacritics repaired : {changed} characters')
    print(f'lessons split       : {len(lessons)} ({min(lessons)}–{max(lessons)})')
    print(f'glossary entries    : {len(gloss)}')
    print(f'lesson 1 vocabulary : {len(by_lesson[1])} words')
