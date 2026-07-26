/**
 * SOTA Dashboard KPI Template (2026)
 *
 * Fleet-standard dashboard: stat cards, action buttons, recent items.
 *
 * Requires: react, lucide-react, framer-motion, @tanstack/react-query, date-fns
 * Customize: STAT_CARDS array, action buttons, items endpoint, health endpoint.
 */

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { formatDistanceToNow } from "date-fns";
import { motion } from "framer-motion";
import { useCallback, useEffect, useRef, useState } from "react";
import {
	Activity,
	AlertTriangle,
	Bell,
	FlaskConical,
	RefreshCw,
	TrendingUp,
	Zap,
} from "lucide-react";

/* CUSTOMIZE: API endpoints */
const BACKEND_PORT = 10946;
const API_BASE = `http://127.0.0.1:${BACKEND_PORT}`;
const HEALTH_BACKOFF = [1, 2, 4, 8, 16];

function apiFetch(path: string, options?: RequestInit) {
	return fetch(`${API_BASE}${path}`, options);
}

/* ── Data fetchers ─────────────────────────────────────────────────────────── */

/* CUSTOMIZE: replace with your repo's stats/items endpoints */
async function fetchStats() {
	const r = await apiFetch("/api/stats");
	return r.json();
}
async function fetchItems() {
	const r = await apiFetch("/api/items?hours=24&limit=10");
	return r.json();
}

/* CUSTOMIZE: replace action buttons */
const ACTIONS = [
	{ key: "poll", label: "Poll", icon: RefreshCw, endpoint: "/api/poll" },
	{ key: "process", label: "Process", icon: FlaskConical, endpoint: "/api/process" },
	{ key: "alerts", label: "Check Alerts", icon: Bell, endpoint: "/api/alerts/check", accent: true },
];

/* CUSTOMIZE: stat cards — add/remove per repo */
const STAT_CARDS: {
	key: string;
	label: string;
	color: string;
	icon: React.ComponentType<{ className?: string }>;
	testid: string;
}[] = [
	{ key: "active_items", label: "Active Items", color: "#3b82f6", icon: Activity, testid: "kpi-active" },
	{ key: "items_today", label: "New Today", color: "#22c55e", icon: TrendingUp, testid: "kpi-today" },
	{ key: "pending", label: "Pending", color: "#f59e0b", icon: Zap, testid: "kpi-pending" },
	{ key: "critical", label: "Critical", color: "#ef4444", icon: AlertTriangle, testid: "kpi-critical" },
];

export function Dashboard() {
	const qc = useQueryClient();
	const [backendOk, setBackendOk] = useState("starting");
	const attemptRef = useRef(0);
	const timerRef = useRef<ReturnType<typeof setTimeout>>();

	// Exponential backoff health polling
	useEffect(() => {
		let cancelled = false;
		const check = async () => {
			try {
				const r = await apiFetch("/api/health");
				if (cancelled) return;
				if (r.ok) {
					setBackendOk("connected");
					attemptRef.current = 0;
				} else setBackendOk("offline");
			} catch {
				if (!cancelled) setBackendOk("offline");
			}
			if (!cancelled) {
				attemptRef.current = Math.min(++attemptRef.current, HEALTH_BACKOFF.length - 1);
				timerRef.current = setTimeout(check, HEALTH_BACKOFF[attemptRef.current] * 1000);
			}
		};
		check();
		return () => {
			cancelled = true;
			clearTimeout(timerRef.current);
		};
	}, []);

	// Tauri event listener
	useEffect(() => {
		let unlisten: (() => void) | undefined;
		(async () => {
			try {
				const { listen } = await import("@tauri-apps/api/event");
				unlisten = await listen<string>("backend-status", (ev) => {
					if (ev.payload === "ready") {
						setBackendOk("connected");
						attemptRef.current = 0;
					} else if (typeof ev.payload === "string" && ev.payload.startsWith("error:"))
						setBackendOk("offline");
				});
			} catch {
				/* not in Tauri */
			}
		})();
		return () => {
			if (unlisten) unlisten();
		};
	}, []);

	const { data: stats } = useQuery({
		queryKey: ["stats"],
		queryFn: fetchStats,
		refetchInterval: 30_000,
	});

	const { data: items } = useQuery({
		queryKey: ["items"],
		queryFn: fetchItems,
		refetchInterval: 60_000,
	});

	const restartBackend = useCallback(async () => {
		try {
			const { invoke } = await import("@tauri-apps/api/core");
			await invoke("start_backend");
		} catch {
			/* not in Tauri */
		}
	}, []);

	return (
		<div data-testid="dashboard" className="space-y-6 max-w-6xl">
			{/* Header */}
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-2xl font-semibold tracking-tight text-zinc-100">
						Dashboard
					</h1>
					<p className="text-sm mt-0.5 text-zinc-500">
						Overview and quick actions
					</p>
				</div>
				<div className="flex gap-2">
					{ACTIONS.map(({ key, label, icon: Icon, endpoint, accent }) => {
						const mutation = qc.getMutationCache().find({ mutationKey: [key] });
						const isPending = mutation?.state.status === "pending";
						const mutate = async () => {
							try {
								await apiFetch(endpoint, { method: "POST" });
								qc.invalidateQueries();
							} catch {
								/* ignore */
							}
						};
						return (
							<button
								key={key}
								onClick={mutate}
								disabled={isPending}
								className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all border disabled:opacity-50 ${
									accent
										? "bg-red-500/15 text-red-400 border-red-500/30"
										: "bg-zinc-800 text-zinc-400 border-zinc-700 hover:bg-zinc-700"
								}`}
							>
								{isPending ? (
									<RefreshCw className="w-4 h-4 animate-spin" />
								) : (
									<Icon className="w-4 h-4" />
								)}
								{label}
							</button>
						);
					})}
				</div>
			</div>

			{/* Backend status */}
			<div className="flex items-center gap-2 text-xs text-zinc-500">
				<div
					data-testid="backend-status"
					className={`w-2 h-2 rounded-full ${
						backendOk === "starting"
							? "bg-yellow-500"
							: backendOk === "connected"
								? "bg-green-500"
								: "bg-red-500"
					}`}
				/>
				<span>
					{backendOk === "starting"
						? "Connecting..."
						: backendOk === "connected"
							? "Connected"
							: "Offline"}
				</span>
				{backendOk === "offline" && (
					<button
						onClick={restartBackend}
						className="ml-2 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-red-500/10 border border-red-500/20 text-red-400 hover:bg-red-500/20 transition-colors"
					>
						Restart
					</button>
				)}
			</div>

			{/* KPI cards */}
			<div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
				{STAT_CARDS.map(({ key, label, color, icon: Icon, testid }, i) => (
					<motion.div
						key={key}
						data-testid={testid}
						initial={{ opacity: 0, y: 12 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ delay: i * 0.05 }}
						className="rounded-xl p-4 border border-zinc-800 bg-zinc-900"
					>
						<div className="flex items-start justify-between mb-3">
							<div
								className="w-8 h-8 rounded-lg flex items-center justify-center"
								style={{
									background: `${color}20`,
									border: `1px solid ${color}40`,
								}}
							>
								<Icon className="w-4 h-4" style={{ color }} />
							</div>
						</div>
						<div className="text-2xl font-semibold font-mono text-zinc-100">
							{stats?.[key] ?? "—"}
						</div>
						<div className="text-xs mt-1 text-zinc-500">{label}</div>
					</motion.div>
				))}
			</div>

			{/* Recent items */}
			<div className="rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden">
				<div className="px-5 py-4 border-b border-zinc-800 flex items-center justify-between">
					<span className="text-sm font-semibold text-zinc-100">
						Recent Items
					</span>
					<span className="text-xs text-zinc-500">sorted by recency</span>
				</div>
				<div className="divide-y divide-zinc-800">
					{!items?.items?.length ? (
						<div className="px-5 py-8 text-center text-sm text-zinc-500">
							No items yet.
						</div>
					) : (
						items.items.map((item: any, i: number) => (
							<div
								key={item.id ?? i}
								className="px-5 py-3.5 flex items-start gap-4 hover:bg-zinc-800/40 transition-colors"
							>
								<div className="flex-1 min-w-0">
									<div className="text-sm font-medium text-zinc-200 truncate">
										{item.title ?? "(no title)"}
									</div>
									{item.summary && (
										<p className="text-xs mt-1 text-zinc-400 line-clamp-2">
											{item.summary}
										</p>
									)}
									{item.fetched_at && (
										<span className="text-xs text-zinc-600 mt-1 block">
											{formatDistanceToNow(new Date(item.fetched_at), {
												addSuffix: true,
											})}
										</span>
									)}
								</div>
							</div>
						))
					)}
				</div>
			</div>
		</div>
	);
}
