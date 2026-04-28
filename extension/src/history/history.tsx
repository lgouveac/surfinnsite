import { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { listClients, listTranscriptions, type Client, type Transcription } from "../lib/supabase";

type Row = Transcription & { client?: Client | null };

function formatDuration(s: number | null | undefined): string {
  if (!s) return "—";
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${m}m ${r}s`;
}

function App() {
  const [rows, setRows] = useState<Row[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [filter, setFilter] = useState<string>("");
  const [search, setSearch] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const [t, c] = await Promise.all([listTranscriptions(), listClients()]);
        setRows(t);
        setClients(c);
      } catch (e) {
        setError((e as Error).message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const filtered = useMemo(() => {
    return rows.filter((r) => {
      if (filter && r.client_id !== filter) return false;
      if (search && !(r.transcript.toLowerCase().includes(search.toLowerCase()) ||
                      r.client?.name?.toLowerCase().includes(search.toLowerCase()))) return false;
      return true;
    });
  }, [rows, filter, search]);

  const copy = (text: string) => navigator.clipboard.writeText(text).catch(() => {});

  return (
    <div className="container">
      <header>
        <h1>Call history</h1>
        <div className="controls">
          <input
            placeholder="Search transcripts…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="">All clients</option>
            {clients.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>
      </header>

      {error && <div className="error">{error}</div>}
      {loading && <div className="empty">Loading…</div>}
      {!loading && !error && filtered.length === 0 && (
        <div className="empty">No transcriptions yet.</div>
      )}

      <div className="list">
        {filtered.map((r) => (
          <div className="card" key={r.id}>
            <header>
              <div>
                <div className="title">{r.client?.name ?? "Unassigned"}</div>
                <div className="meta">
                  {new Date(r.recorded_at).toLocaleString()} · {formatDuration(r.duration_seconds)}
                  {r.call_url && ` · ${new URL(r.call_url).hostname}`}
                </div>
              </div>
              <button className="copy-btn" onClick={() => copy(r.transcript)}>Copy</button>
            </header>
            <div className="transcript">{r.transcript}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
