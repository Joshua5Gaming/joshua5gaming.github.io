import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD_DIR = os.path.join(ROOT, "output", "old")
NEW_DIR = os.path.join(ROOT, "output", "new")

BUTTONS = """
<div style="margin-top:10px; text-align:center;">
  <button onclick="prevChapter()">⬅️ Pasal Sebelumnya</button>
  <button onclick="nextChapter()">Pasal Selanjutnya ➡️</button>
</div>
"""

SCRIPT = """
<!-- PREV/NEXT SCRIPT START -->
<script>
  function getCurrentBookAndChapter() {
    const file = (window.location.pathname.split("/").pop() || "").replace(".html","");
    const parts = file.split("_");
    const chapter = parseInt(parts.pop(), 10);
    const book = parts.join("_");
    return { book, chapter };
  }

  function prevChapter() {
    const { book, chapter } = getCurrentBookAndChapter();
    if (!book || !chapter) return;
    if (chapter > 1) {
      window.location.href = `${book}_${chapter - 1}.html`;
    }
  }

  function nextChapter() {
    const { book, chapter } = getCurrentBookAndChapter();
    if (!book || !chapter) return;
    // assume chapterCounts already exists from your dropdown script
    const max = chapterCounts[book];
    if (chapter < max) {
      window.location.href = `${book}_${chapter + 1}.html`;
    }
  }
</script>
<!-- PREV/NEXT SCRIPT END -->
"""

def process_folder(folder):
    for name in os.listdir(folder):
        if not name.lower().endswith(".html"):
            continue
        path = os.path.join(folder, name)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        # Insert buttons only once (avoid duplicates)
        if "Pasal Selanjutnya" not in html:
            # put buttons after the first </select> block (after chapter dropdown)
            html = re.sub(r"(</select>\s*)", r"\1" + BUTTONS, html, count=1)

        # Insert script before </body>, remove old if exists
        html = re.sub(r"<!-- PREV/NEXT SCRIPT START -->.*?<!-- PREV/NEXT SCRIPT END -->",
                      "", html, flags=re.DOTALL)
        html = re.sub(r"</body>", SCRIPT + "\n</body>", html, count=1, flags=re.IGNORECASE)

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Updated {name}")

def main():
    process_folder(OLD_DIR)
    process_folder(NEW_DIR)
    print("🎉 Done! Prev/Next buttons added to all files.")

if __name__ == "__main__":
    main()
