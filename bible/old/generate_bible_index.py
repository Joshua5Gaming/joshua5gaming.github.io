import os
import re

# Path to your output folder
output_dir = "E:/Documents/A1 - My Stuff/joshua5gaming.github.io/output"

# Regex to capture book name and chapter number from file name
pattern = re.compile(r"^(.*?)-(\d+)\.html$")

# Bible order (Indonesian version)
bible_order = [
    "Kejadian", "Keluaran", "Imamat", "Bilangan", "Ulangan",
    "Yosua", "Hakim-hakim", "Rut",
    "1 Samuel", "2 Samuel", "1 Raja-raja", "2 Raja-raja",
    "1 Tawarikh", "2 Tawarikh", "Ezra", "Nehemia", "Ester",
    "Ayub", "Mazmur", "Amsal", "Pengkhotbah", "Kidung Agung",
    "Yesaya", "Yeremia", "Ratapan", "Yehezkiel", "Daniel",
    "Hosea", "Yoel", "Amos", "Obaja", "Yunus", "Mikha", "Nahum",
    "Habakuk", "Zefanya", "Hagai", "Zakharia", "Maleakhi",
    "Matius", "Markus", "Lukas", "Yohanes", "Kisah Para Rasul",
    "Roma", "1 Korintus", "2 Korintus", "Galatia", "Efesus",
    "Filipi", "Kolose", "1 Tesalonika", "2 Tesalonika",
    "1 Timotius", "2 Timotius", "Titus", "Filemon", "Ibrani",
    "Yakobus", "1 Petrus", "2 Petrus", "1 Yohanes", "2 Yohanes",
    "3 Yohanes", "Yudas", "Wahyu"
]

# Dictionary: book name -> list of chapter numbers
books = {}

# Scan output folder for HTML files
for filename in os.listdir(output_dir):
    match = pattern.match(filename)
    if match:
        book, chapter = match.groups()
        chapter = int(chapter)
        books.setdefault(book, []).append(chapter)

# Sort chapters for each book
for book in books:
    books[book].sort()

# Create HTML index content
html_content = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alkitab Indonesia</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f9f9f9;
        }
        h1 {
            text-align: center;
        }
        details {
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
            box-shadow: 0 0 3px rgba(0,0,0,0.1);
        }
        summary {
            font-weight: bold;
            cursor: pointer;
        }
        a {
            text-decoration: none;
            color: #007BFF;
        }
        a:hover {
            text-decoration: underline;
        }
        ul {
            margin: 5px 0 0 20px;
            padding: 0;
            list-style: none;
        }
    </style>
</head>
<body>
    <h1>Daftar Kitab - Alkitab Indonesia</h1>
"""

# Add dropdowns for each book in Bible order
for book in bible_order:
    if book in books:
        html_content += f"    <details>\n"
        html_content += f"        <summary>{book}</summary>\n"
        html_content += f"        <ul>\n"
        for chapter in books[book]:
            html_content += f'            <li><a href="{book}-{chapter}.html">{book} {chapter}</a></li>\n'
        html_content += f"        </ul>\n"
        html_content += f"    </details>\n\n"

# Close HTML
html_content += "</body>\n</html>"

# Save to index.html inside output folder
index_path = os.path.join(output_dir, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ index.html generated at {index_path}")
