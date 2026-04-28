export type ExtMessage =
  | { type: "DETECT_CALL"; url: string; tabId?: number }
  | { type: "START_RECORDING"; tabId: number; clientId: string | null; callUrl: string }
  | { type: "STOP_RECORDING" }
  | { type: "RECORDING_STATUS_REQUEST" }
  | { type: "RECORDING_STATUS"; isRecording: boolean; startedAt?: number; clientId?: string | null }
  | { type: "OFFSCREEN_AUDIO_READY"; durationSeconds: number; mimeType: string }
  | { type: "OFFSCREEN_ERROR"; message: string };
