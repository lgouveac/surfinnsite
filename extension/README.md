# Call Transcripter — Chrome Extension

Records browser calls (Google Meet, Zoom Web, Microsoft Teams Web), mixes tab audio + microphone, transcribes via OpenAI Whisper, and stores results in Supabase linked to a client.

See [PRD](../docs/PRD.md) for the full spec.

## Setup

### 1. Supabase

Create a Supabase project, then run [`supabase/migrations/0001_init.sql`](../supabase/migrations/0001_init.sql) in the SQL editor. Two tables are created: `clients` and `transcriptions`.

### 2. Build the extension

```bash
cd extension
npm install
npm run build
```

This produces `extension/dist/`.

### 3. Load it in Chrome

1. Go to `chrome://extensions`.
2. Enable **Developer mode** (top right).
3. Click **Load unpacked** and pick the `extension/dist` folder.

### 4. Configure

Click the extension icon → **Settings**, fill in:
- OpenAI API key (used for Whisper)
- Supabase project URL
- Supabase anon key

Keys are stored in `chrome.storage.local` — never leaves the browser.

## Usage

1. Open a Meet/Zoom Web/Teams call.
2. Click the extension icon.
3. Pick a client (or `+ New client`) and hit **Start recording**.
4. Grant microphone permission when prompted.
5. When the call ends, click **Stop & transcribe**.
6. Audio uploads to Whisper, transcript saves to Supabase. A notification opens the **History** page when done.

## Notes

- **Consent**: tell participants you're recording. Compliance (LGPD/GDPR) is your responsibility.
- **Audio**: tab audio + your mic are mixed into one track. Whisper has no diarization in MVP.
- **Whisper limit**: 25MB per request (~25 min of opus audio). Longer calls will fail in MVP — chunking is v2.
- **Single user**: chaves locais, sem auth Supabase. Multi-user é v2.

## Dev

```bash
npm run dev
```

The CRX Vite plugin watches and reloads. Reload the extension in `chrome://extensions` after big changes.
