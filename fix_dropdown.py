import os

# Define Old and New Testament books
old_books = [
    "Kejadian","Keluaran","Imamat","Bilangan","Ulangan",
    "Yosua","Hakim-Hakim","Rut","1_Samuel","2_Samuel",
    "1_Raja-Raja","2_Raja-Raja","1_Tawarikh","2_Tawarikh",
    "Ezra","Nehemia","Ester","Ayub","Mazmur","Amsal",
    "Pengkhotbah","Kidung_Agung","Yesaya","Yeremia",
    "Ratapan","Yehezkiel","Daniel","Hosea","Yoel","Amos",
    "Obaja","Yunus","Mikha","Nahum","Habakuk","Zefanya",
    "Hagai","Zakharia","Maleakhi"
]

new_books = [
    "Matius","Markus","Lukas","Yohanes","Kisah_Para_Rasul",
    "Roma","1_Korintus","2_Korintus","Galatia","Efesus",
    "Filipi","Kolose","1_Tesalonika","2_Tesalonika",
    "1_Timotius","2_Timotius","Titus","Filemon","Ibrani",
    "Yakobus","1_Petrus","2_Petrus","1_Yohanes","2_Yohanes",
    "3_Yohanes","Yudas","Wahyu"
]

def make_dropdown(books, switch_link, switch_text):
    """Generate dropdown HTML with a switch link"""
    html = ['<div style="margin: 10px; text-align: center;">']
    html.append('<select id="bookSelect" onchange="updateChapters()">')
    html.append('<option value="">-- Pilih Kitab --</option>')
    for book in books:
        html.append(f'<option value="{book}">{book.replace("_"," ")}</option>')
    html.append('</select>')

    html.append('<select id="chapterSelect" disabled onchange="goToChapter()">')
    html.append('<option value="">-- Pilih Pasal --</option>')
    html.append('</select>')

    html.append(f'<a href="{switch_link}" style="margin-left:10px;">📖 {switch_text}</a>')
    html.append('</div>')
    return "\n".join(html)

def fix_files(folder, books, switch_link, switch_text):
    for fname in os.listdir(folder):
        if not fname.endswith(".html"):
            continue
        path = os.path.join(folder, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace old dropdown (assume first <div>..</div> block with select)
        start = content.find("<div")
        end = content.find("</div>", start) + 6
        if start != -1 and end != -1:
            new_dropdown = make_dropdown(books, switch_link, switch_text)
            content = content[:start] + new_dropdown + content[end:]

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

# Fix Old Testament
fix_files("output/old", old_books, "../new/Matius_1.html", "Pindah ke Perjanjian Baru")

# Fix New Testament
fix_files("output/new", new_books, "../old/Kejadian_1.html", "Pindah ke Perjanjian Lama")

print("✅ Dropdowns updated for all OT and NT files!")
