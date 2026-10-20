import test from "node:test";
import assert from "node:assert/strict";
import { buildGenerationPayload } from "../generation-request.mjs";

const form = {
  mode: "reply",
  input: "Bitte reichen Sie die Rechnung TEST-17 bis zum 04.11.2026 ein.",
  instruction: "Ich werde TEST-17 bis zum 04.11.2026 einreichen.",
  sourceLanguage: "auto",
  targetLanguage: "de",
  recipient: "Arbeitgeber",
  recipientKey: "employer",
  tone: "Formell",
  name: "Anna Beispiel",
  uiLanguage: "de"
};

test("a new letter cannot inherit the previous reply instruction", () => {
  const shiftRequest = "Schicht am 27.10.2026 von 14:00 bis 18:00 auf den 28.10.2026 von 08:00 bis 12:00 verschieben.";
  const request = buildGenerationPayload({ ...form, mode: "create", input: shiftRequest });
  assert.equal(request.instruction, "");
  assert.equal(request.replyInstruction, "");
  assert.equal(request.intent, "");
  assert.equal(request.text, shiftRequest);
  assert.equal(request.situation, shiftRequest);
  assert.equal(request.message, shiftRequest);
  assert.equal(JSON.stringify(request).includes("TEST-17"), false);
  assert.equal(request.name, "Anna Beispiel");
  assert.equal(request.preserveFacts, true);
  assert.equal(request.preserveDates, true);
});

test("an explanation uses its current document, without instructions from an old reply", () => {
  const document = "Ihr Termin findet am 12.11.2026 um 10:30 Uhr statt.";
  const request = buildGenerationPayload({ ...form, mode: "explain", input: document, targetLanguage: "ru" });
  assert.equal(request.text, document);
  assert.equal(request.language, "ru");
  assert.equal(request.instruction, "");
  assert.equal(request.replyInstruction, "");
  assert.equal(request.intent, "");
  assert.equal(JSON.stringify(request).includes("TEST-17"), false);
});

test("a reply retains its own instruction and reference without changing the draft", () => {
  const draft = Object.freeze({ ...form });
  const request = buildGenerationPayload(draft);
  assert.equal(request.text, form.input);
  assert.equal(request.instruction, form.instruction);
  assert.equal(request.replyInstruction, form.instruction);
  assert.equal(request.intent, form.instruction);
  assert.equal(request.targetLanguage, "de");
  assert.equal(draft.instruction, form.instruction);
});
