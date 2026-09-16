from pathlib import Path
import re

MARKER = "<!-- topic-cluster-2026 -->"
HUB_MARKER = "<!-- topic-hubs-2026 -->"

CLUSTERS = {
    "Jobcenter": [
        ("jobcenter-briefe-verstehen.html", "Jobcenter-Briefe im Überblick"),
        ("jobcenter-bescheid-verstehen.html", "Jobcenter-Bescheid verstehen"),
        ("jobcenter-anhoerung-verstehen.html", "Anhörung verstehen"),
        ("jobcenter-mitwirkung.html", "Mitwirkungsaufforderung verstehen"),
        ("jobcenter-termin-verschieben.html", "Jobcenter-Termin verschieben"),
        ("widerspruch-brief-struktur.html", "Widerspruch strukturieren"),
    ],
    "Behörden": [
        ("behoerdenbriefe-verstehen.html", "Behördenbriefe verstehen"),
        ("termin-behoerde-verschieben.html", "Behördentermin verschieben"),
        ("auslaenderbehoerde-termin-anfragen.html", "Termin bei der Ausländerbehörde"),
        ("familienkasse-kindergeld-brief-verstehen.html", "Familienkasse & Kindergeld"),
        ("finanzamt-brief-verstehen.html", "Brief vom Finanzamt verstehen"),
        ("krankenkasse-brief-verstehen.html", "Brief der Krankenkasse verstehen"),
        ("unterlagen-nachreichen.html", "Unterlagen nachreichen"),
        ("fristverlaengerung-beantragen.html", "Fristverlängerung beantragen"),
    ],
    "Wohnen": [
        ("vermieter-brief-verstehen.html", "Brief vom Vermieter verstehen"),
        ("mietmangel-melden.html", "Mietmangel melden"),
        ("nebenkostenabrechnung-nachfragen.html", "Nebenkostenabrechnung nachfragen"),
        ("kuendigung-mietvertrag-bestaetigung.html", "Kündigung bestätigen lassen"),
    ],
    "Arbeit": [
        ("arbeitsbescheinigung-anfordern.html", "Arbeitsbescheinigung anfordern"),
        ("krankmeldung-arbeitgeber.html", "Krankmeldung an Arbeitgeber"),
        ("schicht-tauschen-anfrage.html", "Schichttausch anfragen"),
        ("formelle-antwort-deutsch.html", "Formell auf Deutsch antworten"),
    ],
}

STYLE = """
<style id="briefly-topic-cluster-style">
.topic-cluster{margin-top:34px;padding:24px;border:1px solid var(--line,#e5e7eb);border-radius:18px;background:linear-gradient(135deg,#fff,#f7f6ff)}
.topic-cluster h2{margin-top:0}.topic-cluster p{margin-bottom:14px}
.topic-cluster-links{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.topic-cluster-links a{display:block;padding:12px 14px;border:1px solid var(--line,#e5e7eb);border-radius:12px;background:#fff;color:var(--accent,#5b55e7);text-decoration:none;font-weight:700;line-height:1.35}
.topic-cluster-links a:hover{text-decoration:underline}
@media(max-width:620px){.topic-cluster-links{grid-template-columns:1fr}}
</style>
"""

changed = []

for cluster_name, items in CLUSTERS.items():
    existing = [(href, label) for href, label in items if Path(href).exists()]
    for current, _ in existing:
        path = Path(current)
        text = path.read_text(encoding="utf-8")
        if MARKER in text or "</main>" not in text:
            continue
        links = [(href, label) for href, label in existing if href != current][:6]
        if not links:
            continue
        block = (
            f'\n{MARKER}\n<section class="topic-cluster" aria-label="Weitere Ratgeber zum Thema {cluster_name}">'
            f'<h2>Mehr zum Thema {cluster_name}</h2>'
            f'<p>Diese Ratgeber gehören zum selben Themenbereich und helfen Ihnen, den nächsten passenden Schritt zu finden.</p>'
            f'<div class="topic-cluster-links">'
            + "".join(f'<a href="{href}">{label} →</a>' for href, label in links)
            + '</div></section>\n'
        )
        if 'id="briefly-topic-cluster-style"' not in text:
            text = text.replace("</head>", STYLE + "</head>", 1)
        text = text.replace("</main>", block + "</main>", 1)
        path.write_text(text, encoding="utf-8")
        changed.append(current)
        print(f"Cluster links added: {current}")

# Strengthen the central Ratgeber page with four visible topic hubs.
ratgeber = Path("ratgeber.html")
if ratgeber.exists():
    text = ratgeber.read_text(encoding="utf-8")
    original = text
    if HUB_MARKER not in text:
        hub_style = """
<style id="briefly-topic-hubs-style">
.topic-hubs{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:0 auto 26px}
.topic-hub{padding:18px;background:rgba(255,255,255,.9);border:1px solid #fff;border-radius:18px;box-shadow:0 10px 30px rgba(15,23,42,.05)}
.topic-hub h2{font-size:18px;margin:0 0 9px}.topic-hub a{display:block;color:var(--accent);text-decoration:none;font-size:14px;font-weight:720;margin-top:7px}.topic-hub a:hover{text-decoration:underline}
@media(max-width:900px){.topic-hubs{grid-template-columns:1fr 1fr}}@media(max-width:620px){.topic-hubs{grid-template-columns:1fr}}
</style>
"""
        if 'id="briefly-topic-hubs-style"' not in text:
            text = text.replace("</head>", hub_style + "</head>", 1)
        hubs = f'''\n{HUB_MARKER}\n<section class="topic-hubs" aria-label="Beliebte Themenbereiche">
<div class="topic-hub"><h2>Jobcenter</h2><a href="jobcenter-bescheid-verstehen.html">Bescheid verstehen →</a><a href="jobcenter-anhoerung-verstehen.html">Anhörung verstehen →</a><a href="jobcenter-termin-verschieben.html">Termin verschieben →</a></div>
<div class="topic-hub"><h2>Behörden</h2><a href="behoerdenbriefe-verstehen.html">Behördenbrief verstehen →</a><a href="unterlagen-nachreichen.html">Unterlagen nachreichen →</a><a href="fristverlaengerung-beantragen.html">Frist verlängern →</a></div>
<div class="topic-hub"><h2>Wohnen</h2><a href="vermieter-brief-verstehen.html">Vermieterbrief verstehen →</a><a href="mietmangel-melden.html">Mietmangel melden →</a><a href="nebenkostenabrechnung-nachfragen.html">Nebenkosten klären →</a></div>
<div class="topic-hub"><h2>Arbeit</h2><a href="arbeitsbescheinigung-anfordern.html">Arbeitsbescheinigung →</a><a href="krankmeldung-arbeitgeber.html">Krankmeldung →</a><a href="schicht-tauschen-anfrage.html">Schichttausch →</a></div>
</section>\n'''
        anchor = '<section class="tools"'
        if anchor in text:
            text = text.replace(anchor, hubs + anchor, 1)

    # Keep the visible catalogue count in sync with the actual number of guide cards.
    card_count = len(re.findall(r'<a class="card"\b', text))
    if card_count:
        text = re.sub(r'(<span id="count">)\d+ Ratgeber(</span>)', rf'\g<1>{card_count} Ratgeber\2', text, count=1)

    if text != original:
        ratgeber.write_text(text, encoding="utf-8")
        changed.append("ratgeber.html")
        print(f"Ratgeber hubs/count updated ({card_count} cards)")

print(f"Updated {len(changed)} files")
