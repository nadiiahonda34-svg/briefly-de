const MODES = new Set(["create", "reply", "explain"]);
const EXPLAIN_INSTRUCTION = "Explain the source document in simple words in the selected target language. State what it means, what action it explicitly requests and any stated deadlines. Return only the explanation, without a greeting, sign-off or signature; do not draft a reply. Preserve names, dates, times, amounts and reference numbers from the source. Do not invent missing details.";

export function buildGenerationPayload(form) {
  if (!MODES.has(form.mode)) throw new TypeError("Unknown generation mode");

  const text = form.input.trim();
  const explaining = form.mode === "explain";
  const instruction = explaining ? EXPLAIN_INSTRUCTION : form.mode === "reply" ? form.instruction.trim() : "";

  return {
    mode: form.mode,
    situation: text,
    text,
    message: text,
    instruction,
    replyInstruction: instruction,
    intent: instruction,
    sourceLanguage: form.sourceLanguage,
    targetLanguage: form.targetLanguage,
    language: form.targetLanguage,
    recipient: form.recipient,
    recipientKey: form.recipientKey,
    tone: form.tone,
    name: explaining ? "" : form.name.trim(),
    uiLanguage: form.uiLanguage,
    preserveFacts: true,
    preserveDates: true,
    naturalReply: true,
    noInventedDates: true
  };
}
