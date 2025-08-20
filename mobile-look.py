import os

folders = ["bible/old", "bible/new"]

custom_css = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
  font-family: Arial, sans-serif;
  background: #f3f3f3;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
}
.container {
  background: white;
  max-width: 600px;
  width: 100%;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
h1 {
  text-align: center;
  font-size: 1.6rem;
  margin: 15px 0;
}
.menu {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}
.menu select, .menu button, .menu a {
  font-size: 1.1rem;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #666;
  background: #f5f5f5;
  cursor: pointer;
}
.menu button:hover {
  background: #e0e0e0;
}
.menu a {
  text-decoration: none;
  background: #eee;
}
</style>
"""

for folder in folders:
    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            path = os.path.join(folder, filename)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # Add CSS into <head>
            if "viewport" not in content:
                content = content.replace("</head>", custom_css + "\n</head>")

            # Wrap body in .container
            if '<div class="container">' not in content:
                content = content.replace("<body>", "<body>\n<div class=\"container\">")
                content = content.replace("</body>", "</div>\n</body>")

            # Turn inline-styled nav into .menu wrapper
            if "id=\"bookSelect\"" in content and "class=\"menu\"" not in content:
                content = content.replace('style="margin: 10px; text-align: center;"', 'class="menu"')
                content = content.replace('style="margin-top:10px; text-align:center;"', '')

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"✅ Updated: {path}")
