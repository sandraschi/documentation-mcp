// Wake-word listener toggle. Deliberately a SEPARATE component from
// MicButton, because it is a genuinely different feature, not a variant of
// the same one:
//
//   MicButton         per-browser-tab STT, request-scoped, browser mic.
//   WakeWordToggle    starts a background thread on whatever MACHINE runs
//                     speech-mcp, listening on THAT machine's own microphone,
//                     until you stop it. Has no per-request lifetime and no
//                     built-in way to notify a specific browser tab when the
//                     keyword fires. On detection it either routes to
//                     speech-mcp's Fleet Voice Command Bus (if speech-mcp has
//                     FLEET_VOICE_DELEGATE=1) or just logs server-side.
//
// In short: this is closer to "flip on Hey Siri on that computer" than a
// webapp voice-input control. Don't present it as a lightweight toggle next
// to MicButton without the distinction being visible to the user — that's
// what the warning copy below is for, don't remove it when you adapt this.
//
// HOW TO VENDOR: copy into <your_webapp>/src/components/WakeWordToggle.tsx,
// fix the `speech.ts` import path.

import { useCallback, useEffect, useState } from "react";
import { type WakeWordStatus, speechApi } from "../lib/speech"; // fix path after vendoring

type Props = {
	apiBase: string;
	defaultKeyword?: string;
};

export function WakeWordToggle({
	apiBase,
	defaultKeyword = "hey_jarvis",
}: Props) {
	const [keyword, setKeyword] = useState(defaultKeyword);
	const [status, setStatus] = useState<WakeWordStatus | null>(null);
	const [busy, setBusy] = useState(false);
	const [error, setError] = useState("");

	const refresh = useCallback(() => {
		speechApi(apiBase)
			.wakeWord("status")
			.then((r) => setStatus(r.data))
			.catch(() => setStatus(null));
	}, [apiBase]);

	useEffect(() => {
		refresh();
	}, [refresh]);

	const toggle = async () => {
		setBusy(true);
		setError("");
		try {
			const action = status?.listening ? "stop" : "start";
			const r = await speechApi(apiBase).wakeWord(action, { keyword });
			if (!r.success) {
				setError(r.message);
			} else {
				setStatus(r.data);
			}
		} catch (e) {
			setError(e instanceof Error ? e.message : String(e));
		} finally {
			setBusy(false);
		}
	};

	const listening = !!status?.listening;

	return (
		<div
			style={{ display: "flex", flexDirection: "column", gap: 6, fontSize: 13 }}
		>
			<p style={{ margin: 0, color: "#f59e0b" }}>
				Starts a MICROPHONE listener on the machine running speech-mcp — not
				this browser tab. Turn it off when you're done, same as any always-on
				mic.
			</p>
			<div
				style={{
					display: "flex",
					flexWrap: "wrap",
					alignItems: "center",
					gap: 8,
				}}
			>
				<input
					value={keyword}
					onChange={(e) => setKeyword(e.target.value)}
					disabled={listening}
					placeholder="wake keyword"
					style={{ width: "10rem" }}
				/>
				<button type="button" onClick={toggle} disabled={busy}>
					{busy
						? "..."
						: listening
							? `Listening for "${status?.keyword}" — Stop`
							: "Start listening"}
				</button>
				<button type="button" onClick={refresh} title="Refresh status">
					↻
				</button>
				{status?.fleet_delegate && (
					<span style={{ color: "#22c55e" }}>fleet voice bus active</span>
				)}
			</div>
			{error && <span style={{ color: "#f87171" }}>{error}</span>}
		</div>
	);
}
