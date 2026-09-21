import {templateIds,draftKey,fields,buildLetter,draftWarnings,validDraft} from './letter-templates.mjs?v=20260921-1';
import {messages} from './letter-template-i18n.mjs?v=20260921-1';
const $=id=>document.getElementById(id), form=$('letter-form'), output=$('letter-result');
const original=new Map([...document.querySelectorAll('[data-i18n]')].map(el=>[el.dataset.i18n,el.textContent]));
original.set('title','Ein Anliegen. Ein klarer Brief.');
const guidePaths={termin:'termin-behoerde-verschieben.html',bescheinigung:'arbeitsbescheinigung-anfordern.html',unterlagen:'unterlagen-nachreichen.html'};
let language='de', step=1, built=false;
const msg=key=>messages[language][key] || messages.de[key] || original.get(key) || key;
const status=key=>{$('form-status').textContent=msg(key);};
function updateWarnings() {
  const warnings=draftWarnings(output.value); $('draft-warning').hidden=!warnings.length;
  $('draft-warning').textContent=warnings.map(msg).join(' ');
  for(const id of ['copy-letter','download-letter','print-letter']) $(id).disabled=!output.value.trim();
}
function localize() {
  language=$('help-language').value; document.documentElement.lang=language;
  for(const el of document.querySelectorAll('[data-i18n]')) el.textContent=msg(el.dataset.i18n);
  $('progress').textContent=msg('progress').replace('{n}',step);
  $('form-status').textContent=''; updateWarnings();
}
function showStep(next, focus=true) {
  step=next; for(const el of document.querySelectorAll('[data-step]')) el.hidden=Number(el.dataset.step)!==step;
  $('progress').textContent=msg('progress').replace('{n}',step);
  if(focus) (step===1 ? $('template') : step===2 ? document.querySelector('[data-template]:not([hidden]) input') : output).focus();
}
function chooseTemplate() {
  const template=$('template').value;
  for(const group of document.querySelectorAll('[data-template]')) {
    group.hidden=group.dataset.template!==template;
    for(const input of group.querySelectorAll('input,textarea')) input.disabled=group.hidden;
  }
  $('matching-guide').href=guidePaths[template]; $('attachment-check').hidden=template!=='unterlagen';
}
function validateStep(number) {
  const inputs=[...document.querySelector(`[data-step="${number}"]`).querySelectorAll('input,textarea,select')].filter(input=>!input.disabled);
  for(const input of inputs) {
    input.setCustomValidity(input.required && !input.value.trim() ? msg('invalid') : '');
    if(!input.checkValidity()) {input.reportValidity();status('invalid');return false;}
  }
  if(number===2 && $('template').value==='unterlagen' && $('attachments').value.split('\n').filter(line=>line.trim()).length>8) {status('attachmentsError');$('attachments').focus();return false;}
  return true;
}
function saveButtons() {
  try {const raw=localStorage.getItem(draftKey); $('delete-draft').disabled=!raw; $('restore-draft').disabled=!raw;}
  catch {$('restore-draft').disabled=true; $('delete-draft').disabled=true;}
}
$('workspace').hidden=false;
const params=new URLSearchParams(location.search), initial=params.get('template');
if(templateIds.includes(initial)) $('template').value=initial;
const requestedLanguage=params.get('lang') || navigator.language.slice(0,2);
$('help-language').value=['de','ru','uk'].includes(requestedLanguage)?requestedLanguage:'de';
chooseTemplate();localize();showStep(1,false);saveButtons();
$('help-language').addEventListener('change',localize);
$('template').addEventListener('change',()=>{chooseTemplate();built=false;$('save-draft').disabled=true;});
form.addEventListener('input',event=>{
  event.target.setCustomValidity?.('');
  built=false;$('save-draft').disabled=true;
});
$('next-details').addEventListener('click',()=>{if(validateStep(1)) showStep(2);});
for(const button of document.querySelectorAll('[data-back]')) button.addEventListener('click',()=>showStep(Number(button.dataset.back)));
form.addEventListener('submit',event=>{
  event.preventDefault();
  if(step===1) {if(validateStep(1))showStep(2);return;}
  if(!validateStep(1)) {showStep(1);return;}
  if(!validateStep(2)) return;
  try {
    output.value=buildLetter($('template').value,Object.fromEntries(new FormData(form)));
    $('facts-checked').checked=false;$('files-checked').checked=false;
    built=true;$('save-draft').disabled=false;showStep(3);updateWarnings();status('built');
  } catch(error) {status(error.message==='attachments'?'attachmentsError':['identity','document','template'].includes(error.message)?'invalid':'dateError');}
});
$('edit-details').addEventListener('click',()=>{showStep(2);status('editing');});
output.addEventListener('input',()=>{$('facts-checked').checked=false;$('files-checked').checked=false;updateWarnings();});
$('copy-letter').addEventListener('click',async()=>{
  try {await navigator.clipboard.writeText(output.value);status('copied');}
  catch {output.focus();output.select();status('copyFallback');}
});
$('download-letter').addEventListener('click',()=>{
  if(!output.value.trim())return;
  const url=URL.createObjectURL(new Blob([output.value],{type:'text/plain;charset=utf-8'}));
  const link=document.createElement('a');link.href=url;link.download='briefly-'+$('template').value+'.txt';document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);status('downloaded');
});
$('print-letter').addEventListener('click',()=>{if(output.value.trim()) {$('print-letter-text').textContent=output.value;window.print();}});
window.addEventListener('beforeprint',()=>{$('print-letter-text').textContent=output.value;});
$('save-draft').addEventListener('click',()=>{
  if(!built)return;
  try {
    const draft={version:1,template:$('template').value,language,fields:Object.fromEntries(fields.filter(key=>!$(key).disabled).map(key=>[key,$(key).value])),text:output.value,savedAt:new Date().toISOString()};
    localStorage.setItem(draftKey,JSON.stringify(draft));saveButtons();status('saved');
  }catch {status('saveError');}
});
$('restore-draft').addEventListener('click',()=>{
  try {
    const draft=validDraft(JSON.parse(localStorage.getItem(draftKey)));
    if(!draft)throw new Error('invalid');
    $('template').value=draft.template;$('help-language').value=draft.language;
    for(const key of fields)$(key).value=draft.fields[key];
    chooseTemplate();output.value=draft.text;built=true;$('save-draft').disabled=false;
    $('facts-checked').checked=false;$('files-checked').checked=false;localize();showStep(3);status('restored');
  }catch {status('restoreError');}
});
$('delete-draft').addEventListener('click',()=>{try {localStorage.removeItem(draftKey);saveButtons();status('deleted');}catch {status('deleteError');}});
