"""Read-only checks of Briefly's published site and public CORS preflight."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import sys
import time
from urllib.request import Request, urlopen
from urllib.parse import urlparse

ORIGIN = "https://brieflyletters.com"
CHECKS = {
    "/": ['<link rel="canonical" href="https://brieflyletters.com/">',
          "ca-pub-8272791832669756"],
    "/ratgeber.html": ["40 häufige Begriffe", "jobcenter-mitwirkung.html"],
    "/krankmeldung-arbeitgeber.html": ["Krankmeldung und ärztlicher Nachweis"],
    "/versicherung-schaden-melden.html": ["Eine Belegliste"],
    "/nebenkostenabrechnung-nachfragen.html": ["Eine Beispielrechnung in drei Zeilen"],
    "/robots.txt": ["Sitemap: https://brieflyletters.com/sitemap.xml"],
    "/sitemap.xml": ["https://brieflyletters.com/ratgeber.html"],
    "/ads.txt": ["google.com, pub-8272791832669756, DIRECT, f08c47fec0942fa0"],
}


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


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check_page, CHECKS.items()))
results.append(check_preflight())
for name, ok, detail in results:
    print(("PASS" if ok else "FAIL") + " " + name + ": " + detail, flush=True)
print("No sign-in, generation, account approval or regional CMP behavior was tested.")
sys.exit(0 if all(ok for _, ok, _ in results) else 1)
