from pathlib import Path
import re

path = Path("sitemap.xml")
text = path.read_text(encoding="utf-8")
cleaned = re.sub(
    r"\s*<url><loc>https://brieflyletters\.com/google[^<]+\.html</loc><lastmod>[^<]+</lastmod></url>",
    "",
    text,
    flags=re.I,
)
if cleaned != text:
    path.write_text(cleaned, encoding="utf-8")
    print("Removed Google verification file from sitemap")
else:
    print("Sitemap already excludes Google verification files")
