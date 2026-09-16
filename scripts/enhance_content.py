from pathlib import Path
import re

BASE = "https://brieflyletters.com"
TODAY = "2026-09-16"
MARKER = "<!-- seo-depth-2026 -->"

BLOCKS = {
    "jobcenter-briefe-verstehen.html": """
<!-- seo-depth-2026 -->
<section>
<h2>Was bedeutet der Brief für Sie?</h2>
<p>Ordnen Sie das Schreiben zuerst ein: Ist es ein Bescheid, eine Anhörung, eine Mitwirkungsaufforderung oder nur eine Information? Erst danach lässt sich entscheiden, ob Sie etwas prüfen, Unterlagen nachreichen, eine Rückfrage stellen oder eine fristgebundene Reaktion vorbereiten sollten.</p>
<h2>Was sollten Sie jetzt tun?</h2>
<ol><li>Absender, Datum und Aktenzeichen notieren.</li><li>Jede genannte Frist markieren.</li><li>Den konkreten Auftrag in einem Satz zusammenfassen.</li><li>Nur die dafür nötigen Unterlagen zusammensuchen.</li><li>Antwort und Anlagen vor dem Versand noch einmal mit dem Original vergleichen.</li></ol>
<h2>Häufige Fehler</h2>
<ul><li>Eine Anhörung mit einem Bescheid verwechseln.</li><li>Eine Bitte um Erklärung bereits als Widerspruch behandeln.</li><li>Mehr persönliche Daten mitsenden als notwendig.</li><li>Fristen nur aus dem Gedächtnis übernehmen statt sie im Schreiben zu prüfen.</li></ul>
<h2>Passende nächste Schritte</h2>
<p>Bei einer Anhörung hilft der Ratgeber <a href="jobcenter-anhoerung-verstehen.html">Anhörung vom Jobcenter verstehen</a>. Bei angeforderten Unterlagen lesen Sie <a href="jobcenter-mitwirkung.html">Mitwirkungsaufforderung verstehen</a>. Für den Aufbau einer formellen Einwendung finden Sie Hinweise unter <a href="widerspruch-brief-struktur.html">Widerspruch sachlich strukturieren</a>.</p>
</section>
""",
    "jobcenter-anhoerung-verstehen.html": """
<!-- seo-depth-2026 -->
<section>
<h2>Was bedeutet eine Anhörung?</h2>
<p>Eine Anhörung gibt Ihnen Gelegenheit, zu einem im Schreiben genannten Sachverhalt Stellung zu nehmen, bevor die Behörde die Angelegenheit weiterbearbeitet. Konzentrieren Sie sich deshalb auf die konkreten Punkte, die im Brief genannt werden, und trennen Sie Tatsachen von Vermutungen.</p>
<h2>Was sollten Sie jetzt tun?</h2>
<ol><li>Lesen Sie den beschriebenen Sachverhalt vollständig.</li><li>Markieren Sie die Antwortfrist.</li><li>Prüfen Sie, welche Aussage Sie bestätigen, korrigieren oder ergänzen können.</li><li>Nennen Sie nur Nachweise, die zu diesem Punkt gehören.</li><li>Formulieren Sie kurz, sachlich und nachvollziehbar.</li></ol>
<h2>Häufige Fehler</h2>
<ul><li>Auf Punkte antworten, die gar nicht gefragt wurden.</li><li>Ungeprüfte Daten oder Beträge übernehmen.</li><li>Eine lange Lebensgeschichte statt einer klaren Stellungnahme schreiben.</li><li>Eine Anlage erwähnen, die tatsächlich nicht beigefügt ist.</li></ul>
<h2>Danach weiter</h2>
<p>Wenn gleichzeitig Unterlagen verlangt werden, hilft <a href="jobcenter-mitwirkung.html">Mitwirkungsaufforderung verstehen</a>. Einen allgemeinen Überblick finden Sie unter <a href="jobcenter-briefe-verstehen.html">Jobcenter-Briefe verstehen</a>. Zum Formulieren können Sie anschließend den <a href="index.html#top">Briefly-Generator</a> verwenden.</p>
</section>
""",
    "jobcenter-mitwirkung.html": """
<!-- seo-depth-2026 -->
<section>
<h2>Was bedeutet die Mitwirkungsaufforderung?</h2>
<p>Bei einer Mitwirkungsaufforderung geht es in der Regel um konkrete Angaben oder Unterlagen. Entscheidend ist nicht, möglichst viel zu senden, sondern genau zu prüfen, was im Schreiben verlangt wird und bis wann es vorliegen soll.</p>
<h2>Was sollten Sie jetzt tun?</h2>
<ol><li>Erstellen Sie eine Liste aller verlangten Unterlagen.</li><li>Markieren Sie, was vorhanden, bereits versendet oder noch ausstehend ist.</li><li>Ordnen Sie jedes Dokument eindeutig zu.</li><li>Wenn etwas fehlt, erklären Sie knapp, was noch aussteht.</li><li>Bewahren Sie eine Kopie Ihrer Nachricht und der Anlagen auf.</li></ol>
<h2>Häufige Fehler</h2>
<ul><li>Unvollständige Unterlagen als vollständig bezeichnen.</li><li>Dateien ohne kurze Zuordnung versenden.</li><li>Eine Fristverlängerung voraussetzen, ohne darum zu bitten.</li><li>Irrelevante sensible Dokumente mitsenden.</li></ul>
<h2>Passende Hilfen</h2>
<p>Für ein Begleitschreiben nutzen Sie <a href="unterlagen-nachreichen.html">Unterlagen nachreichen</a>. Wenn Sie mehr Zeit benötigen, lesen Sie <a href="fristverlaengerung-beantragen.html">Fristverlängerung beantragen</a>. Den Zusammenhang mit anderen Schreiben erklärt <a href="jobcenter-briefe-verstehen.html">Jobcenter-Briefe verstehen</a>.</p>
</section>
""",
    "widerspruch-brief-struktur.html": """
<!-- seo-depth-2026 -->
<section>
<h2>Was gehört in einen klaren Widerspruch?</h2>
<p>Ein gut strukturierter Text macht eindeutig, auf welchen Bescheid Sie sich beziehen und welche Entscheidung oder welcher Punkt überprüft werden soll. Die konkrete Rechtslage und die geltende Frist ergeben sich aus Ihrem Bescheid; Briefly hilft hier bei Sprache und Aufbau, nicht bei der rechtlichen Bewertung.</p>
<h2>Praktischer Aufbau</h2>
<ol><li>Bescheid mit Datum und Aktenzeichen nennen.</li><li>Klar schreiben, dass sich Ihr Schreiben auf diesen Bescheid bezieht.</li><li>Den strittigen Punkt konkret benennen.</li><li>Fakten und vorhandene Nachweise geordnet aufführen.</li><li>Um Prüfung und schriftliche Rückmeldung bitten.</li></ol>
<h2>Häufige Fehler</h2>
<ul><li>Keinen konkreten Bescheid nennen.</li><li>Mehrere unterschiedliche Anliegen in einem unübersichtlichen Text vermischen.</li><li>Behauptungen aufstellen, die sich nicht aus eigenen Unterlagen belegen lassen.</li><li>Fristen oder Rechtsfolgen aus allgemeinen Internetbeispielen übernehmen.</li></ul>
<h2>Vor dem Versand prüfen</h2>
<p>Lesen Sie zuerst <a href="jobcenter-briefe-verstehen.html">Jobcenter-Briefe verstehen</a> oder <a href="behoerdenbriefe-verstehen.html">Behördenbriefe richtig lesen</a>. Wenn der Text fertig ist, hilft die <a href="brief-checkliste.html">Brief-Checkliste</a> bei der Schlusskontrolle.</p>
</section>
""",
    "vermieter-brief-verstehen.html": """
<!-- seo-depth-2026 -->
<section>
<h2>Was bedeutet der Brief vom Vermieter?</h2>
<p>Prüfen Sie zuerst, worum es tatsächlich geht: Zahlung, Nebenkosten, Reparatur, Termin, Vertragsänderung oder Kündigung. Markieren Sie anschließend Beträge, Zeiträume, Fristen und die konkrete Bitte oder Forderung.</p>
<h2>Was sollten Sie jetzt tun?</h2>
<ol><li>Betreff und Datum prüfen.</li><li>Beträge mit Mietvertrag, Abrechnung oder eigenen Zahlungen vergleichen.</li><li>Bei einem Mangel Zustand, Ort und Zeitpunkt dokumentieren.</li><li>Nur den unklaren oder strittigen Punkt ansprechen.</li><li>Eine klare Antwort oder Rückfrage formulieren.</li></ol>
<h2>Häufige Fehler</h2>
<ul><li>Auf eine Nebenkostenfrage mit einem allgemeinen Beschwerdebrief reagieren.</li><li>Einen Mangel nur mit „kaputt“ beschreiben.</li><li>Termine und Beträge ohne Vergleich mit den eigenen Unterlagen übernehmen.</li><li>Mehrere Probleme ohne klare Reihenfolge vermischen.</li></ul>
<h2>Passende Ratgeber</h2>
<p>Bei Reparaturen hilft <a href="mietmangel-melden.html">Mietmangel melden</a>. Bei einer unklaren Abrechnung lesen Sie <a href="nebenkostenabrechnung-nachfragen.html">Nebenkostenabrechnung nachfragen</a>. Nach einer Kündigung finden Sie Hinweise unter <a href="kuendigung-mietvertrag-bestaetigung.html">Kündigung bestätigen lassen</a>.</p>
</section>
""",
    "mietmangel-melden.html": """
<!-- seo-depth-2026 -->
<section>
<h2>Wie beschreiben Sie einen Mietmangel klar?</h2>
<p>Eine verständliche Meldung beantwortet vier Fragen: Was ist defekt? Wo befindet sich der Mangel? Seit wann besteht er? Welche konkrete Reaktion wünschen Sie vom Vermieter? Bleiben Sie bei beobachtbaren Tatsachen.</p>
<h2>Was sollten Sie in die Nachricht aufnehmen?</h2>
<ol><li>Wohnung oder betroffenen Raum nennen.</li><li>Mangel möglichst konkret beschreiben.</li><li>Datum oder Zeitraum angeben, soweit bekannt.</li><li>Bereits erfolgte Kontaktversuche erwähnen, wenn sie relevant sind.</li><li>Um Reparatur, Termin oder Rückmeldung bitten.</li></ol>
<h2>Häufige Fehler</h2>
<ul><li>Nur „Heizung kaputt“ oder „Schimmel“ ohne nähere Angaben schreiben.</li><li>Unklare Forderungen ohne gewünschte nächste Handlung.</li><li>Fotos erwähnen, aber nicht beifügen.</li><li>Vermutete Ursachen als sichere Tatsachen darstellen.</li></ul>
<h2>Danach weiter</h2>
<p>Weitere typische Vermieterschreiben erklärt <a href="vermieter-brief-verstehen.html">Briefe vom Vermieter verstehen</a>. Für eine allgemeine sachliche Beschwerde nutzen Sie <a href="beschwerde-schreiben.html">Beschwerde auf Deutsch</a>. Eine Antwort können Sie anschließend mit <a href="index.html#top">Briefly</a> vorbereiten.</p>
</section>
""",
    "termin-behoerde-verschieben.html": """
<!-- seo-depth-2026 -->
<section>
<h2>Welche Angaben braucht eine Terminanfrage?</h2>
<p>Damit eine Behörde Ihre Nachricht schnell zuordnen kann, sollten Termin, Anliegen und vorhandenes Aktenzeichen klar genannt sein. Wenn Sie einen Ersatztermin vorschlagen, nennen Sie nur Zeiten, die Sie tatsächlich wahrnehmen können.</p>
<h2>Was sollten Sie schreiben?</h2>
<ol><li>Den bestehenden Termin mit Datum und Uhrzeit nennen.</li><li>Kurz mitteilen, dass Sie ihn nicht wahrnehmen können.</li><li>Falls nötig einen knappen Grund nennen, ohne unnötige persönliche Details.</li><li>Um einen neuen Termin bitten oder passende Zeitfenster nennen.</li><li>Aktenzeichen oder Kundennummer ergänzen, wenn vorhanden.</li></ol>
<h2>Häufige Fehler</h2>
<ul><li>Nur „Ich kann nicht kommen“ ohne Bezug auf den Termin schreiben.</li><li>Mehrere alternative Termine anbieten, die nicht sicher verfügbar sind.</li><li>Eine Bestätigung voraussetzen, bevor sie tatsächlich vorliegt.</li><li>Aktenzeichen oder Namen vergessen, obwohl sie für die Zuordnung nötig sind.</li></ul>
<h2>Passende Hilfen</h2>
<p>Für die Ausländerbehörde gibt es <a href="auslaenderbehoerde-termin-anfragen.html">Termin bei der Ausländerbehörde anfragen</a>. Allgemeine Behördenpost erklärt <a href="behoerdenbriefe-verstehen.html">Behördenbriefe richtig lesen</a>. Muss zusätzlich eine Frist verlängert werden, hilft <a href="fristverlaengerung-beantragen.html">Fristverlängerung beantragen</a>.</p>
</section>
""",
    "arbeitsbescheinigung-anfordern.html": """
<!-- seo-depth-2026 -->
<section>
<h2>Wie fordern Sie eine Arbeitsbescheinigung klar an?</h2>
<p>Nennen Sie möglichst genau, welches Dokument Sie benötigen und wofür eine eindeutige Zuordnung nötig ist. Eine kurze, präzise Anfrage ist für den Arbeitgeber meist hilfreicher als eine lange Erklärung.</p>
<h2>Was gehört in die Anfrage?</h2>
<ol><li>Gewünschtes Dokument eindeutig benennen.</li><li>Falls relevant den benötigten Zeitraum nennen.</li><li>Um Zusendung oder Bereitstellung bitten.</li><li>Eine realistische Rückmeldefrist nur nennen, wenn sie für Ihren Vorgang wichtig ist.</li><li>Kontaktdaten oder Personalnummer ergänzen, wenn sie die Zuordnung erleichtern.</li></ol>
<h2>Häufige Fehler</h2>
<ul><li>Nur „Ich brauche eine Bescheinigung“ schreiben.</li><li>Mehrere unterschiedliche Dokumente unter demselben Begriff zusammenfassen.</li><li>Unnötige persönliche Hintergründe schildern.</li><li>Ein gewünschtes Datum als bereits zugesagt darstellen.</li></ul>
<h2>Nächster Schritt</h2>
<p>Für eine allgemeine formelle Nachricht hilft <a href="formelle-antwort-deutsch.html">Formell auf Deutsch antworten</a>. Vor dem Versand können Sie die <a href="brief-checkliste.html">Brief-Checkliste</a> verwenden oder den Text mit dem <a href="index.html#top">Briefly-Generator</a> vorbereiten.</p>
</section>
""",
}

changed = []
for name, block in BLOCKS.items():
    path = Path(name)
    if not path.exists():
        print(f"Missing: {name}")
        continue
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"Already enhanced: {name}")
        continue
    if "</main>" not in text:
        print(f"No </main> marker: {name}")
        continue
    text = text.replace("</main>", block.strip() + "\n</main>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(name)
    print(f"Enhanced: {name}")

if changed:
    sitemap = Path("sitemap.xml")
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        for name in changed:
            pattern = rf"(<loc>{re.escape(BASE + '/' + name)}</loc><lastmod>)[^<]+"
            text = re.sub(pattern, rf"\g<1>{TODAY}", text)
        sitemap.write_text(text, encoding="utf-8")
        print("Updated sitemap lastmod for enhanced pages")
