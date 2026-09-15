"""Read-only checks of Briefly source, published site and public CORS preflight."""
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import time
from urllib.request import Request, urlopen
from urllib.parse import urlparse

ORIGIN = "https://brieflyletters.com"
OLD_ORIGIN = "nadiiahonda34-svg.github.io"
LEGACY_NOINDEX = {"brief-an-jobcenter-behoerde.html", "brief-an-vermieter.html", "404.html"}
CHECKS = {
    "/": ['<link rel="canonical" href="https://brieflyletters.com/">',
          "ca-pub-8272791832669756"],
    "/ratgeber.html": ["40 häufige Begriffe", "jobcenter-mitwirkung.html"],
    "/wege.html": ["Vom schwierigen Schreiben zur geprüften Antwort"],
    "/krankmeldung-arbeitgeber.html": ["Krankmeldung und ärztlicher Nachweis"],
    "/versicherung-schaden-melden.html": ["Eine Belegliste"],
    "/nebenkostenabrechnung-nachfragen.html": ["Eine Beispielrechnung in drei Zeilen"],
    "/robots.txt": ["Sitemap: https://brieflyletters.com/sitemap.xml"],
    "/sitemap.xml": ["https://brieflyletters.com/ratgeber.html", "https://brieflyletters.com/wege.html"],
    "/ads.txt": ["google.com, pub-8272791832669756, DIRECT, f08c47fec0942fa0"],
}


class HeadAndLinksParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title_parts = []
        self.description = ""
        self.robots = ""
        self.canonical = ""
        self.links = []

    @property
    def title(self):
        return "".join(self.title_parts).strip()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = attrs.get("name", "").lower()
            if name == "description":
                self.description = attrs.get("content", "").strip()
            elif name == "robots":
                self.robots = attrs.get("content", "").strip().lower()
        elif tag == "link":
            rel = attrs.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonical = attrs.get("href", "").strip()
        elif tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"].strip())

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)


def check_source_seo():
    sitemap = Path("sitemap.xml").read_text(encoding="utf-8")
    urls = re.findall(r"<loc>(https://brieflyletters\.com/[^<]*)</loc>", sitemap)
    expected_files = []
    for url in urls:
        path = urlparse(url).path.lstrip("/") or "index.html"
        expected_files.append((url, path))

    errors = []
    titles = defaultdict(list)
    descriptions = defaultdict(list)
    repo_files = {str(p.as_posix()) for p in Path(".").rglob("*") if p.is_file()}

    for url, path in expected_files:
        file_path = Path(path)
        if not file_path.is_file():
            errors.append(f"sitemap target missing: {path}")
            continue
        parser = HeadAndLinksParser()
        parser.feed(file_path.read_text(encoding="utf-8"))
        if not parser.title:
            errors.append(f"missing title: {path}")
        else:
            titles[parser.title].append(path)
        if not parser.description:
            errors.append(f"missing description: {path}")
        else:
            descriptions[parser.description].append(path)
        if parser.canonical != url:
            errors.append(f"canonical mismatch: {path} -> {parser.canonical or 'missing'}")
        if "noindex" in parser.robots:
            errors.append(f"noindex page present in sitemap: {path}")

        for href in parser.links:
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue
            parsed = urlparse(href)
            if parsed.scheme in ("http", "https"):
                continue
            target = parsed.path.lstrip("/")
            if not target:
                target = "index.html"
            if target.endswith("/"):
                target += "index.html"
            if target not in repo_files:
                errors.append(f"broken internal link: {path} -> {href}")

    for title, pages in titles.items():
        if len(pages) > 1:
            errors.append("duplicate title: " + " | ".join(pages))
    for description, pages in descriptions.items():
        if len(pages) > 1:
            errors.append("duplicate description: " + " | ".join(pages))

    for legacy in LEGACY_NOINDEX:
        parser = HeadAndLinksParser()
        parser.feed(Path(legacy).read_text(encoding="utf-8"))
        if "noindex" not in parser.robots:
            errors.append(f"legacy page is not noindex: {legacy}")
        if any(path == legacy for _, path in expected_files):
            errors.append(f"legacy page unexpectedly present in sitemap: {legacy}")

    text_suffixes = {".html", ".js", ".css", ".xml", ".txt"}
    for file_path in Path(".").rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in text_suffixes:
            text = file_path.read_text(encoding="utf-8", errors="replace")
            if OLD_ORIGIN in text:
                errors.append(f"old github.io reference: {file_path.as_posix()}")

    if errors:
        return "Source SEO/link audit", False, "; ".join(errors)
    return ("Source SEO/link audit", True,
            f"{len(expected_files)} sitemap pages: unique title/description, canonical, noindex and internal links OK")


def check_page(item):
    path, markers = item
    error = None
    for attempt in range(3):
        try:
            request = Request(ORIGIN + path, headers={"User-Agent": "BrieflySiteCheck/1.0"})
            with urlopen(request, timeout=20) as response:
                final = urlparse(response.url)
                if response.status != 200:
                    raise ValueError("unexpected HTTP status")
                if final.scheme != "https" or final.netloc != "brieflyletters.com":
                    raise ValueError("unexpected final origin: " + final.netloc)
                body = response.read(2000000).decode("utf-8")
            if not all(marker in body for marker in markers):
                raise ValueError("expected published content not found")
            return path, True, "HTTPS and expected content OK"
        except Exception as exc:
            error = str(exc)
            if attempt < 2:
                time.sleep(5)
    return path, False, error


def check_preflight():
    source = Path("index.html").read_text(encoding="utf-8")
    match = re.search(r'const WORKER_URL="(https://[^"]+)"', source)
    if not match:
        return "Backend preflight", False, "backend URL missing from source"
    request = Request(match.group(1), method="OPTIONS", headers={
        "Origin": ORIGIN,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "authorization,content-type",
        "User-Agent": "BrieflySiteCheck/1.0",
    })
    try:
        with urlopen(request, timeout=20) as response:
            headers = response.headers
            if not 200 <= response.status < 300:
                raise ValueError("preflight did not return a successful status")
            if headers.get("Access-Control-Allow-Origin") not in (ORIGIN, "*"):
                raise ValueError("production origin not allowed")
            allowed = {value.strip().lower() for value in
                       headers.get("Access-Control-Allow-Headers", "").split(",")}
            if "authorization" not in allowed or not ({"content-type", "*"} & allowed):
                raise ValueError("Authorization or Content-Type header not allowed")
            methods = headers.get("Access-Control-Allow-Methods", "").upper()
            if methods and "POST" not in methods and "*" not in methods:
                raise ValueError("POST is not an allowed method")
        return "Backend preflight", True, "production origin and request headers OK"
    except Exception as exc:
        return "Backend preflight", False, str(exc)


results = [check_source_seo()]
with ThreadPoolExecutor(max_workers=4) as pool:
    results.extend(pool.map(check_page, CHECKS.items()))
results.append(check_preflight())
for name, ok, detail in results:
    print(("PASS" if ok else "FAIL") + " " + name + ": " + detail, flush=True)
print("No sign-in, generation, account approval or regional CMP behavior was tested.")
sys.exit(0 if all(ok for _, ok, _ in results) else 1)
