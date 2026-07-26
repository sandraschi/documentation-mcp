/**
 * SOTA Logs Page Template (2026)
 *
 * Fleet-standard MCP JSON-RPC log viewer with filter, search, auto-scroll.
 *
 * Requires: react, lucide-react, framer-motion, @tanstack/react-query
 */

import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { useCallback, useEffect, useRef, useState } from "react";
import {
	AlertCircle,
	CheckCircle2,
	Info,
	RefreshCw,
	Search,
	Terminal,
	XCircle,
} from "lucide-react";

/* CUSTOMIZE: API endpoints and polling interval */
const BACKEND_PORT = 10946;
const API_BASE = `http://127.0.0.1:${BACKEND_PORT}`;
const POLL_INTERVAL = 10_000;

/* ── Types ──────────────────────────────────────────────────────────────────── */

interface LogEntry {
	timestamp: string;
	level: string;
	message: string;
	source?: string;
}

/* ── Level helpers ─────────────────────────────────────────────────────────── */

const LEVEL_ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
	info: Info,
	warn: AlertCircle,
	error: XCircle,
	debug: Terminal,
	success: CheckCircle2,
};

const LEVEL_COLORS: Record<string, string> = {
	info: "text-blue-400",
	warn: "text-amber-400",
	error: "text-red-400",
	debug: "text-zinc-500",
	success: "text-green-400",
};

const LEVEL_BG: Record<string, string> = {
	info: "bg-blue-500/10 border-blue-500/20",
	warn: "bg-amber-500/10 border-amber-500/20",
	error: "bg-red-500/10 border-red-500/20",
	debug: "bg-zinc-800/50 border-zinc-700/50",
	success: "bg-green-500/10 border-green-500/20",
};

/* ── Component ─────────────────────────────────────────────────────────────── */

export function LogsPage() {
	const [levelFilter, setLevelFilter] = useState<string>("all");
	const [search, setSearch] = useState("");
	const [autoScroll, setAutoScroll] = useState(true);
	const scrollRef = useRef<HTMLDivElement>(null);

	const { data, isLoading, refetch } = useQuery({
		queryKey: ["logs"],
		queryFn: async () => {
			/* CUSTOMIZE: replace with your log endpoint */
			const r = await fetch(`${API_BASE}/api/logs`);
			if (!r.ok) throw new Error(`HTTP ${r.status}`);
			return r.json() as Promise<{ logs: LogEntry[] }>;
		},
		refetchInterval: POLL_INTERVAL,
	});

	const logs = data?.logs ?? [];

	const filtered = logs.filter((entry) => {
		if (levelFilter !== "all" && entry.level !== levelFilter) return false;
		if (search && !entry.message.toLowerCase().includes(search.toLowerCase()))
			return false;
		return true;
	});

	const handleScroll = useCallback(() => {
		if (!scrollRef.current) return;
		const { scrollTop, scrollHeight, clientHeight } = scrollRef.current;
		setAutoScroll(scrollHeight - scrollTop - clientHeight < 100);
	}, []);

	useEffect(() => {
		if (autoScroll && scrollRef.current) {
			scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
		}
	}, [filtered, autoScroll]);

	const levels = ["all", ...new Set(logs.map((l) => l.level))];

	return (
		<div data-testid="logs-page" className="flex flex-col h-[calc(100vh-8rem)] max-w-6xl mx-auto">
			{/* Header + controls */}
			<div className="flex items-center justify-between mb-4" data-testid="logs-controls">
				<h1 className="text-2xl font-bold text-zinc-100 flex items-center gap-3">
					<Terminal className="text-zinc-400" /> Logs
				</h1>
				<div className="flex items-center gap-3">
					{/* Level filter */}
					<div className="flex gap-1 bg-zinc-900 rounded-lg p-1 border border-zinc-800">
						{levels.map((lv) => (
							<button
								key={lv}
								onClick={() => setLevelFilter(lv)}
								className={`px-2.5 py-1 text-xs rounded-md transition-colors capitalize ${
									levelFilter === lv
										? "bg-zinc-700 text-zinc-200"
										: "text-zinc-500 hover:text-zinc-300"
								}`}
							>
								{lv === "all" ? "All" : lv}
								{lv !== "all" && (
									<span className="ml-1 opacity-60">
										{logs.filter((e) => e.level === lv).length}
									</span>
								)}
							</button>
						))}
					</div>

					{/* Search */}
					<div className="relative">
						<Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-500" />
						<input
							type="text"
							value={search}
							onChange={(e) => setSearch(e.target.value)}
							placeholder="Search logs…"
							data-testid="logs-search"
							className="bg-zinc-900 border border-zinc-800 rounded-lg pl-8 pr-3 py-1.5 text-xs text-zinc-200 placeholder-zinc-500 outline-none focus:border-zinc-600 w-48"
						/>
					</div>

					<button
						onClick={() => refetch()}
						disabled={isLoading}
						className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 transition-colors"
						title="Refresh"
					>
						<RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
					</button>

					<label className="flex items-center gap-1.5 text-xs text-zinc-500 cursor-pointer">
						<input
							type="checkbox"
							checked={autoScroll}
							onChange={(e) => setAutoScroll(e.target.checked)}
							className="rounded border-zinc-600 bg-zinc-900"
						/>
						Auto-scroll
					</label>
				</div>
			</div>

			{/* Log entries */}
			<div
				data-testid="logs-entries"
				ref={scrollRef}
				onScroll={handleScroll}
				className="flex-1 overflow-y-auto font-mono text-xs space-y-0.5"
			>
				{filtered.length === 0 && (
					<div className="flex items-center justify-center h-full text-zinc-600 text-sm">
						{isLoading ? "Loading logs…" : "No matching log entries."}
					</div>
				)}
				{filtered.map((entry, i) => {
					const Icon = LEVEL_ICONS[entry.level] ?? Info;
					const color = LEVEL_COLORS[entry.level] ?? "text-zinc-400";
					const bg = LEVEL_BG[entry.level] ?? "bg-zinc-800/30";
					return (
						<motion.div
							key={i}
							initial={{ opacity: 0 }}
							animate={{ opacity: 1 }}
							className={`flex items-start gap-3 px-4 py-1.5 rounded border ${bg}`}
						>
							<Icon className={`w-3.5 h-3.5 mt-0.5 shrink-0 ${color}`} />
							<span className="text-zinc-500 shrink-0 w-20">
								{entry.timestamp?.slice(11, 23) ?? ""}
							</span>
							{entry.source && (
								<span className="text-zinc-600 shrink-0 w-24 truncate">
									{entry.source}
								</span>
							)}
							<span className={`${color} break-words`}>
								{entry.message}
							</span>
						</motion.div>
					);
				})}
			</div>
		</div>
	);
}
