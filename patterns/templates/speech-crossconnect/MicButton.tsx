// Mic input button — browser-native Web Speech API STT, vendored (and
// generalized) from the fleet's older templates/speech/MicButton.tsx.
//
// This does NOT go through crossconnect.ts/speech.ts and does not call
// speech-mcp at all — the browser's own SpeechRecognition API needs no
// backend proxy. speech-mcp DOES have its own STT (FunASR batch,
// sherpa-onnx streaming) but that's a file-upload / websocket-streaming
// flow, not a drop-in mic button — see speech-mcp's docs/STREAMING_ASR.md
// if you need that instead of (or as well as) this browser-native path.
//
// Tradeoffs of the browser-native approach, so you can decide if it's
// right for your repo:
//   - Zero backend dependency — works even if speech-mcp isn't running.
//   - Chrome/Edge only. Safari and Firefox have no SpeechRecognition;
//     isSttAvailable() returns false there and the button renders nothing.
//   - Chrome sends the audio to Google's servers under the hood to do the
//     recognition — same privacy tradeoff as any browser STT, not
//     specific to this component, but worth knowing before you ship it.
//
// HOW TO VENDOR: copy into <your_webapp>/src/components/MicButton.tsx.

import { useEffect, useRef, useState } from "react";

interface SpeechRecognitionEvent extends Event {
	resultIndex: number;
	results: SpeechRecognitionResultList;
}
interface SpeechRecognition extends EventTarget {
	continuous: boolean;
	interimResults: boolean;
	lang: string;
	onresult: (event: SpeechRecognitionEvent) => void;
	onend: () => void;
	onerror: (event: Event) => void;
	start: () => void;
	stop: () => void;
	abort: () => void;
}
interface SpeechRecognitionConstructor {
	new (): SpeechRecognition;
}
declare global {
	interface Window {
		SpeechRecognition?: SpeechRecognitionConstructor;
		webkitSpeechRecognition?: SpeechRecognitionConstructor;
	}
}

const RecognitionCtor: SpeechRecognitionConstructor | undefined =
	typeof window !== "undefined"
		? window.SpeechRecognition || window.webkitSpeechRecognition
		: undefined;

export function isSttAvailable(): boolean {
	return !!RecognitionCtor;
}

type Props = {
	/** Called with the live transcript as the user speaks. `isFinal` marks the
	 * end of one recognized phrase — Web Speech API fires several times per
	 * phrase while `continuous` is on (interim results), then once more with
	 * isFinal=true. Typical use: setInput(transcript) on every call. */
	onResult: (transcript: string, isFinal: boolean) => void;
	/** Called when recognition stops, for any reason (user stopped it, an
	 * error, or the browser ended the session on its own). */
	onEnd?: () => void;
	label?: string;
};

/** Renders nothing if the browser has no SpeechRecognition (Safari, Firefox,
 * or a non-browser environment) — check isSttAvailable() yourself first if
 * you want different fallback UI instead of nothing. */
export function MicButton({ onResult, onEnd, label = "🎤" }: Props) {
	const [listening, setListening] = useState(false);
	const recognitionRef = useRef<SpeechRecognition | null>(null);

	useEffect(() => {
		return () => {
			recognitionRef.current?.abort();
		};
	}, []);

	if (!RecognitionCtor) return null;

	const toggle = () => {
		if (listening) {
			recognitionRef.current?.stop();
			return;
		}
		const Ctor = RecognitionCtor;
		if (!Ctor) return;
		const recognition = new Ctor();
		recognition.continuous = true;
		recognition.interimResults = true;
		recognition.lang = navigator.language || "en-US";
		recognition.onresult = (e: SpeechRecognitionEvent) => {
			let transcript = "";
			for (let i = e.resultIndex; i < e.results.length; i++) {
				transcript += e.results[i][0].transcript;
			}
			onResult(transcript, e.results[e.results.length - 1].isFinal);
		};
		recognition.onend = () => {
			setListening(false);
			onEnd?.();
		};
		recognition.onerror = () => {
			setListening(false);
			onEnd?.();
		};
		recognitionRef.current = recognition;
		try {
			recognition.start();
			setListening(true);
		} catch {
			setListening(false);
		}
	};

	return (
		<button
			type="button"
			onClick={toggle}
			title={listening ? "Stop listening" : "Start voice input"}
			style={listening ? { color: "#ef4444" } : undefined}
		>
			{listening ? "⏺" : label}
		</button>
	);
}
