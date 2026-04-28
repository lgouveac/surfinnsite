// Offscreen document: captures tab audio + microphone, mixes them, and
// records via MediaRecorder. Service workers can't use MediaRecorder, so
// this lives in an offscreen page.

interface StartMsg { target: "offscreen"; type: "START"; streamId: string }
interface StopMsg { target: "offscreen"; type: "STOP" }
type Msg = StartMsg | StopMsg;

let recorder: MediaRecorder | null = null;
let chunks: Blob[] = [];
let tabStream: MediaStream | null = null;
let micStream: MediaStream | null = null;
let mixedStream: MediaStream | null = null;
let audioContext: AudioContext | null = null;
let startedAt = 0;

chrome.runtime.onMessage.addListener((msg: Msg, _sender, sendResponse) => {
  if (msg?.target !== "offscreen") return false;

  if (msg.type === "START") {
    start(msg.streamId)
      .then(() => sendResponse({ ok: true }))
      .catch((e) => sendResponse({ ok: false, error: String(e?.message ?? e) }));
    return true;
  }
  if (msg.type === "STOP") {
    stop()
      .then((res) => sendResponse({ ok: true, ...res }))
      .catch((e) => sendResponse({ ok: false, error: String(e?.message ?? e) }));
    return true;
  }
  return false;
});

async function start(streamId: string): Promise<void> {
  if (recorder) throw new Error("Already recording.");

  // Tab audio via getUserMedia with chromeMediaSource=tab
  tabStream = await navigator.mediaDevices.getUserMedia({
    audio: {
      // @ts-expect-error: chromeMediaSource is non-standard but required for tabCapture stream IDs
      mandatory: { chromeMediaSource: "tab", chromeMediaSourceId: streamId },
    },
    video: false,
  });

  // Keep playing tab audio to user's speakers (otherwise capturing mutes it).
  const ctx = new AudioContext();
  audioContext = ctx;
  const tabSource = ctx.createMediaStreamSource(tabStream);
  tabSource.connect(ctx.destination);

  // Mic
  try {
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
  } catch (e) {
    // If user denies mic, fall back to tab-only.
    console.warn("Mic permission denied; recording tab only.", e);
    micStream = null;
  }

  // Mix tab + mic into a single stream
  const dest = ctx.createMediaStreamDestination();
  tabSource.connect(dest);
  if (micStream) {
    const micSource = ctx.createMediaStreamSource(micStream);
    micSource.connect(dest);
  }
  mixedStream = dest.stream;

  chunks = [];
  recorder = new MediaRecorder(mixedStream, { mimeType: "audio/webm;codecs=opus" });
  recorder.ondataavailable = (ev) => {
    if (ev.data.size > 0) chunks.push(ev.data);
  };
  recorder.start(1000);
  startedAt = Date.now();
}

async function stop(): Promise<{ dataUrl: string; durationSeconds: number; mimeType: string }> {
  if (!recorder) throw new Error("Not recording.");
  const r = recorder;
  await new Promise<void>((resolve) => {
    r.onstop = () => resolve();
    r.stop();
  });

  const durationSeconds = Math.round((Date.now() - startedAt) / 1000);
  const blob = new Blob(chunks, { type: "audio/webm" });

  // Cleanup
  tabStream?.getTracks().forEach((t) => t.stop());
  micStream?.getTracks().forEach((t) => t.stop());
  audioContext?.close().catch(() => {});
  recorder = null;
  tabStream = null;
  micStream = null;
  mixedStream = null;
  audioContext = null;
  chunks = [];

  // Send back as data URL via FileReader so the service worker can rebuild Blob.
  const dataUrl: string = await new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onload = () => resolve(fr.result as string);
    fr.onerror = () => reject(fr.error);
    fr.readAsDataURL(blob);
  });

  return { dataUrl, durationSeconds, mimeType: blob.type };
}
