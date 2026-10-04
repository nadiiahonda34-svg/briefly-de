export const templateIds = ['termin', 'jobcenter-termin', 'bescheinigung', 'unterlagen', 'krankmeldung', 'mietmangel', 'schule'];
export const draftKey = 'briefly-guided-draft-v1';
export const fields = ['recipient','sender','reference','appointmentDate','appointmentTime','reason','alternative','jcAppointmentDate','jcAppointmentTime','jcReasonType','jcOtherReason','jcProof','jcAlternative','document','purpose','neededBy','letterDate','attachments','sickType','sickStart','sickEnd','sickShift','repairType','repairRoom','repairOtherRoom','repairAddress','repairSince','repairNote','repairAccess','childName','childClass','schoolMode','schoolStart','schoolEnd'];
export const repairProblems = {heating:'Die Heizung bleibt kalt.',water:'Es kommt kein warmes Wasser.',leak:'Es tritt Wasser aus.',window:'Das Fenster lässt sich nicht richtig schließen.'};
export const repairRooms = {kitchen:'Küche',bathroom:'Badezimmer',living:'Wohnzimmer',bedroom:'Schlafzimmer',all:'gesamte Wohnung'};
const clean = (value, max = 600) => String(value ?? '').replace(/\r\n?/g,'\n').trim().slice(0,max);
export function germanDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error('date');
  const date = new Date(value+'T12:00:00Z');
  if (!Number.isFinite(+date) || date.toISOString().slice(0,10) !== value) throw new Error('date');
  return value.split('-').reverse().join('.');
}
function dateRange(start,end) {
  const from=germanDate(start),to=end?germanDate(end):'';
  if(end && end<start) throw new Error('date');
  return {from,to};
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
  } else if (template === 'jobcenter-termin') {
    const date = germanDate(v.jcAppointmentDate);
    if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(v.jcAppointmentTime)) throw new Error('time');
    const reasons = {
      illness: 'ich bin erkrankt',
      child: 'mein Kind ist erkrankt und ich muss die Betreuung übernehmen'
    };
    if (!['illness','child','other'].includes(v.jcReasonType)) throw new Error('reason');
    if (v.jcReasonType === 'other' && !v.jcOtherReason) throw new Error('reason');
    if (!['attached','later','ask'].includes(v.jcProof)) throw new Error('proof');
    const reason = v.jcReasonType === 'other' ? v.jcOtherReason : reasons[v.jcReasonType];
    subject = 'Bitte um Verlegung meines Jobcenter-Termins am '+date;
    body = `den Termin am ${date} um ${v.jcAppointmentTime} Uhr kann ich aus folgendem Grund nicht wahrnehmen: ${reason}${/[.!?…]$/.test(reason) ? '' : '.'}`;
    if (v.jcProof === 'attached') body += '\n\nEinen Nachweis füge ich bei.';
    if (v.jcProof === 'later') body += '\n\nEinen Nachweis reiche ich zeitnah nach, sobald er vorliegt.';
    if (v.jcProof === 'ask') body += '\n\nBitte teilen Sie mir mit, welchen Nachweis ich für die Verhinderung einreichen soll.';
    body += '\n\nIch bitte um einen Ersatztermin und um Rückmeldung zum bisherigen Termin.';
    if (v.jcAlternative) body += '\nAls möglichen Zeitraum schlage ich vor: '+v.jcAlternative;
  } else if (template === 'bescheinigung') {
    if (!v.document) throw new Error('document');
    subject = 'Bitte um Ausstellung einer Bescheinigung';
    body = 'ich bitte Sie um folgende Bescheinigung:\n'+v.document;
    if (v.purpose) body += '\n\nIch benötige sie für folgenden Zweck: '+v.purpose;
    if (v.neededBy) body += '\n\nWenn möglich, benötige ich die Bescheinigung bis zum '+germanDate(v.neededBy)+'.';
    body += '\n\nBitte teilen Sie mir mit, ob Sie dafür weitere Angaben benötigen und wie ich die Bescheinigung erhalten kann.';
  } else if (template === 'krankmeldung') {
    if(!['initial','extension'].includes(v.sickType)) throw new Error('kind');
    const {from,to}=dateRange(v.sickStart,v.sickEnd);
    if(v.sickShift && !/^([01]\d|2[0-3]):[0-5]\d$/.test(v.sickShift)) throw new Error('time');
    subject=(v.sickType==='extension'?'Verlängerung meiner Krankmeldung ab ':'Krankmeldung ab ')+from;
    body=v.sickType==='extension'?'ergänzend zu meiner bisherigen Krankmeldung teile ich Ihnen mit, dass ich weiterhin arbeitsunfähig bin.\n\n':'';
    body+=`${v.sickType==='extension'?'Ich':'ich'} bin ab dem ${from} arbeitsunfähig und kann meine Arbeit${v.sickShift?' bzw. meine Schicht ab '+v.sickShift+' Uhr':''} nicht aufnehmen.`;
    body+='\n\n'+(to?`Voraussichtlich dauert meine Abwesenheit bis einschließlich ${to}.`:'Wie lange ich ausfalle, kann ich derzeit noch nicht sicher sagen.');
    body+=' Ich informiere Sie, sobald mir Näheres bekannt ist oder sich die voraussichtliche Dauer ändert.';
  } else if (template === 'mietmangel') {
    if(!v.repairAddress) throw new Error('address');
    if(![...Object.keys(repairProblems),'other'].includes(v.repairType)) throw new Error('kind');
    if(![...Object.keys(repairRooms),'other'].includes(v.repairRoom)) throw new Error('room');
    if(v.repairType==='other' && !v.repairNote) throw new Error('details');
    if(v.repairRoom==='other' && !v.repairOtherRoom) throw new Error('details');
    const room=v.repairRoom==='other'?v.repairOtherRoom:repairRooms[v.repairRoom];
    subject='Mängelmeldung und Bitte um Reparatur';
    body=`ich möchte Ihnen einen Mangel in meiner Mietwohnung melden.\n\nWohnung: ${v.repairAddress}\nBetroffener Bereich: ${room}\nErstmals bemerkt am: ${germanDate(v.repairSince)}\n\n`;
    if(v.repairType!=='other') body+=repairProblems[v.repairType]+(v.repairNote?'\nWeitere Beobachtung: '+v.repairNote:'');
    else body+=v.repairNote;
    body+='\n\nBitte bestätigen Sie den Eingang dieser Meldung und teilen Sie mir mit, wann der Mangel geprüft und behoben werden kann.';
    if(v.repairAccess) body+='\nFür eine vorherige Terminabsprache schlage ich folgende Zeitfenster vor: '+v.repairAccess;
    body+='\n\nBitte stimmen Sie einen Besuchstermin vorher mit mir ab.';
  } else if (template === 'schule') {
    if(!v.childName) throw new Error('child');
    if(!['current','past'].includes(v.schoolMode)) throw new Error('kind');
    if(v.schoolMode==='past' && !v.schoolEnd) throw new Error('date');
    const {from,to}=dateRange(v.schoolStart,v.schoolEnd);
    subject=(v.schoolMode==='past'?'Entschuldigung für die krankheitsbedingte Abwesenheit: ':'Krankheitsbedingte Abwesenheit: ')+v.childName;
    const child=`mein Kind ${v.childName}${v.childClass?' aus der Klasse '+v.childClass:''}`;
    if(v.schoolMode==='past') {
      const period=from===to?'am '+from:`vom ${from} bis einschließlich ${to}`;
      body=`${child} konnte ${period} wegen Krankheit nicht am Unterricht teilnehmen.\n\nIch bitte Sie, die krankheitsbedingte Abwesenheit zu entschuldigen.`;
    } else {
      body=`${child} ist erkrankt und kann ab dem ${from} nicht am Unterricht teilnehmen.`;
      body+='\n\n'+(to?`Voraussichtlich dauert die Abwesenheit bis einschließlich ${to}.`:'Wie lange die Abwesenheit dauert, kann ich derzeit noch nicht sicher sagen.');
      body+=' Ich informiere Sie, sobald die voraussichtliche Dauer feststeht oder sich ändert.';
    }
    body+='\n\nBitte teilen Sie mir mit, falls nach den Vorgaben der Schule noch eine schriftliche Entschuldigung oder ein Nachweis benötigt wird.';
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
