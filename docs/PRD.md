# PRD — Call Transcripter

## 1. Visão geral
Extensão Chrome que detecta calls em andamento (Google Meet, Zoom Web, Teams Web), pergunta ao usuário se deseja gravar, associa a transcrição a um cliente (lista vinda do Supabase) e gera a transcrição via OpenAI Whisper. Permite cadastrar novos clientes direto na extensão.

## 2. Por que extensão Chrome
- `chrome.tabCapture` / `chrome.desktopCapture` capturam áudio da aba sem instalar nada extra.
- Sem bot entrando na reunião, sem app desktop separado, sem permissões de SO.
- Funciona em qualquer call que rode no navegador.

Alternativas descartadas: app Electron (overhead), bot recorder (Recall.ai etc — custo + complexidade), extensão Meet-only (limita escopo).

## 3. Personas e fluxo
**Usuário**: consultor/atendimento que faz várias calls por semana com clientes diferentes.

**Fluxo principal**:
1. Usuário abre Meet/Zoom/Teams. Extensão detecta a aba de call.
2. Popup pergunta: *"Gravar esta call?"* + dropdown de clientes (busca no Supabase) + botão "+ Novo cliente".
3. Se sim: começa a capturar áudio da aba.
4. Ao fim da call (usuário clica "Parar" ou aba fecha): áudio é enviado para OpenAI Whisper.
5. Transcrição é salva no Supabase, vinculada ao cliente, com timestamp e duração.
6. Notificação com link para ver/copiar a transcrição.

**Fluxo "+ Novo cliente"**: modal simples (nome, email opcional, notas) → insere em `clients` no Supabase → seleciona automaticamente.

## 4. Escopo MVP
### Inclui
- Detecção automática de calls (URLs: `meet.google.com`, `zoom.us/wc`, `teams.microsoft.com`).
- Prompt pré-call (gravar sim/não + selecionar cliente).
- Captura de áudio da aba via `chrome.tabCapture`.
- Upload chunked para OpenAI Whisper API (`whisper-1` ou `gpt-4o-transcribe`).
- CRUD básico de clientes (criar + listar; editar/deletar fica para v2).
- Storage de transcrições no Supabase com FK para cliente.
- Tela de configuração: chave OpenAI + URL/anon key Supabase.
- Tela de histórico: transcrições passadas, busca por cliente.

### Fora (v2+)
- Captura de microfone separado (gravar só o usuário).
- Resumo automático / extração de action items via GPT.
- Multi-usuário com auth (MVP é single-user, chave local).
- Diarização (separar quem falou).
- Integrações (Notion, Slack, CRM).

## 5. Arquitetura técnica

### Componentes
- **Extension (Manifest V3)**:
  - `background.js` (service worker): orquestra captura, upload, escrita no Supabase.
  - `content.js`: detecta estado da call (entrou, saiu) injetando em domínios de meeting.
  - `popup.html/tsx`: UI do prompt pré-call e seleção de cliente.
  - `options.html/tsx`: configuração de chaves.
  - `history.html/tsx`: lista de transcrições.
- **Supabase**: tabelas `clients` e `transcriptions`. RLS opcional no MVP (single-user).
- **OpenAI**: Whisper para STT. Chamada direta do background script (chave fica em `chrome.storage.local`).

### Schema Supabase
```sql
create table clients (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text,
  notes text,
  created_at timestamptz default now()
);

create table transcriptions (
  id uuid primary key default gen_random_uuid(),
  client_id uuid references clients(id) on delete set null,
  title text,
  transcript text not null,
  duration_seconds int,
  call_url text,
  recorded_at timestamptz default now()
);
```

### Captura de áudio
- `chrome.tabCapture.capture({ audio: true, video: false })` retorna `MediaStream`.
- `MediaRecorder` com `audio/webm; codecs=opus` em chunks de 30s.
- Cada chunk pode ir streaming pro Whisper, ou acumula e envia ao final (MVP: envia ao final, mais simples).
- Limite Whisper: 25MB/request → se passar, dividir antes de enviar.

### Segurança
- Chave OpenAI em `chrome.storage.local` (não sincroniza, fica só no device).
- Supabase: usar `anon key` + RLS, ou `service_role` se single-user local (avaliar).
- **Aviso de consentimento**: extensão deve mostrar lembrete pro usuário avisar os participantes antes de gravar (compliance LGPD/GDPR).

## 6. Stack proposta
- **Extension**: TypeScript + React + Vite (`@crxjs/vite-plugin`) + Tailwind.
- **Supabase JS client**: `@supabase/supabase-js`.
- **OpenAI**: fetch direto na API (`/v1/audio/transcriptions`), sem SDK pra manter bundle pequeno.

## 7. Estrutura de pastas
```
callTranscripter/
├── docs/
│   └── PRD.md
├── extension/
│   ├── src/
│   │   ├── background/
│   │   ├── content/
│   │   ├── popup/
│   │   ├── options/
│   │   ├── history/
│   │   └── lib/         # supabase client, openai client, storage
│   ├── manifest.json
│   └── vite.config.ts
├── supabase/
│   └── migrations/
└── package.json
```

## 8. Milestones
1. **M1 — Setup**: scaffold da extensão + Supabase + tela de options funcionando com chaves.
2. **M2 — Clientes**: CRUD mínimo (criar + listar) com Supabase.
3. **M3 — Captura**: detectar call, prompt pré-call, gravar áudio da aba, salvar local.
4. **M4 — Whisper**: enviar pro OpenAI, persistir transcrição vinculada ao cliente.
5. **M5 — Histórico**: tela de listagem + busca.
6. **M6 — Polish**: aviso de consentimento, error states, empty states, ícones.

## 9. Riscos / questões em aberto
- **Permissão de captura**: alguns domínios (Zoom desktop client) não rodam na aba — só Zoom Web funciona. Documentar.
- **Áudio só do remoto vs local**: `tabCapture` pega o áudio que SAI da aba (o que você ouve). Pra pegar seu microfone também, precisa combinar com `getUserMedia` e mixar. **Decidir**: MVP captura só áudio da aba, ou já mistura mic?
- **Custo Whisper**: ~$0.006/min. Uma call de 1h ≈ $0.36. OK pra MVP, mas mostrar uso.
- **Chrome Web Store**: publicar ou usar como unpacked? MVP unpacked, publicação depois.

## 10. Decisões confirmadas
1. **Áudio**: mic + remoto mixados (Web Audio API combina `tabCapture` stream + `getUserMedia` stream).
2. **Auth**: single-user local. Chaves no `chrome.storage.local`. Sem login Supabase no MVP.
3. **Domínios suportados no MVP**: Google Meet, Zoom Web, Microsoft Teams Web — todos.
