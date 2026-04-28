// Background service worker: orchestrates recording lifecycle, manages the
// offscreen capture document, and handles upload to Whisper + Supabase.
import { transcribeAudio } from "../lib/openai";
import { saveTranscription } from "../lib/supabase";
import type { ExtMessage } from "../lib/messages";

interface RecordingState {
  isRecording: boolean;
  startedAt?: number;
  tabId?: number;
  clientId?: string | null;
  callUrl?: string;
}

let state: RecordingState = { isRecording: false };

const OFFSCREEN_PATH = "src/offscreen/offscreen.html";

async function ensureOffscreen(): Promise<void> {
  const url = chrome.runtime.getURL(OFFSCREEN_PATH);
  const runtimeAny = chrome.runtime as unknown as {
    getContexts?: (filter: { contextTypes: string[]; documentUrls?: string[] }) => Promise<unknown[]>;
  };
  if (runtimeAny.getContexts) {
    const contexts = await runtimeAny.getContexts({
      contextTypes: ["OFFSCREEN_DOCUMENT"],
      documentUrls: [url],
    });
    if (contexts && contexts.length > 0) return;
  }

  await chrome.offscreen.createDocument({
    url: OFFSCREEN_PATH,
    reasons: [chrome.offscreen.Reason.USER_MEDIA],
    justification: "Capture tab audio and mic to transcribe the call.",
  });
}

async function closeOffscreen(): Promise<void> {
  try {
    await chrome.offscreen.closeDocument();
  } catch {
    /* ignore */
  }
}

async function startRecording(tabId: number, clientId: string | null, callUrl: string): Promise<void> {
  if (state.isRecording) throw new Error("Already recording.");

  await ensureOffscreen();

  const streamId: string = await new Promise((resolve, reject) => {
    chrome.tabCapture.getMediaStreamId({ targetTabId: tabId }, (id) => {
      if (chrome.runtime.lastError || !id) {
        reject(new Error(chrome.runtime.lastError?.message ?? "Failed to get stream id."));
      } else {
        resolve(id);
      }
    });
  });

  const res = await chrome.runtime.sendMessage({
    target: "offscreen",
    type: "START",
    streamId,
  });
  if (!res?.ok) throw new Error(res?.error ?? "Offscreen failed to start.");

  state = {
    isRecording: true,
    startedAt: Date.now(),
    tabId,
    clientId,
    callUrl,
  };

  await chrome.action.setBadgeText({ text: "REC" });
  await chrome.action.setBadgeBackgroundColor({ color: "#dc2626" });
}

async function stopRecording(): Promise<void> {
  if (!state.isRecording) throw new Error("Not recording.");

  const res = await chrome.runtime.sendMessage({ target: "offscreen", type: "STOP" });
  if (!res?.ok) throw new Error(res?.error ?? "Offscreen failed to stop.");

  const { dataUrl, durationSeconds } = res as {
    dataUrl: string;
    durationSeconds: number;
    mimeType: string;
  };

  const captured = { ...state };
  state = { isRecording: false };
  await chrome.action.setBadgeText({ text: "" });
  await closeOffscreen();

  // Process async — don't block stop response
  void processRecording(dataUrl, durationSeconds, captured);
}

async function processRecording(
  dataUrl: string,
  durationSeconds: number,
  captured: RecordingState,
): Promise<void> {
  try {
    notify("Transcribing…", "Uploading audio to OpenAI Whisper.");
    const blob = await (await fetch(dataUrl)).blob();
    const transcript = await transcribeAudio(blob);
    const title = captured.callUrl ? new URL(captured.callUrl).hostname : "Call";
    await saveTranscription({
      client_id: captured.clientId ?? null,
      title,
      transcript,
      duration_seconds: durationSeconds,
      call_url: captured.callUrl ?? null,
    });
    notify("Transcription saved", `${Math.round(durationSeconds / 60)} min recorded. Click to view history.`, true);
  } catch (e) {
    notify("Transcription failed", String((e as Error).message ?? e));
  }
}

function notify(title: string, message: string, openHistory = false): void {
  const id = `ct_${Date.now()}`;
  chrome.notifications.create(id, {
    type: "basic",
    iconUrl: chrome.runtime.getURL("public/icons/icon128.png"),
    title,
    message,
  });
  if (openHistory) {
    chrome.notifications.onClicked.addListener((clicked) => {
      if (clicked === id) {
        chrome.tabs.create({ url: chrome.runtime.getURL("src/history/history.html") });
      }
    });
  }
}

chrome.runtime.onMessage.addListener((msg: ExtMessage, _sender, sendResponse) => {
  (async () => {
    try {
      if (msg.type === "START_RECORDING") {
        await startRecording(msg.tabId, msg.clientId, msg.callUrl);
        sendResponse({ ok: true });
      } else if (msg.type === "STOP_RECORDING") {
        await stopRecording();
        sendResponse({ ok: true });
      } else if (msg.type === "RECORDING_STATUS_REQUEST") {
        sendResponse({
          isRecording: state.isRecording,
          startedAt: state.startedAt,
          clientId: state.clientId,
        });
      } else if (msg.type === "DETECT_CALL") {
        sendResponse({ ok: true });
      } else {
        sendResponse({ ok: false, error: "Unknown message" });
      }
    } catch (e) {
      sendResponse({ ok: false, error: String((e as Error).message ?? e) });
    }
  })();
  return true;
});
