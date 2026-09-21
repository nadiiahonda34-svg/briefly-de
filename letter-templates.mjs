export const templateIds = ['termin', 'bescheinigung', 'unterlagen'];
export const draftKey = 'briefly-guided-draft-v1';
export const fields = ['recipient','sender','reference','appointmentDate','appointmentTime','reason','alternative','document','purpose','neededBy','letterDate','attachments'];
const clean = (value, max = 600) => String(value ?? '').replace(/\r\n?/g,'\n').trim().slice(0,max);
export function germanDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error('date');
  const date = new Date(value+'T12:00:00Z');
  if (!Number.isFinite(+date) || date.toISOString().slice(0,10) !== value) throw new Error('date');
  return value.split('-').reverse().join('.');
}
export function buildLetter(template, values) {
  if (!templateIds.includes(template)) throw new Error('template');
  const v = Object.fromEntries(fields.map(key=>[key,clean(values[key])]));
  if (!v.sender || !v.recipient) throw new Error('identity');
  let subject, body;
  if (template === 'termin') {
    const date = germanDate(v.appointmentDate);
    if (v.appointmentTime && !/^([01]\d|2[0-3]):[0-5]\d$/.test(v.appointmentTime)) throw new Error('time');
    subject = 'Bitte um Verschiebung meines Termins am '+date;
    body = `ich habe bei Ihnen einen Termin am ${date}${v.appointmentTime ? ' um '+v.appointmentTime+' Uhr' : ''}. Diesen Termin kann ich leider nicht wahrnehmen.`;
    if (v.reason) body += '\n\nGrund meiner Anfrage: '+v.reason;
    body += '\n\nIch bitte Sie um einen Ersatztermin.';
    if (v.alternative) body += '\nAls mögliche Alternative schlage ich vor: '+v.alternative;
    body += '\n\nBitte teilen Sie mir mit, ob der bisherige Termin geändert werden kann und welcher neue Termin vorgesehen ist.';
  } else if (template === 'bescheinigung') {
    if (!v.document) throw new Error('document');
    subject = 'Bitte um Ausstellung einer Bescheinigung';
    body = 'ich bitte Sie um folgende Bescheinigung:\n'+v.document;
    if (v.purpose) body += '\n\nIch benötige sie für folgenden Zweck: '+v.purpose;
    if (v.neededBy) body += '\n\nWenn möglich, benötige ich die Bescheinigung bis zum '+germanDate(v.neededBy)+'.';
    body += '\n\nBitte teilen Sie mir mit, ob Sie dafür weitere Angaben benötigen und wie ich die Bescheinigung erhalten kann.';
  } else {
    const documents = v.attachments.split('\n').map(line=>line.trim()).filter(Boolean);
    if (!documents.length || documents.length > 8) throw new Error('attachments');
    subject = 'Nachreichung von Unterlagen';
    body = v.letterDate ? 'ich beziehe mich auf Ihr Schreiben vom '+germanDate(v.letterDate)+'.\n\n' : '';
    body += 'Hiermit reiche ich folgende Unterlagen nach:\n'+documents.map(line=>'– '+line).join('\n');
    body += '\n\nBitte bestätigen Sie den Eingang und teilen Sie mir mit, falls zu diesem Vorgang noch Unterlagen fehlen.';
  }
  return `An: ${v.recipient}\n\nBetreff: ${subject}${v.reference ? '\nAktenzeichen / Referenz: '+v.reference : ''}\n\nSehr geehrte Damen und Herren,\n\n${body}\n\nMit freundlichen Grüßen\n${v.sender}`;
}
export function draftWarnings(text) {
  const warnings = [];
  if (/\[[^\]\n]{1,100}\]|\{\{[^}]+\}\}/.test(text)) warnings.push('placeholders');
  if (!String(text).trim()) warnings.push('empty');
  return warnings;
}
export function validDraft(value) {
  if (!value || value.version !== 1 || !templateIds.includes(value.template) || !value.fields || typeof value.fields !== 'object' || Array.isArray(value.fields) || typeof value.text !== 'string' || value.text.length > 12000 || !Number.isFinite(Date.parse(value.savedAt))) return null;
  return {version:1,template:value.template,language:['de','ru','uk'].includes(value.language) ? value.language : 'de',fields:Object.fromEntries(fields.map(key=>[key,clean(value.fields[key])])),text:value.text,savedAt:value.savedAt};
}
