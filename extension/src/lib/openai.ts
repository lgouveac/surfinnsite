import { getConfig } from "./storage";

const WHISPER_LIMIT_BYTES = 25 * 1024 * 1024;

export async function transcribeAudio(
  audio: Blob,
  opts?: { language?: string; prompt?: string },
): Promise<string> {
  const cfg = await getConfig();
  if (!cfg?.openaiKey) throw new Error("OpenAI key not configured.");

  if (audio.size > WHISPER_LIMIT_BYTES) {
    throw new Error(
      `Audio is ${(audio.size / 1024 / 1024).toFixed(1)}MB; Whisper limit is 25MB. Split before uploading.`,
    );
  }

  const form = new FormData();
  form.append("file", audio, "call.webm");
  form.append("model", "whisper-1");
  form.append("response_format", "text");
  if (opts?.language) form.append("language", opts.language);
  if (opts?.prompt) form.append("prompt", opts.prompt);

  const res = await fetch("https://api.openai.com/v1/audio/transcriptions", {
    method: "POST",
    headers: { Authorization: `Bearer ${cfg.openaiKey}` },
    body: form,
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Whisper failed (${res.status}): ${txt}`);
  }
  return await res.text();
}
