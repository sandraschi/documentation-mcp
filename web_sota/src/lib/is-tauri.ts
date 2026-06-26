/** Check if code is running inside a Tauri WebView (not a regular browser). */
export function isTauri(): boolean {
  return (
    typeof window !== "undefined" &&
    (window as unknown as Record<string, unknown>).__TAURI_INTERNALS__ !== undefined
  );
}
