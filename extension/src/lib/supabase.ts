import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { getConfig } from "./storage";

export interface Client {
  id: string;
  name: string;
  email: string | null;
  notes: string | null;
  created_at: string;
}

export interface Transcription {
  id: string;
  client_id: string | null;
  title: string | null;
  transcript: string;
  duration_seconds: number | null;
  call_url: string | null;
  recorded_at: string;
}

let cached: SupabaseClient | null = null;

export async function getSupabase(): Promise<SupabaseClient> {
  if (cached) return cached;
  const cfg = await getConfig();
  if (!cfg?.supabaseUrl || !cfg?.supabaseAnonKey) {
    throw new Error("Supabase not configured. Open the options page.");
  }
  cached = createClient(cfg.supabaseUrl, cfg.supabaseAnonKey, {
    auth: { persistSession: false },
  });
  return cached;
}

export function resetSupabase(): void {
  cached = null;
}

export async function listClients(): Promise<Client[]> {
  const sb = await getSupabase();
  const { data, error } = await sb
    .from("clients")
    .select("*")
    .order("name", { ascending: true });
  if (error) throw error;
  return (data ?? []) as Client[];
}

export async function createClient_(input: {
  name: string;
  email?: string;
  notes?: string;
}): Promise<Client> {
  const sb = await getSupabase();
  const { data, error } = await sb
    .from("clients")
    .insert({
      name: input.name,
      email: input.email || null,
      notes: input.notes || null,
    })
    .select()
    .single();
  if (error) throw error;
  return data as Client;
}

export async function saveTranscription(input: {
  client_id: string | null;
  title?: string | null;
  transcript: string;
  duration_seconds?: number | null;
  call_url?: string | null;
}): Promise<Transcription> {
  const sb = await getSupabase();
  const { data, error } = await sb
    .from("transcriptions")
    .insert({
      client_id: input.client_id,
      title: input.title ?? null,
      transcript: input.transcript,
      duration_seconds: input.duration_seconds ?? null,
      call_url: input.call_url ?? null,
    })
    .select()
    .single();
  if (error) throw error;
  return data as Transcription;
}

export async function listTranscriptions(filter?: {
  clientId?: string;
}): Promise<(Transcription & { client?: Client | null })[]> {
  const sb = await getSupabase();
  let q = sb
    .from("transcriptions")
    .select("*, client:clients(*)")
    .order("recorded_at", { ascending: false });
  if (filter?.clientId) q = q.eq("client_id", filter.clientId);
  const { data, error } = await q;
  if (error) throw error;
  return (data ?? []) as (Transcription & { client?: Client | null })[];
}
