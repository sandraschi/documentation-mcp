// Drop-in Listen button + provider/voice dropdowns. HOW TO VENDOR: copy into
// <your_webapp>/src/components/SpeechControls.tsx, fix the `speech.ts` import
// path, and use it wherever you have text to read aloud:
//
//   <SpeechControls apiBase={API_BASE} getText={() => currentArticleText} />
//
// `getText` may be sync (string) or async (Promise<string>) — call your own
// API to fetch the text right before speaking if you don't already have it
// loaded. Inline styles on purpose: no assumption about Tailwind/CSS setup in
// the repo this gets vendored into — replace with your own classes freely.

import { useEffect, useRef, useState } from "react";
import { speechApi, type VoiceProvider } from "../lib/speech"; // fix path after vendoring

const PROVIDER_KEY = "speech_crossconnect.provider";
const VOICE_KEY = "speech_crossconnect.voice";

function loadPref(key: string, fallback: string): string {
	try {
		return localStorage.getItem(key) ?? fallback;
	} catch {
		return fallback;
	}
}

function savePref(key: string, value: string) {
	try {
		localStorage.setItem(key, value);
	} catch {
		/* private mode / storage disabled — selection just won't persist */
	}
}

type Props = {
	apiBase: string;
	getText: () => string | Promise<string>;
	label?: string;
	/** Trim long text before sending — Gemini takes ~10-20s per short excerpt,
	 * so an unbounded article will feel broken, not just slow. Default 200. */
	maxChars?: number;
};

export function SpeechControls({
	apiBase,
	getText,
	label = "🔊 Listen",
	maxChars = 200,
}: Props) {
	const api = speechApi(apiBase);
	const audioRef = useRef<HTMLAudioElement>(null);
	const [providers, setProviders] = useState<VoiceProvider[]>([]);
	const [provider, setProvider] = useState(() => loadPref(PROVIDER_KEY, "gemini"));
	const [voice, setVoice] = useState(() => loadPref(VOICE_KEY, "default"));
	const [state, setState] = useState<"idle" | "loading" | "error">("idle");

	useEffect(() => {
		api
			.voices()
			.then((r) =>
				setProviders((r.data?.providers ?? []).filter((p) => p.status === "available")),
			)
			.catch(() => setProviders([]));
		// biome-ignore lint/correctness/useExhaustiveDependencies: `api` is a fresh
		// factory result each render, not stateful — apiBase is the real dependency.
	}, [apiBase]);

	const changeProvider = (name: string) => {
		setProvider(name);
		savePref(PROVIDER_KEY, name);
		setVoice("default");
		savePref(VOICE_KEY, "default");
	};
	const changeVoice = (v: string) => {
		setVoice(v);
		savePref(VOICE_KEY, v);
	};
	const currentVoices = providers.find((p) => p.name === provider)?.voices ?? [];

	const listen = async () => {
		setState("loading");
		try {
			const raw = await getText();
			const text = raw.slice(0, maxChars).trim();
			if (!text) throw new Error("No text to read.");
			const audio = audioRef.current;
			if (!audio) return;
			audio.src = api.speakWavUrl(text, provider, voice);
			await audio.play();
			setState("idle");
		} catch {
			setState("error");
		}
	};

	return (
		<div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 8 }}>
			<button type="button" onClick={listen} disabled={state === "loading"}>
				{state === "loading" ? "Synthesizing…" : label}
			</button>
			<select value={provider} onChange={(e) => changeProvider(e.target.value)} title="TTS provider">
				{providers.length === 0 && <option value={provider}>{provider}</option>}
				{providers.map((p) => (
					<option key={p.name} value={p.name}>
						{p.name}
					</option>
				))}
			</select>
			<select value={voice} onChange={(e) => changeVoice(e.target.value)} title="Voice/speaker">
				<option value="default">default</option>
				{currentVoices.map((v) => (
					<option key={v} value={v}>
						{v}
					</option>
				))}
			</select>
			{state === "error" && (
				<span style={{ color: "#f87171", fontSize: 12 }}>speech-mcp not reachable</span>
			)}
			{/* biome-ignore lint/a11y/useMediaCaption: TTS output has no source track to caption */}
			<audio ref={audioRef} hidden />
		</div>
	);
}
