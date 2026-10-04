"""Build reviewed DE/RU/UK entry pages for the three local letter helpers."""
from pathlib import Path
from html import escape as esc
import json, re

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-04'
TOPICS = {'krankmeldung':'krankmeldung-arbeitgeber','mietmangel':'mietmangel-melden','schule':'kind-schule-krankmelden'}
SOURCES = {
 'krankmeldung': ('https://www.gesetze-im-internet.de/entgfg/BJNR106500994.html', '§ 5 Entgeltfortzahlungsgesetz'),
 'mietmangel': ('https://www.gesetze-im-internet.de/bgb/__536c.html', '§ 536c BGB'),
 'schule': ('https://bass.schule.nrw/6043.htm', '§ 43 Schulgesetz NRW — Beispiel Nordrhein-Westfalen')
}
SAMPLES = {
 'krankmeldung': 'Betreff: Krankmeldung ab [Datum]\n\nSehr geehrte Damen und Herren,\n\nich bin ab dem [Datum] arbeitsunfähig und kann meine Arbeit nicht aufnehmen. Wie lange ich ausfalle, kann ich derzeit noch nicht sicher sagen. Ich informiere Sie, sobald mir Näheres bekannt ist.\n\nMit freundlichen Grüßen\n[Ihr Name]',
 'mietmangel': 'Betreff: Mängelmeldung und Bitte um Reparatur\n\nSehr geehrte Damen und Herren,\n\nich möchte Ihnen einen Mangel in meiner Mietwohnung melden.\nWohnung: [Adresse / Wohnungsnummer]\nBetroffener Bereich: [Raum]\nErstmals bemerkt am: [Datum]\n\n[Eigene Beobachtung auf Deutsch]\n\nBitte bestätigen Sie den Eingang dieser Meldung und teilen Sie mir mit, wann der Mangel geprüft und behoben werden kann. Bitte stimmen Sie einen Besuchstermin vorher mit mir ab.\n\nMit freundlichen Grüßen\n[Ihr Name]',
 'schule': 'Betreff: Krankheitsbedingte Abwesenheit: [Name des Kindes]\n\nSehr geehrte Damen und Herren,\n\nmein Kind [Name] aus der Klasse [Klasse] ist erkrankt und kann ab dem [Datum] nicht am Unterricht teilnehmen. Wie lange die Abwesenheit dauert, kann ich derzeit noch nicht sicher sagen. Ich informiere Sie, sobald die voraussichtliche Dauer feststeht oder sich ändert.\n\nBitte teilen Sie mir mit, falls nach den Vorgaben der Schule noch eine schriftliche Entschuldigung oder ein Nachweis benötigt wird.\n\nMit freundlichen Grüßen\n[Ihr Name]'
}
UI = {
 'de': {'skip':'Zum Inhalt','guides':'Alle Ratgeber','cta':'Deutsches Schreiben ohne Anmeldung vorbereiten →','ready':'Vorher bereitlegen','choice':'Die passende Variante wählen','sample':'Muster auf Deutsch','sampleHint':'Ersetzen Sie die Platzhalter. Der bearbeitbare Entwurf entsteht im Formular; eigene zusätzliche Sätze müssen auf Deutsch eingegeben werden.','check':'Vor dem Verwenden prüfen','source':'Offizielle Grundlage','review':'Quelle gelesen am 4. Oktober 2026. Formulierungen und Prüfschritte von Briefly, mit KI-Unterstützung erstellt. Die Seite ersetzt keine Beratung im Einzelfall.','next':'Mit dem Formular weiterarbeiten','local':'Die Vorlage wird auf der Seite erstellt. Es wird nichts automatisch gesendet oder gespeichert. Sie können den Text ändern, kopieren, als TXT herunterladen, drucken oder auf Wunsch in diesem Browser speichern.','more':'Weitere Alltagshilfen'},
 'ru': {'skip':'К содержанию','guides':'Все материалы','cta':'Подготовить немецкое письмо без регистрации →','ready':'Что подготовить','choice':'Какой вариант выбрать','sample':'Образец на немецком','sampleHint':'Замените места в квадратных скобках. В форме получится редактируемый черновик; собственные дополнительные предложения нужно вводить по-немецки.','check':'Что проверить перед использованием','source':'Официальный источник','review':'Источник прочитан 4 октября 2026 года. Формулировки и порядок проверки подготовлены Briefly с помощью ИИ. Материал не заменяет консультацию по вашему случаю.','next':'Перейти к заполнению','local':'Шаблон создаётся на странице. Автоматической отправки и сохранения нет. Текст можно изменить, скопировать, скачать в TXT, распечатать или по желанию сохранить в этом браузере.','more':'Другие повседневные задачи'},
 'uk': {'skip':'До змісту','guides':'Усі матеріали','cta':'Підготувати німецький лист без реєстрації →','ready':'Що підготувати','choice':'Який варіант обрати','sample':'Зразок німецькою','sampleHint':'Замініть місця у квадратних дужках. У формі вийде редагована чернетка; власні додаткові речення потрібно вводити німецькою.','check':'Що перевірити перед використанням','source':'Офіційне джерело','review':'Джерело прочитано 4 жовтня 2026 року. Формулювання й порядок перевірки підготовлено Briefly за допомогою ШІ. Матеріал не замінює консультацію щодо вашого випадку.','next':'Перейти до заповнення','local':'Шаблон створюється на сторінці. Автоматичного надсилання й збереження немає. Текст можна змінити, скопіювати, завантажити в TXT, роздрукувати або за бажанням зберегти в цьому браузері.','more':'Інші повсякденні завдання'}
}
CONTENT = {
 ('krankmeldung','ru'): {
 'title':'Как сообщить работодателю о болезни на немецком',
 'description':'Первое сообщение о болезни или продление отсутствия: немецкий образец и форма без регистрации с русскими подсказками. Без придуманного диагноза и даты возвращения.',
 'lead':'Если вы заболели и не можете работать, подготовьте короткое сообщение: кто отсутствует, с какой даты и как долго, если это уже известно. Форма помогает составить немецкий текст без регистрации.',
 'ready':['Имя работодателя, руководителя или отдела, куда нужно сообщить об отсутствии.','Ваше имя, первый день отсутствия и, при необходимости, время смены.','Предполагаемый последний день отсутствия, только если вы действительно его знаете.'],
 'choice':['Первое сообщение: выберите дату, с которой не можете работать. Если длительность неизвестна, оставьте последнее число пустым — черновик прямо скажет об этом.','Продление: выберите этот вариант, если вы уже сообщали об отсутствии и оно продолжается. Укажите новый период, а не выдумывайте дату первого сообщения.','Время смены необязательно. Оно помогает получателю понять, какую смену вы пропускаете, но не заменяет внутренний порядок уведомления.'],
 'detailTitle':'Сообщение и медицинское подтверждение — разные действия',
 'detail':'По § 5 EntgFG о нетрудоспособности и ожидаемой длительности нужно сообщить без промедления. Порядок медицинского подтверждения проверяйте отдельно. Эта форма не заявляет о справке или о подтверждении врачом.',
 'checks':['Вы действительно не можете работать с указанной даты?','Последний день известен или его следует убрать? Он не может быть раньше первого.','Нет ли в тексте диагноза или утверждения о справке, которых вы не собирались сообщать?','Вы выбрали способ уведомления, предусмотренный работодателем, и сохранили копию отправленного сообщения?']},
 ('krankmeldung','uk'): {
 'title':'Як повідомити роботодавцю про хворобу німецькою',
 'description':'Перше повідомлення про хворобу або продовження відсутності: німецький зразок і форма без реєстрації з українськими підказками. Без вигаданого діагнозу й дати повернення.',
 'lead':'Якщо ви захворіли й не можете працювати, підготуйте коротке повідомлення: хто відсутній, з якої дати й на який час, якщо це вже відомо. Форма допомагає скласти німецький текст без реєстрації.',
 'ready':['Ім’я роботодавця, керівника або відділу, якому потрібно повідомити про відсутність.','Ваше ім’я, перший день відсутності й за потреби час зміни.','Очікуваний останній день відсутності, лише якщо ви справді його знаєте.'],
 'choice':['Перше повідомлення: оберіть дату, з якої не можете працювати. Якщо тривалість невідома, залиште останню дату порожньою — чернетка прямо про це скаже.','Продовження: оберіть цей варіант, якщо вже повідомляли про відсутність і вона триває. Вкажіть новий період, а не вигадуйте дату першого повідомлення.','Час зміни необов’язковий. Він допомагає одержувачу зрозуміти, яку зміну ви пропускаєте, але не замінює внутрішнього порядку повідомлення.'],
 'detailTitle':'Повідомлення й медичне підтвердження — різні дії',
 'detail':'За § 5 EntgFG про непрацездатність та очікувану тривалість потрібно повідомити без зволікання. Порядок медичного підтвердження перевіряйте окремо. Форма не стверджує, що у вас є довідка чи підтвердження лікаря.',
 'checks':['Ви справді не можете працювати з указаної дати?','Останній день відомий чи його слід прибрати? Він не може бути раніше першого.','Чи немає в тексті діагнозу або твердження про довідку, яких ви не збиралися повідомляти?','Ви обрали спосіб повідомлення, передбачений роботодавцем, і зберегли копію надісланого повідомлення?']},
 ('mietmangel','ru'): {
 'title':'Как написать арендодателю о ремонте на немецком',
 'description':'Сообщить о холодном отоплении, отсутствии горячей воды, протечке или окне: немецкий образец и форма с русскими подсказками. Без регистрации.',
 'lead':'Сообщение о недостатке жилья должно помочь арендодателю найти квартиру, понять наблюдаемую проблему и согласовать следующий шаг. Выберите готовую фразу либо добавьте своё описание на немецком.',
 'ready':['Адрес съёмной квартиры и при необходимости её номер.','Комната или место, где вы заметили проблему.','Дата первого наблюдения и короткие факты, которые вы можете подтвердить.'],
 'choice':['В форме есть варианты: отопление остаётся холодным, нет горячей воды, вытекает вода, окно не закрывается как следует. Выберите только наблюдение, соответствующее действительности.','Для другой проблемы нужно самостоятельно написать описание по-немецки. Дополнительные наблюдения и время возможного визита необязательны.','Черновик просит подтвердить получение и сообщить о проверке и ремонте. Он не выдаёт пожелание за согласованный визит.'],
 'detailTitle':'Описание проблемы и срочный случай',
 'detail':'§ 536c BGB регулирует сообщение о недостатках жилья. Форма помогает описать наблюдение, но не определяет юридический срок или снижение аренды. При аварии используйте соответствующий экстренный контакт, а не ждите ответа через сайт.',
 'checks':['Адрес и комната точно относятся к проблеме?','В тексте есть наблюдение, а не неподтверждённая причина повреждения?','Дата — день, когда вы впервые заметили проблему, а не придуманная дата её появления?','Вы действительно приложили фотографии, если сами добавили такое утверждение? Шаблон не заявляет о приложениях автоматически.']},
 ('mietmangel','uk'): {
 'title':'Як написати орендодавцю про ремонт німецькою',
 'description':'Повідомити про холодне опалення, відсутність гарячої води, витік або вікно: німецький зразок і форма з українськими підказками. Без реєстрації.',
 'lead':'Повідомлення про недолік житла має допомогти орендодавцю знайти квартиру, зрозуміти спостережувану проблему й погодити наступний крок. Оберіть готову фразу або додайте власний опис німецькою.',
 'ready':['Адреса орендованої квартири й за потреби її номер.','Кімната або місце, де ви помітили проблему.','Дата першого спостереження й короткі факти, які можете підтвердити.'],
 'choice':['У формі є варіанти: опалення залишається холодним, немає гарячої води, витікає вода, вікно не закривається належним чином. Оберіть лише спостереження, що відповідає дійсності.','Для іншої проблеми потрібно самостійно написати опис німецькою. Додаткові спостереження й час можливого візиту необов’язкові.','Чернетка просить підтвердити отримання й повідомити про перевірку та ремонт. Вона не подає побажання як погоджений візит.'],
 'detailTitle':'Опис проблеми й терміновий випадок',
 'detail':'§ 536c BGB регулює повідомлення про недоліки житла. Форма допомагає описати спостереження, але не визначає юридичний строк чи зниження орендної плати. У разі аварії використовуйте відповідний екстрений контакт, а не чекайте відповіді через сайт.',
 'checks':['Адреса й кімната точно стосуються проблеми?','У тексті є спостереження, а не непідтверджена причина пошкодження?','Дата — день, коли ви вперше помітили проблему, а не вигадана дата її появи?','Ви справді додали фотографії, якщо самі вписали таке твердження? Шаблон не заявляє про додатки автоматично.']},
 ('schule','de'): {
 'title':'Kind in der Schule krankmelden: Nachricht und Entschuldigung',
 'description':'Ein krankes Kind in der Schule abmelden oder vergangene Fehltage entschuldigen: deutsche Muster und kostenloses Formular mit Hilfe DE/RU/UK. Ohne Anmeldung.',
 'lead':'Bereiten Sie eine kurze Schulnachricht mit Name, Klasse und tatsächlichem Zeitraum vor. Das Formular unterscheidet eine aktuelle Krankheitsmeldung von der Entschuldigung für vergangene Fehltage.',
 'ready':['Name des Kindes und gegebenenfalls die Klasse.','Erster Fehltag und letzter Fehltag, soweit bekannt.','Zuständige Lehrkraft oder Schulstelle sowie den von Ihrer Schule vorgesehenen Meldeweg.'],
 'choice':['Aktuelle Erkrankung: nennen Sie den ersten Fehltag. Bleibt das Ende leer, sagt der Entwurf, dass die Dauer noch nicht feststeht. Ein eingetragenes Ende wird als voraussichtlich bezeichnet.','Vergangene Fehltage: tragen Sie den tatsächlichen ersten und letzten Fehltag ein. Für einen einzelnen Tag sind beide Daten gleich. Der Entwurf bittet um Entschuldigung dieses Zeitraums.','Das Muster betrifft Krankheit. Für eine geplante Abwesenheit müssen Sie die Regeln für Beurlaubung separat klären. Eine Krankheitsmeldung ist keine Genehmigung.'],
 'detailTitle':'Den Meldeweg der Schule zuerst prüfen',
 'detail':'Regeln unterscheiden sich nach Bundesland und Schule. In NRW sieht § 43 SchulG eine zeitnahe Benachrichtigung und schriftliche Mitteilung des Grundes vor. Prüfen Sie Ihre Schulvorgaben zu Meldeweg, schriftlicher Entschuldigung und Nachweisen.',
 'checks':['Stimmen Name, Klasse und Zeitraum?','Ist der letzte Fehltag wirklich bekannt oder nur erwartet?','Haben Sie keine Diagnose und keine nicht vorhandene ärztliche Bescheinigung ergänzt?','Müssen Sie zusätzlich anrufen, eine Schul-App nutzen oder eine unterschriebene Entschuldigung einreichen? Die Seite sendet und unterschreibt nichts.']},
 ('schule','ru'): {
 'title':'Как сообщить школе о болезни ребёнка на немецком',
 'description':'Сообщить о болезни ребёнка или объяснить прошедшие пропуски школы: немецкий образец и бесплатная форма с русскими подсказками. Без регистрации.',
 'lead':'Подготовьте короткое сообщение школе с именем ребёнка, классом и настоящими датами. Форма различает текущую болезнь и объяснение уже прошедших пропусков.',
 'ready':['Имя и фамилия ребёнка, при необходимости класс.','Первый и последний день отсутствия, если они известны.','Учитель или школьный отдел и установленный школой способ уведомления.'],
 'choice':['Текущая болезнь: укажите первый день отсутствия. Если конец неизвестен, оставьте последнее число пустым. Указанный последний день будет назван предполагаемым.','Прошедшие пропуски: укажите фактические первый и последний день. Для одного дня обе даты одинаковы. Черновик просит считать отсутствие за этот период уважительным.','Образец предназначен для болезни. Для запланированного отсутствия отдельно уточняйте правила Beurlaubung. Сообщение о болезни не является разрешением на пропуск.'],
 'detailTitle':'Сначала уточните порядок в вашей школе',
 'detail':'Правила зависят от федеральной земли и школы. В NRW § 43 SchulG предусматривает своевременное уведомление и письменное сообщение о причине. Проверьте требования вашей школы к уведомлению, объяснению и подтверждению.',
 'checks':['Верны ли имя, класс и период отсутствия?','Последний день действительно известен или только предполагается?','Не добавлены ли диагноз или утверждение о справке, которой нет?','Нужно ли дополнительно позвонить, использовать школьное приложение или передать подписанное объяснение? Сайт ничего не отправляет и не подписывает.']},
 ('schule','uk'): {
 'title':'Як повідомити школі про хворобу дитини німецькою',
 'description':'Повідомити про хворобу дитини або пояснити минулі пропуски школи: німецький зразок і безкоштовна форма з українськими підказками. Без реєстрації.',
 'lead':'Підготуйте коротке повідомлення школі з ім’ям дитини, класом і справжніми датами. Форма розрізняє поточну хворобу й пояснення вже минулих пропусків.',
 'ready':['Ім’я та прізвище дитини, за потреби клас.','Перший та останній день відсутності, якщо вони відомі.','Учитель або шкільний відділ і встановлений школою спосіб повідомлення.'],
 'choice':['Поточна хвороба: вкажіть перший день відсутності. Якщо закінчення невідоме, залиште останню дату порожньою. Указаний останній день буде названо очікуваним.','Минулі пропуски: вкажіть фактичні перший та останній день. Для одного дня обидві дати однакові. Чернетка просить визнати відсутність за цей період поважною.','Зразок призначений для хвороби. Для запланованої відсутності окремо уточнюйте правила Beurlaubung. Повідомлення про хворобу не є дозволом на пропуск.'],
 'detailTitle':'Спочатку уточніть порядок у вашій школі',
 'detail':'Правила залежать від федеральної землі та школи. У NRW § 43 SchulG передбачає своєчасне повідомлення й письмове зазначення причини. Перевірте вимоги вашої школи до повідомлення, пояснення та підтвердження.',
 'checks':['Чи правильні ім’я, клас і період відсутності?','Останній день справді відомий чи лише очікується?','Чи не додано діагноз або твердження про довідку, якої немає?','Чи потрібно додатково зателефонувати, використати шкільний застосунок або передати підписане пояснення? Сайт нічого не надсилає й не підписує.']}
}

def filename(topic,lang):return TOPICS[topic]+('' if lang=='de' else '-'+lang)+'.html'
def alternatives(topic):return '\n'.join(f'<link rel="alternate" hreflang="{lang}" href="https://brieflyletters.com/{filename(topic,lang)}">' for lang in ['de','ru','uk'])
def ul(items):return '<ul>'+''.join('<li>'+esc(text)+'</li>' for text in items)+'</ul>'
def build(topic,lang,c):
    u=UI[lang];url='https://brieflyletters.com/'+filename(topic,lang)
    form=f'brief-vorlagen.html?template={topic}&amp;lang={lang}'
    switch=' '.join(f'<a href="{filename(topic,l)}" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+'>'+name+'</a>' for l,name in [('de','Deutsch'),('ru','Русский'),('uk','Українська')])
    schema={'@context':'https://schema.org','@type':'Article','headline':c['title'],'description':c['description'],'url':url,'inLanguage':lang,'dateModified':DATE,'publisher':{'@type':'Organization','name':'Briefly','url':'https://brieflyletters.com/'}}
    related=' '.join(f'<a href="{filename(t,lang)}">'+esc(CONTENT.get((t,lang),{'title':{'krankmeldung':'Krankmeldung an den Arbeitgeber','mietmangel':'Mietmangel melden'}[t] if t!='schule' else CONTENT[('schule','de')]['title']})['title'])+' →</a>' for t in TOPICS if t!=topic)
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(c['title'])} | Briefly</title><meta name="description" content="{esc(c['description'],quote=True)}"><meta name="robots" content="index,follow">
<link rel="canonical" href="{url}">{alternatives(topic)}
<meta property="og:type" content="article"><meta property="og:title" content="{esc(c['title'],quote=True)}"><meta property="og:description" content="{esc(c['description'],quote=True)}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="Briefly">
<link rel="icon" href="favicon.ico?v=5"><link rel="stylesheet" href="everyday-guides.css?v=20261004-1">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>
<body><a class="skip" href="#main">{u['skip']}</a><div class="wrap"><header class="nav"><a class="brand" href="index.html">Briefly ✒</a><a href="ratgeber.html">{u['guides']}</a><nav aria-label="Language">{switch}</nav></header>
<section class="hero"><span class="eyebrow">DE / RU / UK · Briefly</span><h1>{esc(c['title'])}</h1><p class="lead">{esc(c['lead'])}</p><a class="cta" href="{form}">{u['cta']}</a></section>
<main id="main" class="article"><section><h2>{u['ready']}</h2>{ul(c['ready'])}</section><section><h2>{u['choice']}</h2>{ul(c['choice'])}</section>
<section><h2>{u['sample']}</h2><p>{u['sampleHint']}</p><pre class="sample" lang="de">{esc(SAMPLES[topic])}</pre></section>
<section><h2>{esc(c['detailTitle'])}</h2><p>{esc(c['detail'])}</p></section><section><h2>{u['check']}</h2>{ul(c['checks'])}</section>
<section><h2>{u['next']}</h2><p>{u['local']}</p><a class="cta" href="{form}">{u['cta']}</a></section>
<section><h2>{u['more']}</h2><div class="links">{related}</div></section>
<section class="sources"><h2>{u['source']}</h2><a href="{SOURCES[topic][0]}">{esc(SOURCES[topic][1])}</a><p class="fine">{u['review']}</p></section></main>
<footer class="footer">© 2026 Briefly · <a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a> · <a href="kontakt.html">Kontakt</a></footer></div></body></html>\n'''

for (topic,lang),c in CONTENT.items():
    (ROOT/filename(topic,lang)).write_text(build(topic,lang,c),encoding='utf-8')
# Add the helper to existing German articles, preserving their reviewed content.
for topic in ['krankmeldung','mietmangel']:
    p=ROOT/filename(topic,'de');s=p.read_text()
    s=re.sub(r'<link rel="alternate" hreflang="(?:de|ru|uk)"[^>]*>','',s)
    s=s.replace('</head>',alternatives(topic)+'\n</head>',1)
    block=f'<section class="section" id="everyday-helper"><h2>{"Krankmeldung" if topic=="krankmeldung" else "Reparaturmeldung"} ohne Anmeldung vorbereiten</h2><p>Ergänzen Sie Ihre tatsächlichen Angaben und bearbeiten Sie den deutschen Entwurf. Hilfe auf Deutsch, Russisch und Ukrainisch. Eigene zusätzliche Sätze werden nicht übersetzt.</p><a class="cta" href="brief-vorlagen.html?template={topic}&amp;lang=de">Zum kostenlosen Formular →</a><p><a href="{filename(topic,"ru")}" lang="ru">Инструкция на русском →</a> · <a href="{filename(topic,"uk")}" lang="uk">Інструкція українською →</a></p></section>'
    s=re.sub(r'<section class="section" id="everyday-helper">.*?</section>','',s,flags=re.S)
    s=s.replace('</main>',block+'\n</main>',1)
    s=s.replace('Text überarbeitet: 3. Oktober 2026.','Text überarbeitet: 3. Oktober 2026. Formular und Sprachversionen ergänzt: 4. Oktober 2026.')
    p.write_text(s,encoding='utf-8')

p=ROOT/'sitemap.xml';s=p.read_text()
for topic,lang in CONTENT:
    url='https://brieflyletters.com/'+filename(topic,lang)
    if '<loc>'+url+'</loc>' not in s:s=s.replace('</urlset>',f'<url><loc>{url}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>')
for name in ['index.html','brief-vorlagen.html','ratgeber.html','krankmeldung-arbeitgeber.html','mietmangel-melden.html']:
    url='https://brieflyletters.com/'+('' if name=='index.html' else name)
    s=re.sub(r'(<url>\s*<loc>'+re.escape(url)+r'</loc>\s*<lastmod>)[^<]*(</lastmod>)',lambda m:m[1]+DATE+m[2],s)
p.write_text(s,encoding='utf-8')
print('Built 7 translated entry pages and linked both existing German guides.')
