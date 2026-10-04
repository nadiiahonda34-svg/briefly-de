import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {buildLetter,validDraft,fields,templateIds} from '../letter-templates.mjs';
import {everydayMessages} from '../everyday-template-i18n.mjs';
import {messages} from '../letter-template-i18n.mjs';
const identity={recipient:'Teststelle',sender:'Testperson'};

test('sick leave preserves unknown duration and never claims a medical certificate',()=>{
  const letter=buildLetter('krankmeldung',{...identity,sickType:'initial',sickStart:'2026-10-06'});
  assert.match(letter,/ab dem 06\.10\.2026 arbeitsunfähig/);
  assert.match(letter,/Wie lange ich ausfalle, kann ich derzeit noch nicht sicher sagen/);
  assert.doesNotMatch(letter,/bis einschließlich|ärztlich|Bescheinigung|Diagnose|Schicht|Verlängerung/);
  const extension=buildLetter('krankmeldung',{...identity,sickType:'extension',sickStart:'2026-10-06',sickEnd:'2026-10-09',sickShift:'07:30'});
  assert.match(extension,/ergänzend zu meiner bisherigen Krankmeldung/);
  assert.match(extension,/Voraussichtlich dauert meine Abwesenheit bis einschließlich 09\.10\.2026/);
  assert.match(extension,/Schicht ab 07:30 Uhr/);
  assert.throws(()=>buildLetter('krankmeldung',{...identity,sickType:'initial',sickStart:'2026-10-06',sickShift:'24:00'}),/time/);
});
test('absence ranges reject impossible dates and reversed ranges',()=>{
  for(const template of ['krankmeldung','schule']) {
    const data=template==='krankmeldung'?{sickType:'initial',sickStart:'2026-10-08',sickEnd:'2026-10-07'}:{childName:'Testkind',schoolMode:'current',schoolStart:'2026-10-08',schoolEnd:'2026-10-07'};
    assert.throws(()=>buildLetter(template,{...identity,...data}),/date/);
    const start=template==='krankmeldung'?'sickStart':'schoolStart';
    assert.throws(()=>buildLetter(template,{...identity,...data,[start]:'2026-02-30'}),/date/);
  }
});
test('repair message uses selected observations and omits unused custom data',()=>{
  const base={...identity,repairAddress:'Teststraße 1, Wohnung 2',repairType:'heating',repairRoom:'bedroom',repairSince:'2026-10-04'};
  const letter=buildLetter('mietmangel',{...base,repairOtherRoom:'NOT SELECTED',repairAccess:'dienstags 10–12 Uhr'});
  assert.match(letter,/Teststraße 1, Wohnung 2/);assert.match(letter,/Schlafzimmer/);assert.match(letter,/Erstmals bemerkt am: 04\.10\.2026/);
  assert.match(letter,/Die Heizung bleibt kalt/);assert.match(letter,/dienstags 10–12 Uhr/);
  assert.doesNotMatch(letter,/NOT SELECTED|Mietminderung|14 Tage|Fotos|Ursache|defekt/);
  const custom=buildLetter('mietmangel',{...base,repairType:'other',repairRoom:'other',repairOtherRoom:'Flur',repairNote:'Die Lampe flackert.'});
  assert.match(custom,/Betroffener Bereich: Flur/);assert.match(custom,/Die Lampe flackert/);assert.doesNotMatch(custom,/Heizung bleibt kalt/);
  for(const data of [{...base,repairType:'other',repairNote:''},{...base,repairRoom:'other',repairOtherRoom:''},{...base,repairAddress:''},{...base,repairType:'not-real'},{...base,repairRoom:'not-real'}])assert.throws(()=>buildLetter('mietmangel',data));
});
test('school letter distinguishes current illness from completed absence',()=>{
  const base={...identity,childName:'Testkind',childClass:'3b',schoolStart:'2026-10-06'};
  const current=buildLetter('schule',{...base,schoolMode:'current'});
  assert.match(current,/Testkind aus der Klasse 3b/);assert.match(current,/Dauer feststeht oder sich ändert/);
  assert.doesNotMatch(current,/bis einschließlich|entschuldigen|ärztlich|Attest liegt/);
  const single=buildLetter('schule',{...base,schoolMode:'past',schoolEnd:'2026-10-06'});
  assert.match(single,/am 06\.10\.2026 wegen Krankheit/);assert.match(single,/Abwesenheit zu entschuldigen/);assert.doesNotMatch(single,/Voraussichtlich/);
  const range=buildLetter('schule',{...base,schoolMode:'past',schoolEnd:'2026-10-08'});
  assert.match(range,/vom 06\.10\.2026 bis einschließlich 08\.10\.2026/);
  assert.throws(()=>buildLetter('schule',{...base,schoolMode:'past'}),/date/);
  assert.throws(()=>buildLetter('schule',{...base,schoolMode:'current',childName:''}),/child/);
});
test('new saved drafts restore fields and manual edits while old drafts remain compatible',()=>{
  for(const template of ['krankmeldung','mietmangel','schule']) {
    const data={version:1,template,language:'uk',fields:{...identity,sickType:'extension',repairType:'other',repairOtherRoom:'Flur',childName:'Testkind',schoolMode:'past'},text:'Manuell bearbeitet.\n<Nur Text>',savedAt:'2026-10-04T08:00:00Z'};
    const restored=validDraft(JSON.parse(JSON.stringify(data)));
    assert.equal(restored.text,data.text);assert.deepEqual(restored.fields,Object.fromEntries(fields.map(k=>[k,data.fields[k]||''])));
  }
  const old=validDraft({version:1,template:'termin',language:'ru',fields:{...identity,appointmentDate:'2026-10-06'},text:'Bestehender Entwurf',savedAt:'2026-09-29T12:00:00Z'});
  assert.equal(old.text,'Bestehender Entwurf');assert.equal(old.fields.appointmentDate,'2026-10-06');assert.equal(old.fields.schoolMode,'');
});
test('all new helper text has German, Russian and Ukrainian coverage and field bindings',()=>{
  const html=readFileSync(new URL('../brief-vorlagen.html',import.meta.url),'utf8');
  const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(new Set(ids).size,ids.length);
  for(const field of fields)assert.ok(ids.includes(field),field);
  for(const key of Object.keys(everydayMessages.de)) for(const lang of ['de','ru','uk']) {
    assert.ok(everydayMessages[lang][key]?.trim(),`${lang}:${key}`);assert.equal(messages[lang][key],everydayMessages[lang][key]);
  }
  assert.equal(templateIds.length,7);
});
test('each new search entry has a reciprocal language family and directs to the matching local helper',()=>{
  for(const [topic,base] of Object.entries({krankmeldung:'krankmeldung-arbeitgeber',mietmangel:'mietmangel-melden',schule:'kind-schule-krankmelden'})) for(const lang of ['de','ru','uk']) {
    const name=base+(lang==='de'?'':'-'+lang)+'.html',html=readFileSync(new URL('../'+name,import.meta.url),'utf8');
    for(const alternate of ['de','ru','uk']) assert.ok(html.includes(`hreflang="${alternate}" href="https://brieflyletters.com/${base}${alternate==='de'?'':'-'+alternate}.html"`),`${name}:${alternate}`);
    assert.ok(html.includes(`template=${topic}&amp;lang=${lang}`),name);
    assert.ok(html.includes(`<html lang="${lang}"`),name);
  }
});
