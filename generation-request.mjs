const MODES = new Set(["create", "reply", "explain"]);

export function buildGenerationPayload(form) {
  if (!MODES.has(form.mode)) throw new TypeError("Unknown generation mode");

  const text = form.input.trim();
  const instruction = form.mode === "reply" ? form.instruction.trim() : "";

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
    name: form.name.trim(),
    uiLanguage: form.uiLanguage,
    preserveFacts: true,
    preserveDates: true,
    naturalReply: true,
    noInventedDates: true
  };
}
