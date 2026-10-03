import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import {buildLetter,germanDate,draftWarnings,validDraft} from '../letter-templates.mjs';

const identity={recipient:'Teststelle',sender:'Testperson',reference:'TEST-123'};
test('appointment request uses the supplied date and does not invent a reason or confirmation',()=>{
  const result=buildLetter('termin',{...identity,appointmentDate:'2026-10-08',appointmentTime:'09:30',alternative:'freitags ab 10 Uhr'});
  assert.match(result,/08\.10\.2026 um 09:30 Uhr/);
  assert.match(result,/Als mögliche Alternative schlage ich vor: freitags ab 10 Uhr/);
  assert.match(result,/ob der bisherige Termin geändert werden kann/);
  assert.doesNotMatch(result,/Grund meiner Anfrage|krank|undefined|null/);
  assert.throws(()=>buildLetter('termin',{...identity,appointmentDate:'2026-10-08',appointmentTime:'25:00'}),/time/);
});
test('Jobcenter draft names only the chosen cause and proof plan',()=>{
  const base={...identity,jcAppointmentDate:'2026-10-08',jcAppointmentTime:'09:30'};
  const attached=buildLetter('jobcenter-termin',{...base,jcReasonType:'illness',jcProof:'attached'});
  assert.match(attached,/Jobcenter-Termins am 08\.10\.2026/);
  assert.match(attached,/08\.10\.2026 um 09:30 Uhr/);
  assert.match(attached,/ich bin erkrankt/);
  assert.match(attached,/Einen Nachweis füge ich bei/);
  assert.doesNotMatch(attached,/Kind ist erkrankt|reiche ich zeitnah nach|bereits bestätigt/);
  const later=buildLetter('jobcenter-termin',{...base,jcReasonType:'child',jcProof:'later'});
  assert.match(later,/mein Kind ist erkrankt und ich muss die Betreuung übernehmen/);
  assert.match(later,/reiche ich zeitnah nach, sobald er vorliegt/);
  assert.doesNotMatch(later,/füge ich bei/);
  const custom=buildLetter('jobcenter-termin',{...base,jcReasonType:'other',jcOtherReason:'wichtiger anderer Termin',jcProof:'ask',jcAlternative:'freitags ab 10 Uhr'});
  assert.match(custom,/wichtiger anderer Termin/);
  assert.match(custom,/welchen Nachweis ich für die Verhinderung einreichen soll/);
  assert.match(custom,/Als möglichen Zeitraum schlage ich vor: freitags ab 10 Uhr/);
});
test('Jobcenter draft cannot omit the real reason, proof choice, date or time',()=>{
  const base={...identity,jcAppointmentDate:'2026-10-08',jcAppointmentTime:'09:30',jcReasonType:'other',jcOtherReason:'ein wichtiger Termin',jcProof:'ask'};
  for(const field of ['jcReasonType','jcOtherReason','jcProof','jcAppointmentDate','jcAppointmentTime']) {
    const values={...base,[field]:''};
    assert.throws(()=>buildLetter('jobcenter-termin',values),undefined,field);
  }
  assert.throws(()=>buildLetter('jobcenter-termin',{...base,jcAppointmentDate:'2026-02-30'}),/date/);
  assert.throws(()=>buildLetter('jobcenter-termin',{...base,jcAppointmentTime:'29:99'}),/time/);
  assert.throws(()=>buildLetter('jobcenter-termin',{...base,jcProof:'not-real'}),/proof/);
});
test('invalid dates and blank identity are rejected',()=>{
  assert.equal(germanDate('2028-02-29'),'29.02.2028');
  for(const date of ['2026-02-29','2026-13-02','2026-04-31','08.10.2026','']) assert.throws(()=>germanDate(date),/date/);
  assert.throws(()=>buildLetter('termin',{...identity,sender:'  ',appointmentDate:'2026-10-08'}),/identity/);
  assert.throws(()=>buildLetter('unknown',identity),/template/);
});
test('certificate names remain exact and a requested date is a request',()=>{
  const result=buildLetter('bescheinigung',{...identity,document:'Verdienstbescheinigung für August 2026',neededBy:'2026-10-09'});
  assert.match(result,/Verdienstbescheinigung für August 2026/);
  assert.match(result,/Wenn möglich, benötige ich die Bescheinigung bis zum 09\.10\.2026/);
  assert.doesNotMatch(result,/folgenden Zweck|undefined/);
  assert.throws(()=>buildLetter('bescheinigung',{...identity,document:'  '}),/document/);
});
test('attachment list includes only the entered documents and enforces the limit',()=>{
  const result=buildLetter('unterlagen',{...identity,letterDate:'2026-09-17',attachments:'Dokument A\n\n Dokument B '});
  assert.match(result,/Ihr Schreiben vom 17\.09\.2026/);
  assert.match(result,/– Dokument A\n– Dokument B/);
  assert.throws(()=>buildLetter('unterlagen',{...identity,attachments:'\n '}),/attachments/);
  assert.throws(()=>buildLetter('unterlagen',{...identity,attachments:Array(9).fill('Dokument').join('\n')}),/attachments/);
  assert.doesNotThrow(()=>buildLetter('unterlagen',{...identity,attachments:Array(8).fill('Dokument').join('\n')}));
});
test('draft restoration preserves manual edits and rejects incompatible data',()=>{
  const draft={version:1,template:'termin',language:'ru',fields:identity,text:'Mein manuell bearbeiteter Text.\n<Das ist Text>',savedAt:'2026-09-21T12:00:00Z'};
  const restored=validDraft(JSON.parse(JSON.stringify(draft)));
  assert.equal(restored.text,draft.text);assert.equal(restored.language,'ru');
  for(const invalid of [null,{...draft,version:2},{...draft,template:'other'},{...draft,text:'x'.repeat(12001)},{...draft,savedAt:'bad'},{...draft,fields:[]}]) assert.equal(validDraft(invalid),null);
  assert.deepEqual(draftWarnings('[Dokument]'),['placeholders']);
  assert.deepEqual(draftWarnings('{{Name}}'),['placeholders']);
  assert.deepEqual(draftWarnings('   '),['empty']);
  assert.deepEqual(draftWarnings('Fertiger Text.'),[]);
  const jobcenter={...draft,template:'jobcenter-termin',fields:{...identity,jcReasonType:'child',jcProof:'later'}};
  assert.equal(validDraft(jobcenter).fields.jcReasonType,'child');
  assert.equal(validDraft(jobcenter).fields.jcProof,'later');
});

const homepage=readFileSync(new URL('../index.html',import.meta.url),'utf8');
test('every inline homepage script parses',()=>{
  for(const match of homepage.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)) {
    if(!/application\/ld\+json/.test(match[1]) && match[2].trim()) new vm.Script(match[2]);
  }
});
test('all nine UI languages keep guide titles attached to their links after card reordering',()=>{
  const script=[...homepage.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes('function localizeGuidesSection'));
  const translations=JSON.parse(script.match(/const CARD_I18N=(.*);/)[1]);
  const paths=['jobcenter-briefe-verstehen.html','vermieter-brief-verstehen.html','behoerdenbriefe-verstehen.html','formelle-antwort-deutsch.html','ueber-briefly.html','ratgeber.html','behoerden-deutsch-glossar.html','brief-checkliste.html'];
  const node=textContent=>({textContent});
  const cardsFrom=section=>[...section.matchAll(/<a class="resource-card" href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g)].map(m=>{
    const parts={'.tag':node(''),h3:node(m[2].match(/<h3>(.*?)<\/h3>/)[1]),p:node(''),'.read':node('')};
    return {href:m[1],parts,getAttribute:()=>m[1],querySelector:s=>parts[s]};
  });
  const startCards=cardsFrom(homepage.match(/<section class="section" id="start-here">([\s\S]*?)<\/section>/)[1]);
  const guideCards=cardsFrom(homepage.match(/<section class="section resources" id="resources">([\s\S]*?)<\/section>/)[1]);
  assert.equal(startCards.length,6);
  assert.equal(guideCards.length,6);
  const startTitles=startCards.map(c=>c.parts.h3.textContent);
  const resources=guideCards.slice().reverse();
  resources.push({getAttribute:()=> 'future-guide.html',querySelector:()=>{throw new Error('Unknown cards must be left alone');}});
  const ids=new Map(['guidesTitle','guidesIntro','guided-title','guided-description','guided-link'].map(id=>[id,node('')]));
  const select={value:'de',addEventListener:()=>{}};
  const document={getElementById:id=>ids.get(id),documentElement:{lang:'de'},querySelector:s=>s==='select'?select:null,querySelectorAll:s=>s==='#resources .resource-card'?resources:s==='.resource-card'?[...startCards,...resources]:[]};
  const window={};const STATUS_UI=Object.fromEntries(Object.keys(translations).map(lang=>[lang,['','','','','Guides in German']]));
  vm.runInNewContext(script,{document,window,STATUS_UI,navigator:{language:'de'}});
  for(const lang of ['de','en','ru','uk','pl','fr','es','it','ar']) {
    window.localizeGuidesSection(lang);
    for(const card of guideCards) assert.equal(card.parts.h3.textContent,translations[lang][paths.indexOf(card.href)][1],`${lang}: ${card.href}`);
    assert.deepEqual(startCards.map(c=>c.parts.h3.textContent),startTitles);
  }
});

