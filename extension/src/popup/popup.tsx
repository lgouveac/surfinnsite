import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { isConfigured } from "../lib/storage";
import { listClients, createClient_, type Client } from "../lib/supabase";
import type { ExtMessage } from "../lib/messages";

const CALL_DOMAINS = [
  "meet.google.com",
  "zoom.us",
  "teams.microsoft.com",
];

function isCallUrl(url?: string): boolean {
  if (!url) return false;
  try {
    const u = new URL(url);
    return CALL_DOMAINS.some((d) => u.hostname.endsWith(d));
  } catch {
    return false;
  }
}

function App() {
  const [configured, setConfigured] = useState<boolean | null>(null);
  const [tab, setTab] = useState<chrome.tabs.Tab | null>(null);
  const [clients, setClients] = useState<Client[]>([]);
  const [selectedClient, setSelectedClient] = useState<string>("");
  const [showNewClient, setShowNewClient] = useState(false);
  const [newName, setNewName] = useState("");
  const [newEmail, setNewEmail] = useState("");
  const [newNotes, setNewNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [recordingStatus, setRecordingStatus] = useState<{
    isRecording: boolean;
    startedAt?: number;
  }>({ isRecording: false });

  useEffect(() => {
    (async () => {
      const ok = await isConfigured();
      setConfigured(ok);
      const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
      setTab(activeTab ?? null);
      if (ok) await refreshClients();
      const status = await chrome.runtime.sendMessage({ type: "RECORDING_STATUS_REQUEST" } satisfies ExtMessage);
      if (status) setRecordingStatus(status);
    })();
  }, []);

  const refreshClients = async () => {
    try {
      const list = await listClients();
      setClients(list);
    } catch (e) {
      setError(`Failed to load clients: ${(e as Error).message}`);
    }
  };

  const handleCreateClient = async () => {
    setError(null);
    if (!newName.trim()) {
      setError("Name is required.");
      return;
    }
    setLoading(true);
    try {
      const c = await createClient_({ name: newName.trim(), email: newEmail.trim(), notes: newNotes.trim() });
      await refreshClients();
      setSelectedClient(c.id);
      setShowNewClient(false);
      setNewName(""); setNewEmail(""); setNewNotes("");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleStart = async () => {
    setError(null);
    if (!tab?.id || !tab.url) { setError("No active tab."); return; }
    setLoading(true);
    try {
      await chrome.runtime.sendMessage({
        type: "START_RECORDING",
        tabId: tab.id,
        clientId: selectedClient || null,
        callUrl: tab.url,
      } satisfies ExtMessage);
      setRecordingStatus({ isRecording: true, startedAt: Date.now() });
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    setError(null);
    setLoading(true);
    try {
      await chrome.runtime.sendMessage({ type: "STOP_RECORDING" } satisfies ExtMessage);
      setRecordingStatus({ isRecording: false });
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  if (configured === null) return <div className="app">Loading…</div>;

  if (!configured) {
    return (
      <div className="app">
        <h1>Call Transcripter</h1>
        <p className="sub">Set your OpenAI key and Supabase project first.</p>
        <button className="primary" onClick={() => chrome.runtime.openOptionsPage()}>
          Open settings
        </button>
      </div>
    );
  }

  if (recordingStatus.isRecording) {
    return (
      <div className="app">
        <div className="recording-banner">
          <span className="recording-dot" /> Recording in progress
        </div>
        <button className="stop" onClick={handleStop} disabled={loading}>
          {loading ? "Stopping…" : "Stop & transcribe"}
        </button>
        <p className="sub" style={{ marginTop: 12 }}>
          Audio uploads to OpenAI Whisper after stop. Transcript saves to Supabase.
        </p>
      </div>
    );
  }

  const onCall = isCallUrl(tab?.url);

  return (
    <div className="app">
      <h1>Call Transcripter</h1>
      <p className="sub">
        {onCall ? "Call detected on this tab." : "Open a Meet, Zoom or Teams call."}
      </p>

      {!showNewClient ? (
        <>
          <label>Client</label>
          <select value={selectedClient} onChange={(e) => setSelectedClient(e.target.value)}>
            <option value="">— No client —</option>
            {clients.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
          <button className="ghost" onClick={() => setShowNewClient(true)}>+ New client</button>
        </>
      ) : (
        <>
          <label>Name</label>
          <input value={newName} onChange={(e) => setNewName(e.target.value)} placeholder="Acme Inc." />
          <label>Email (optional)</label>
          <input value={newEmail} onChange={(e) => setNewEmail(e.target.value)} placeholder="contact@acme.com" />
          <label>Notes (optional)</label>
          <textarea value={newNotes} onChange={(e) => setNewNotes(e.target.value)} />
          <div className="row">
            <button className="primary" onClick={handleCreateClient} disabled={loading}>
              {loading ? "Saving…" : "Create"}
            </button>
            <button className="ghost" onClick={() => setShowNewClient(false)}>Cancel</button>
          </div>
        </>
      )}

      {!showNewClient && (
        <>
          <div className="row">
            <button className="primary" onClick={handleStart} disabled={loading || !onCall}>
              {loading ? "Starting…" : "Start recording"}
            </button>
          </div>
          {!onCall && (
            <div className="status warn" style={{ marginTop: 8 }}>
              Recording works on Meet, Zoom Web, or Teams Web tabs.
            </div>
          )}
          <div className="consent">
            ⚠️ Tell participants you're recording before you start. Compliance is on you.
          </div>
        </>
      )}

      {error && <div className="status err">{error}</div>}

      <div style={{ marginTop: 14, display: "flex", justifyContent: "space-between" }}>
        <a href="#" onClick={(e) => { e.preventDefault(); chrome.tabs.create({ url: chrome.runtime.getURL("src/history/history.html") }); }}>
          History
        </a>
        <a href="#" onClick={(e) => { e.preventDefault(); chrome.runtime.openOptionsPage(); }}>
          Settings
        </a>
      </div>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
