-- Call Transcripter — initial schema
-- Single-user MVP. RLS off; tighten before multi-user.

create extension if not exists "pgcrypto";

create table if not exists clients (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text,
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists transcriptions (
  id uuid primary key default gen_random_uuid(),
  client_id uuid references clients(id) on delete set null,
  title text,
  transcript text not null,
  duration_seconds int,
  call_url text,
  recorded_at timestamptz not null default now()
);

create index if not exists transcriptions_client_id_idx on transcriptions(client_id);
create index if not exists transcriptions_recorded_at_idx on transcriptions(recorded_at desc);
