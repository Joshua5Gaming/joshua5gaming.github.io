# update_bible_nav.py
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD_DIR = os.path.join(ROOT, "output", "old")
NEW_DIR = os.path.join(ROOT, "output", "new")

# Book lists (use exact filename book tokens that your files use)
OLD_BOOKS = [
    "Kejadian","Keluaran","Imamat","Bilangan","Ulangan",
    "Yosua","Hakim-Hakim","Rut",
    "1_Samuel","2_Samuel","1_Raja-Raja","2_Raja-Raja",
    "1_Tawarikh","2_Tawarikh","Ezra","Nehemia","Ester",
    "Ayub","Mazmur","Amsal","Pengkhotbah","Kidung_Agung",
    "Yesaya","Yeremia","Ratapan","Yehezkiel","Daniel",
    "Hosea","Yoel","Amos","Obaja","Yunus","Mikha","Nahum",
    "Habakuk","Zefanya","Hagai","Zakharia","Maleakhi"
]

NEW_BOOKS = [
    "Matius","Markus","Lukas","Yohanes","Kisah_Para_Rasul",
    "Roma","1_Korintus","2_Korintus","Galatia","Efesus",
    "Filipi","Kolose","1_Tesalonika","2_Tesalonika",
    "1_Timotius","2_Timotius","Titus","Filemon","Ibrani",
    "Yakobus","1_Petrus","2_Petrus","1_Yohanes","2_Yohanes",
    "3_Yohanes","Yudas","Wahyu"
]

# Full chapter counts (keys must match filenames' book tokens)
CHAPTER_COUNTS = {
    "Kejadian": 50, "Keluaran": 40, "Imamat": 27, "Bilangan": 36, "Ulangan": 34,
    "Yosua": 24, "Hakim-Hakim": 21, "Rut": 4,
    "1_Samuel": 31, "2_Samuel": 24,
    "1_Raja-Raja": 22, "2_Raja-Raja": 25,
    "1_Tawarikh": 29, "2_Tawarikh": 36,
    "Ezra": 10, "Nehemia": 13, "Ester": 10,
    "Ayub": 42, "Mazmur": 150, "Amsal": 31, "Pengkhotbah": 12, "Kidung_Agung": 8,
    "Yesaya": 66, "Yeremia": 52, "Ratapan": 5,
    "Yehezkiel": 48, "Daniel": 12,
    "Hosea": 14, "Yoel": 3, "Amos": 9, "Obaja": 1, "Yunus": 4,
    "Mikha": 7, "Nahum": 3, "Habakuk": 3, "Zefanya": 3, "Hagai": 2,
    "Zakharia": 14, "Maleakhi": 4,

    "Matius": 28, "Markus": 16, "Lukas": 24, "Yohanes": 21,
    "Kisah_Para_Rasul": 28,
    "Roma": 16, "1_Korintus": 16, "2_Korintus": 13,
    "Galatia": 6, "Efesus": 6, "Filipi": 4, "Kolose": 4,
    "1_Tesalonika": 5, "2_Tesalonika": 3,
    "1_Timotius": 6, "2_Timotius": 4,
    "Titus": 3, "Filemon": 1,
    "Ibrani": 13, "Yakobus": 5,
    "1_Petrus": 5, "2_Petrus": 3,
    "1_Yohanes": 5, "2_Yohanes": 1, "3_Yohanes": 1,
    "Yudas": 1, "Wahyu": 22
}

NAV_START = "<!-- BIBLE NAV START -->"
NAV_END   = "<!-- BIBLE NAV END -->"
JS_START  = "<!-- BIBLE SCRIPT START -->"
JS_END    = "<!-- BIBLE SCRIPT END -->"

def book_label(book_token: str) -> str:
    # Show underscores as spaces in the UI (e.g., Kisah_Para_Rasul -> Kisah Para Rasul)
    return book_token.replace("_", " ")

def nav_html(books, is_old: bool) -> str:
    switch_href = "../new/Matius_1.html" if is_old else "../old/Kejadian_1.html"
    switch_text = "Pindah ke Perjanjian Baru" if is_old else "Pindah ke Perjanjian Lama"

    options = ['<option value="">-- Pilih Kitab --</option>']
    for b in books:
        options.append(f'<option value="{b}">{book_label(b)}</option>')
    options_html = "\n      ".join(options)

    return f"""{NAV_START}
<div id="bible-nav" style="margin:10px; text-align:center;">
  <select id="bookSelect" onchange="updateChapters()">
      {options_html}
  </select>

  <select id="chapterSelect" disabled onchange="goToChapter()">
      <option value="">-- Pilih Pasal --</option>
  </select>

  <a href="{switch_href}" style="margin-left:10px;">📖 {switch_text}</a>

  <br><br>
  <button onclick="prevChapter()">⬅️ Pasal Sebelumnya</button>
  <button onclick="nextChapter()">Pasal Selanjutnya ➡️</button>
</div>
{NAV_END}"""

def js_block() -> str:
    # One shared JS for both sections
    # - populates chapters
    # - navigates via dropdown
    # - prev/next buttons
    # - auto-select current book/pasal if applicable
    # - idempotent; safe to reinject
    # Use JSON-like literal for chapter counts
    import json
    counts_json = json.dumps(CHAPTER_COUNTS, ensure_ascii=False, indent=2)
    return f"""{JS_START}
<script>
  const chapterCounts = {counts_json};

  function updateChapters() {
    const bookSel = document.getElementById("bookSelect");
    const chapSel = document.getElementById("chapterSelect");
    if (!bookSel || !chapSel) return;

    const book = bookSel.value;
    chapSel.innerHTML = '<option value="">-- Pilih Pasal --</option>';

    if (book && chapterCounts[book]) {
      const max = chapterCounts[book];
      for (let i = 1; i <= max; i++) {
        const opt = document.createElement("option");
        opt.value = i;
        opt.textContent = i;
        chapSel.appendChild(opt);
      }
      chapSel.disabled = false;
    } else {
      chapSel.disabled = true;
    }
  }

  function goToChapter() {
    const bookSel = document.getElementById("bookSelect");
    const chapSel = document.getElementById("chapterSelect");
    if (!bookSel || !chapSel) return;

    const book = bookSel.value;
    const chapter = chapSel.value;
    if (book && chapter) {
      window.location.href = `${book}_${chapter}.html`;
    }
  }

  function getCurrentBookAndChapter() {
    const file = (window.location.pathname.split("/").pop() || "").replace(".html",""); // e.g. Kejadian_3
    if (!file) return {{ book: "", chapter: 0 }};
    const parts = file.split("_");
    const chapter = parseInt(parts.pop(), 10);
    const book = parts.join("_");
    return {{ book, chapter }};
  }

  function prevChapter() {
    const {{ book, chapter }} = getCurrentBookAndChapter();
    if (!book || !chapter) return;
    if (chapter > 1) {
      window.location.href = `${book}_${chapter - 1}.html`;
    }
  }

  function nextChapter() {
    const {{ book, chapter }} = getCurrentBookAndChapter();
    if (!book || !chapter) return;
    const max = chapterCounts[book];
    if (chapter < max) {
      window.location.href = `${book}_${chapter + 1}.html`;
    }
  }

  // Auto-select current book/chapter in dropdowns (if present in this section)
  document.addEventListener("DOMContentLoaded", () => {{
    const bookSel = document.getElementById("bookSelect");
    const chapSel = document.getElementById("chapterSelect");
    if (!bookSel || !chapSel) return;

    const {{ book, chapter }} = getCurrentBookAndChapter();
    if (!book || !chapter) return;

    // If current book is in this dropdown, preselect + populate chapters
    const opt = Array.from(bookSel.options).find(o => o.value === book);
    if (opt) {{
      bookSel.value = book;
      updateChapters();
      chapSel.value = String(chapter);
    }}
  }});
</script>
{JS_END}"""

def remove_between_markers(content: str, start_marker: str, end_marker: str) -> str:
    # Remove any existing block between markers (idempotent updates)
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL | re.IGNORECASE)
    return re.sub(pattern, "", content)

def insert_nav(content: str, nav: str) -> str:
    # Insert NAV right after <body ...>
    m = re.search(r"<body[^>]*>", content, flags=re.IGNORECASE)
    if m:
        idx = m.end()
        return content[:idx] + "\n" + nav + "\n" + content[idx:]
    # If no <body>, prepend
    return nav + "\n" + content

def insert_js(content: str, js: str) -> str:
    # Insert JS right before </body>
    m = re.search(r"</body\s*>", content, flags=re.IGNORECASE)
    if m:
        idx = m.start()
        return content[:idx] + "\n" + js + "\n" + content[idx:]
    # If no </body>, append
    return content + "\n" + js

def process_folder(folder: str, books, is_old: bool):
    if not os.path.isdir(folder):
        return
    nav = nav_html(books, is_old)
    js = js_block()
    for name in os.listdir(folder):
        if not name.lower().endswith(".html"):
            continue
        path = os.path.join(folder, name)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        # 1) Remove any previous injected blocks
        html = remove_between_markers(html, NAV_START, NAV_END)
        html = remove_between_markers(html, JS_START, JS_END)

        # 2) Insert fresh NAV and JS
        html = insert_nav(html, nav)
        html = insert_js(html, js)

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated: {path}")

def main():
    process_folder(OLD_DIR, OLD_BOOKS, is_old=True)
    process_folder(NEW_DIR, NEW_BOOKS, is_old=False)
    print("✅ All pages updated: section-specific dropdowns, switch link, and prev/next buttons.")

if __name__ == "__main__":
    main()
