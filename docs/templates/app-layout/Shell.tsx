/**
 * SOTA AppLayout / Shell Template (2026)
 *
 * Fleet-standard sidebar + topbar layout.
 * Drop into any webapp. Customize NAV items and constants marked CUSTOMIZE.
 *
 * Requires: react, react-router-dom, lucide-react, framer-motion, zustand, clsx
 * Also requires: useZoom() hook and CSS variables in index.css (see companion files)
 */

import clsx from "clsx";
import { AnimatePresence, motion } from "framer-motion";
import {
	/* CUSTOMIZE: import icons used in nav */
	Activity,
	ChevronLeft,
	ChevronRight,
	HelpCircle,
	LayoutDashboard,
	MessageSquare,
	Settings,
	Terminal,
	Wrench,
} from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { create } from "zustand";

/* ── Connection store ─────────────────────────────────────────────────────── */

export const useConnection = create<{
	state: "connecting" | "connected" | "offline" | "error";
	lastError: string | null;
}>(() => ({ state: "connecting", lastError: null }));

/* ── Zoom hook ─────────────────────────────────────────────────────────────── */

/* CUSTOMIZE: paste use-zoom.ts content here or import from ../hooks/useZoom */
const ZOOM_LEVELS = [0.8, 1.0, 1.25, 1.5, 2.0, 3.0];

function useZoom() {
	const [zoomIndex, setZoomIndex] = useState(() => {
		try {
			const saved = localStorage.getItem("tauri-zoom");
			return saved ? ZOOM_LEVELS.indexOf(parseFloat(saved)) : 0;
		} catch {
			return 0;
		}
	});

	const applyZoom = useCallback(async (level: number) => {
		localStorage.setItem("tauri-zoom", String(level));
		try {
			const { getCurrentWindow } = await import("@tauri-apps/api/window");
			await getCurrentWindow().setZoom(level);
			return;
		} catch {
			/* dev browser — CSS zoom */
		}
		document.documentElement.style.zoom = String(level);
	}, []);

	useEffect(() => {
		const handler = (e: WheelEvent) => {
			if (!e.ctrlKey) return;
			e.preventDefault();
			setZoomIndex((prev) => {
				const next =
					e.deltaY < 0
						? Math.min(prev + 1, ZOOM_LEVELS.length - 1)
						: Math.max(prev - 1, 0);
				if (next !== prev) applyZoom(ZOOM_LEVELS[next]);
				return next;
			});
		};
		window.addEventListener("wheel", handler, { passive: false });
		const saved = localStorage.getItem("tauri-zoom");
		if (saved) applyZoom(parseFloat(saved));
		return () => window.removeEventListener("wheel", handler);
	}, [applyZoom]);
}

/* ── Health polling ────────────────────────────────────────────────────────── */

const HEALTH_BACKOFF = [1, 2, 4, 8, 16, 30];

/* CUSTOMIZE: set your backend port */
const BACKEND_PORT = 10946;
const HEALTH_URL = `http://127.0.0.1:${BACKEND_PORT}/api/health`;

/* ── Navigation items ──────────────────────────────────────────────────────── */

/* CUSTOMIZE: add/remove nav items for this repo */
const NAV = [
	{ to: "/", label: "Dashboard", icon: LayoutDashboard },
	{ to: "/chat", label: "Chat", icon: MessageSquare },
	{ to: "/tools", label: "Tools", icon: Wrench },
	{ to: "/status", label: "Status", icon: Activity },
	{ to: "/logs", label: "Logs", icon: Terminal },
	{ to: "/settings", label: "Settings", icon: Settings },
	{ to: "/help", label: "Help", icon: HelpCircle },
];

/* ── Shell component ───────────────────────────────────────────────────────── */

export function Shell({ children }: { children: React.ReactNode }) {
	useZoom();
	const [collapsed, setCollapsed] = useState(false);
	const location = useLocation();
	const attemptRef = useRef(0);
	const timerRef = useRef<ReturnType<typeof setTimeout>>();

	// Exponential backoff health check
	const tick = useCallback(async () => {
		try {
			const r = await fetch(HEALTH_URL, {
				signal: AbortSignal.timeout(5000),
			});
			if (r.ok) {
				useConnection.setState({ state: "connected" });
				attemptRef.current = 0;
			} else {
				useConnection.setState({ state: "offline", lastError: `HTTP ${r.status}` });
			}
		} catch (e) {
			useConnection.setState({
				state: "offline",
				lastError: (e as Error).message,
			});
		}
		attemptRef.current = Math.min(++attemptRef.current, HEALTH_BACKOFF.length - 1);
		timerRef.current = setTimeout(tick, HEALTH_BACKOFF[attemptRef.current] * 1000);
	}, []);

	useEffect(() => {
		tick();
		// Tauri event listener
		(async () => {
			try {
				const { listen } = await import("@tauri-apps/api/event");
				const unlisten = await listen<string>("backend-status", (event) => {
					if (event.payload === "ready") {
						useConnection.setState({ state: "connected" });
						attemptRef.current = 0;
					} else if (typeof event.payload === "string" && event.payload.startsWith("error:")) {
						useConnection.setState({ state: "error", lastError: event.payload });
					}
				});
				return () => {
					unlisten();
					clearTimeout(timerRef.current);
				};
			} catch {
				return () => clearTimeout(timerRef.current);
			}
		})();
		return () => clearTimeout(timerRef.current);
	}, [tick]);

	const { state, lastError } = useConnection();
	const statusColor =
		state === "connected"
			? "bg-green-500"
			: state === "connecting"
				? "bg-amber-500"
				: "bg-red-500";
	const statusLabel =
		state === "connected"
			? "Connected"
			: state === "connecting"
				? "Connecting..."
				: `Offline${lastError ? ` (${lastError.slice(0, 60)})` : ""}`;

	return (
		<div className="flex h-screen overflow-hidden bg-zinc-950">
			{/* Sidebar */}
			<motion.aside
				animate={{ width: collapsed ? 64 : 220 }}
				transition={{ type: "spring", stiffness: 400, damping: 40 }}
				className="flex-shrink-0 flex flex-col border-r border-zinc-800 bg-zinc-900 z-40"
			>
				{/* Logo area */}
				<div className="flex items-center gap-3 px-4 py-5 border-b border-zinc-800">
					<div className="w-8 h-8 rounded-lg flex items-center justify-center bg-amber-500/20 border border-amber-500/30 flex-shrink-0">
						<Activity className="w-4 h-4 text-amber-400" />
					</div>
					<AnimatePresence>
						{!collapsed && (
							<motion.div
								initial={{ opacity: 0, x: -8 }}
								animate={{ opacity: 1, x: 0 }}
								exit={{ opacity: 0, x: -8 }}
								className="overflow-hidden"
							>
								{/* CUSTOMIZE: app name + version */}
								<div className="text-sm font-semibold text-zinc-100 leading-tight">
									App Name
								</div>
								<div className="text-xs text-zinc-500">v0.1.0</div>
							</motion.div>
						)}
					</AnimatePresence>
				</div>

				{/* Collapse toggle — at TOP per fleet standard */}
				<button
					onClick={() => setCollapsed((c) => !c)}
					className="mx-2 mb-1 p-2 rounded-lg flex items-center justify-center text-zinc-500 hover:bg-zinc-800 transition-colors"
					title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
				>
					{collapsed ? (
						<ChevronRight className="w-4 h-4" />
					) : (
						<ChevronLeft className="w-4 h-4" />
					)}
				</button>

				{/* Navigation */}
				<nav className="flex-1 py-1 px-2 flex flex-col gap-0.5 overflow-y-auto">
					{NAV.map(({ to, label, icon: Icon }) => (
						<NavLink
							key={to}
							to={to}
							end={to === "/"}
							className={({ isActive }) =>
								clsx(
									"flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150",
									isActive
										? "bg-amber-500/10 text-amber-400"
										: "text-zinc-400 hover:bg-zinc-800",
								)
							}
							title={collapsed ? label : undefined}
						>
							<Icon className="w-4 h-4 flex-shrink-0" />
							<AnimatePresence>
								{!collapsed && (
									<motion.span
										initial={{ opacity: 0 }}
										animate={{ opacity: 1 }}
										exit={{ opacity: 0 }}
										className="truncate"
									>
										{label}
									</motion.span>
								)}
							</AnimatePresence>
						</NavLink>
					))}
				</nav>
			</motion.aside>

			{/* Main area */}
			<div className="flex-1 flex flex-col overflow-hidden">
				{/* Topbar */}
				<header
					className="flex items-center justify-between px-6 py-3 border-b border-zinc-800 bg-zinc-900 flex-shrink-0"
					data-testid="topbar"
				>
					<div className="flex items-center gap-4">
						<span className="text-sm font-medium text-zinc-400">
							{/* CUSTOMIZE: topbar title */}
							App Dashboard
						</span>
					</div>
					<div className="flex items-center gap-4">
						<div
							data-testid="backend-dot"
							className="flex items-center gap-2"
						>
							<div
								className={`w-2 h-2 rounded-full ${statusColor} animate-pulse-slow`}
							/>
							<span className="text-xs text-zinc-500">{statusLabel}</span>
						</div>
						<span className="text-xs font-mono text-zinc-600">
							{new Date().toLocaleTimeString()}
						</span>
					</div>
				</header>

				{/* Page content */}
				<main className="flex-1 overflow-y-auto p-6">
					<motion.div
						key={location.pathname}
						initial={{ opacity: 0, y: 6 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ duration: 0.18 }}
					>
						{children}
					</motion.div>
				</main>
			</div>
		</div>
	);
}
