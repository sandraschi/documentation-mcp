// Frontend client for speech_routes.py. Built on crossconnect.ts's
// crossconnectPeer() — read ../../CROSSCONNECT_PATTERN.md before adding a
// second peer integration to your webapp.
//
// HOW TO VENDOR:
// 1. Vendor crossconnect.ts first (../crossconnect-base/crossconnect.ts) into
//    the same lib/ directory as this file — it's peer-agnostic, shared by
//    every adapter you add.
// 2. Copy this file into <your_webapp>/src/lib/speech.ts, then:
//
//      import { speechApi } from "./speech";
//      export const speech = speechApi(API_BASE); // your existing backend base URL
//
//    Or just import { speechApi } directly wherever you need it — it's a
//    plain factory function, no framework dependency.

import { crossconnectPeer } from "./crossconnect"; // fix path after vendoring

export interface VoiceProvider {
	name: string;
	status: string;
	voices: string[];
}

export interface WakeWordStatus {
	success: boolean;
	listening?: boolean;
	status?: string;
	engine?: string;
	keyword?: string;
	fleet_delegate?: boolean;
	error?: string;
}

export function speechApi(apiBase: string) {
	const peer = crossconnectPeer(apiBase, "/api/speech");
	return {
		voices: () => peer.get<{ providers: VoiceProvider[] }>("/voices"),
		/** Direct URL for an <audio> tag — proxied through your backend, so no
		 * CORS/port wiring needed in the browser. Defaults to Gemini over Windows
		 * SAPI (voice quality); Gemini takes ~10-20s for a short excerpt — size
		 * your UI's "loading" state and your excerpt length accordingly. */
		speakWavUrl: (text: string, provider = "gemini", voiceId = "default") =>
			peer.binaryUrl("/speak.wav", { text, provider, voice_id: voiceId }),
		/** start/stop/status of speech-mcp's MACHINE-WIDE background wake-word
		 * listener — NOT per-browser-tab STT, see WakeWordToggle.tsx's warning
		 * copy and speech_crossconnect.py's wake_word() docstring before using
		 * this for anything other than a clearly-labeled global toggle. */
		wakeWord: (
			action: "start" | "stop" | "status",
			opts?: { keyword?: string; sleepKeyword?: string; sensitivity?: number },
		) =>
			peer.post<WakeWordStatus>("/wake_word", {
				action,
				keyword: opts?.keyword ?? "hey_jarvis",
				sleep_keyword: opts?.sleepKeyword,
				sensitivity: opts?.sensitivity ?? 0.5,
			}),
	};
}
