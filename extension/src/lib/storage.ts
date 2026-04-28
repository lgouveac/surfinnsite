export interface AppConfig {
  openaiKey: string;
  supabaseUrl: string;
  supabaseAnonKey: string;
}

const KEY = "ct_config";

export async function getConfig(): Promise<AppConfig | null> {
  const res = await chrome.storage.local.get(KEY);
  return (res[KEY] as AppConfig) ?? null;
}

export async function setConfig(cfg: AppConfig): Promise<void> {
  await chrome.storage.local.set({ [KEY]: cfg });
}

export async function isConfigured(): Promise<boolean> {
  const cfg = await getConfig();
  return !!(cfg?.openaiKey && cfg?.supabaseUrl && cfg?.supabaseAnonKey);
}
