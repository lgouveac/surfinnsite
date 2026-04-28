import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { getConfig, setConfig, type AppConfig } from "../lib/storage";
import { resetSupabase } from "../lib/supabase";

function App() {
  const [cfg, setCfg] = useState<AppConfig>({
    openaiKey: "",
    supabaseUrl: "",
    supabaseAnonKey: "",
  });
  const [status, setStatus] = useState<{ kind: "ok" | "err"; text: string } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getConfig().then((c) => {
      if (c) setCfg(c);
      setLoading(false);
    });
  }, []);

  const save = async () => {
    setStatus(null);
    if (!cfg.openaiKey || !cfg.supabaseUrl || !cfg.supabaseAnonKey) {
      setStatus({ kind: "err", text: "All three fields are required." });
      return;
    }
    try {
      await setConfig(cfg);
      resetSupabase();
      setStatus({ kind: "ok", text: "Saved." });
    } catch (e) {
      setStatus({ kind: "err", text: String((e as Error).message ?? e) });
    }
  };

  if (loading) return <div className="container">Loading…</div>;

  return (
    <div className="container">
      <h1>Call Transcripter — Settings</h1>
      <p className="sub">Keys are stored locally in this browser only.</p>

      <label>OpenAI API key</label>
      <input
        type="password"
        placeholder="sk-…"
        value={cfg.openaiKey}
        onChange={(e) => setCfg({ ...cfg, openaiKey: e.target.value })}
      />
      <div className="hint">Used for Whisper transcription.</div>

      <label>Supabase project URL</label>
      <input
        type="text"
        placeholder="https://xxxx.supabase.co"
        value={cfg.supabaseUrl}
        onChange={(e) => setCfg({ ...cfg, supabaseUrl: e.target.value })}
      />

      <label>Supabase anon key</label>
      <input
        type="password"
        placeholder="eyJ…"
        value={cfg.supabaseAnonKey}
        onChange={(e) => setCfg({ ...cfg, supabaseAnonKey: e.target.value })}
      />
      <div className="hint">Run the SQL in supabase/migrations/0001_init.sql in your project first.</div>

      <div className="row">
        <button className="primary" onClick={save}>Save</button>
        {status && <span className={`status ${status.kind}`}>{status.text}</span>}
      </div>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
