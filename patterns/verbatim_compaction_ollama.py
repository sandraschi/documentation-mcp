"""Verbatim compaction with a local Ollama scorer (no TypeSafe key).

Port of tamaratran/fast-jev-compaction core idea, minus the vendor:
never rewrites anything, only drops tool calls / tool results a local
model says are stale. Whole conversation is sent as state, oldest first,
results replaced by short notes. User + assistant text stays verbatim.

Stdlib only. Measured 2026-09-19 on Goliath:
- heuristic (default): 93% char reduction on demo transcript, ~1ms, no network.
- LM Studio live scorer: plumbing verified (deephermes-3-llama-3-8b: 12.6s,
  hedged 0.5 everywhere -> 0% reduction; qwen 27b: >120s first-load timeout).
- Ollama: BROKEN that day (llama-server.exe missing from install dir, 500 on
  /api/chat for every model). Reinstall Ollama before trusting --backend ollama.

  python patterns/verbatim_compaction_ollama.py --demo --backend heuristic
  python patterns/verbatim_compaction_ollama.py --demo --backend lmstudio --model deephermes-3-llama-3-8b-preview
  python patterns/verbatim_compaction_ollama.py --demo --backend ollama --model mistral-nemo:12b

Importable too:
  from verbatim_compaction_ollama import compact, OllamaAsker
  result = compact(messages, OllamaAsker(model="mistral-nemo:12b"))
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import copy
import json
import re
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# --------------------------------------------------------------------------
# Token estimation (faithful port of state.ts: word/6 letters, digit/2, other 0.9)
# --------------------------------------------------------------------------

_TOKEN_PIECES = re.compile(r"[A-Za-z]+|\d+|[^\sA-Za-z\d]")


def estimate_tokens(text: str) -> int:
    tokens = 0.0
    for m in _TOKEN_PIECES.finditer(text):
        piece = m.group(0)
        first = ord(piece[0])
        if 48 <= first <= 57:  # digit run
            tokens += len(piece) / 2.0
        elif (65 <= first <= 90) or (97 <= first <= 122):  # word
            tokens += 1 + (len(piece) - 1) // 6
        else:
            tokens += 0.9
    return int(__import__("math").ceil(tokens)) if tokens else 0


def truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: max(0, limit - 1)] + "\u2026"


def abridge(text: str, head: int = 400, tail: int = 150) -> str:
    if len(text) <= head + tail + 40:
        return text
    omitted = len(text) - head - tail
    return f"{text[:head]}\n[\u2026 {omitted} chars omitted \u2026]\n{text[-tail:]}"


STATE_CONTEXT = (
    "A coding assistant conversation is being compacted to free context. "
    "`history` is the whole conversation so far, oldest first; tool outputs are "
    "replaced by a short `result` note and long texts may be abridged. Each question "
    "asks whether one tool call, or the full output of that call, still needs to stay "
    "in the history verbatim. Whatever is not kept is deleted permanently, but the "
    "assistant can always re-run a tool or re-read a file."
)

INPUT_CHARS = (1000, 200, 60)
TEXT_HEAD, TEXT_TAIL = 400, 150
REQUEST_OVERHEAD_TOKENS = 20


@dataclass
class ToolCall:
    id: str  # t1, t2, ...
    tool_use_id: str
    tool: str
    input: Dict[str, Any]
    call_index: int
    result_index: int
    result_chars: int
    is_error: bool
    pinned: bool


@dataclass
class Options:
    goal: str = ""
    keep_threshold: float = 0.5
    preserve_recent_messages: int = 6
    max_state_tokens: int = 25000
    max_request_tokens: int = 30000
    truncate_head_chars: int = 300


def is_pinned(index: int, total: int, preserve: int) -> bool:
    return index == 0 or index >= total - preserve


def collect_tool_calls(messages: List[Dict[str, Any]], preserve: int) -> List[ToolCall]:
    results: Dict[str, Tuple[int, Dict[str, Any]]] = {}
    for i, m in enumerate(messages):
        for r in m.get("toolResults") or []:
            results[r["tool_use_id"]] = (i, r)
    calls: List[ToolCall] = []
    for call_idx, m in enumerate(messages):
        for t in m.get("toolUses") or []:
            found = results.get(t["tool_use_id"])
            if not found:
                continue  # no result yet -> nothing to drop
            res_idx, res = found
            calls.append(
                ToolCall(
                    id=f"t{len(calls) + 1}",
                    tool_use_id=t["tool_use_id"],
                    tool=t.get("tool", "?"),
                    input=t.get("input", {}) or {},
                    call_index=call_idx,
                    result_index=res_idx,
                    result_chars=len(res.get("text", "")),
                    is_error=bool(res.get("isError", False)),
                    pinned=is_pinned(call_idx, len(messages), preserve)
                    or is_pinned(res_idx, len(messages), preserve),
                )
            )
    return calls


def _input_text(inp: Dict[str, Any], limit: int) -> str:
    try:
        js = json.dumps(inp, ensure_ascii=False)
    except Exception:
        js = "[unserializable input]"
    return truncate(js, limit)


def _result_note(call: ToolCall) -> str:
    return f"{'error' if call.is_error else 'ok'}, {call.result_chars} chars (omitted)"


def _compact_call_line(call: ToolCall) -> str:
    parts = []
    for k, v in (call.input or {}).items():
        txt = v if isinstance(v, str) else _input_text({k: v}, 200)
        parts.append(f"{k}={re.sub(r'\s+', ' ', txt)}")
    return f"{call.id} {call.tool} {truncate(' '.join(parts), INPUT_CHARS[2])} -> {'error' if call.is_error else 'ok'} {call.result_chars}ch"


def goal_from_messages(messages: List[Dict[str, Any]]) -> str:
    prompts = [
        m for m in messages
        if m.get("role") == "user" and (m.get("text") or "").strip() and not (m.get("toolResults") or [])
    ]
    return "\n".join(truncate(m["text"], 500) for m in prompts[-3:])


def history_entries(messages, calls, input_chars) -> List[Dict[str, Any]]:
    by_msg: Dict[int, List[ToolCall]] = {}
    for c in calls:
        by_msg.setdefault(c.call_index, []).append(c)
    entries = []
    for i, m in enumerate(messages):
        tool_calls = [
            {"id": c.id, "tool": c.tool, "input": _input_text(c.input, input_chars), "result": _result_note(c)}
            for c in by_msg.get(i, [])
        ]
        if not (m.get("text") or "").strip() and not tool_calls:
            continue
        e: Dict[str, Any] = {"i": i, "role": m.get("role"), "text": m.get("text", "")}
        if tool_calls:
            e["tool_calls"] = tool_calls
        entries.append(e)
    return entries


def fit_state(messages, calls, opt: Options) -> Tuple[Dict[str, Any], int, str]:
    goal = opt.goal or goal_from_messages(messages)

    def state_of(history):
        return {"context": STATE_CONTEXT, "goal": goal, "history": history}

    def entry_tokens(e) -> int:
        return estimate_tokens(json.dumps(e, ensure_ascii=False)) + 1

    base = estimate_tokens(json.dumps(state_of([]), ensure_ascii=False))

    def fitted(history, tokens, stage):
        return (state_of(history), tokens, stage)

    # stage 0: full, then tighter input caps
    history: List[Dict[str, Any]] = []
    per_entry: List[int] = []
    tokens = 0

    def rebuild(input_chars: int):
        nonlocal history, per_entry, tokens
        history = history_entries(messages, calls, input_chars)
        per_entry = [entry_tokens(e) for e in history]
        tokens = base + sum(per_entry)

    def fits() -> bool:
        return tokens <= opt.max_state_tokens

    def shrink(idx: int, change):
        nonlocal tokens
        e = history[idx]
        change(e)
        now = entry_tokens(e)
        tokens += now - per_entry[idx]
        per_entry[idx] = now

    rebuild(INPUT_CHARS[0])
    if fits():
        return fitted(history, tokens, "full")
    for limit in INPUT_CHARS[1:]:
        rebuild(limit)
        if fits():
            return fitted(history, tokens, f"inputs<={limit}")

    def pinned(e) -> bool:
        return is_pinned(e["i"], len(messages), opt.preserve_recent_messages)

    order = [i for i, e in enumerate(history) if not pinned(e)] + [i for i, e in enumerate(history) if pinned(e)]

    for i in order:  # abridge long texts oldest-first
        if len(history[i].get("text", "")) <= TEXT_HEAD + TEXT_TAIL + 40:
            continue
        shrink(i, lambda e: e.update(text=abridge(e["text"], TEXT_HEAD, TEXT_TAIL)))
        if fits():
            return fitted(history, tokens, "texts abridged")

    for i in order:  # collapse old texts to one-line note
        e = history[i]
        if pinned(e) or not e.get("text"):
            continue
        orig = len((messages[e["i"]].get("text") or "")) if e["i"] < len(messages) else len(e["text"])
        shrink(i, lambda e2, n=orig: e2.update(text=f"[\u2026 {n} chars omitted \u2026]"))
        if fits():
            return fitted(history, tokens, "old messages collapsed")

    by_msg: Dict[int, List[ToolCall]] = {}
    for c in calls:
        by_msg.setdefault(c.call_index, []).append(c)
    for i in order:  # one line per old call
        e = history[i]
        own = by_msg.get(e["i"])
        if pinned(e) or not own:
            continue
        shrink(i, lambda e2, o=own: e2.update(tool_calls=[_compact_call_line(c) for c in o]))
        if fits():
            return fitted(history, tokens, "old calls compacted")

    left_out = set()
    for i in order:  # drop old call-less messages
        e = history[i]
        if pinned(e) or e.get("tool_calls"):
            continue
        left_out.add(i)
        tokens -= per_entry[i]
        if fits():
            return fitted([e2 for j, e2 in enumerate(history) if j not in left_out], tokens, "old messages left out")

    # fold runs of old call-only messages
    kept_hist = [e2 for j, e2 in enumerate(history) if j not in left_out]

    def foldable(e) -> bool:
        tc = e.get("tool_calls")
        return not pinned(e) and not (e.get("text") or "").strip() and isinstance(tc, list) and tc and all(isinstance(x, str) for x in tc)

    merged: List[Dict[str, Any]] = []
    for e in kept_hist:
        prev = merged[-1] if merged else None
        if prev is not None and foldable(prev) and foldable(e) and prev["role"] == e["role"]:
            prev = copy.deepcopy(prev)
            prev["tool_calls"] = list(prev["tool_calls"]) + list(e["tool_calls"])
            merged[-1] = prev
            continue
        merged.append(copy.copy(e))
    per_entry = [entry_tokens(e) for e in merged]
    tokens = base + sum(per_entry)
    if fits():
        return fitted(merged, tokens, "old calls merged")
    raise ValueError(f"history too large (~{tokens} tokens after truncation, limit {opt.max_state_tokens})")


# --------------------------------------------------------------------------
# Ollama scorer (replaces Jev). One fast request per batch, JSON out.
# --------------------------------------------------------------------------

SCORER_SYSTEM = (
    "You score tool calls for conversation compaction. "
    "Return JSON ONLY: a flat object mapping each question name to a number 0..1. "
    "call_<id> = knowing this call was made (with its input) still matters. "
    "result_<id> = the full verbatim output is still needed AND re-running would not do. "
    "Score high (0.8-1.0) for: errors, exact paths/IDs/commands still referenced by the goal, "
    "test failures, decisions/constraints. Score low (0.0-0.3) for: superseded reads, "
    "successful listings later refined, stale search results. When unsure, 0.5."
)


class OllamaAsker:
    """Drop-in JevAsker over local Ollama. No API key, no data leaves the box."""

    def __init__(self, model: str = "mistral-nemo:12b", host: str = "http://localhost:11434",
                 temperature: float = 0.0, timeout: int = 120, num_ctx: int = 32768):
        self.model = model
        self.host = host.rstrip("/")
        self.temperature = temperature
        self.timeout = timeout
        self.num_ctx = num_ctx

    def _prompt(self, state: Dict[str, Any], qnames: List[str], qtext: Dict[str, str]) -> str:
        lines = [
            f"GOAL:\n{state.get('goal') or '(none)'}",
            f"\nHISTORY (results omitted, oldest first):\n{json.dumps(state.get('history'), ensure_ascii=False)}",
            "\nQUESTIONS (score each 0..1):",
        ]
        for n in qnames:
            lines.append(f"- {n}: {qtext[n]}")
        lines.append('\nReturn JSON only, e.g. {"call_t1": 0.9, "result_t1": 0.2}. No prose.')
        return "\n".join(lines)

    def ask(self, state: Dict[str, Any], questions: Dict[str, str]) -> Dict[str, float]:
        """questions: name -> instruction. Returns name -> 0..1."""
        qnames = list(questions.keys())
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SCORER_SYSTEM},
                {"role": "user", "content": self._prompt(state, qnames, questions)},
            ],
            "stream": False,
            "format": "json",
            "options": {"temperature": self.temperature, "num_ctx": self.num_ctx},
        }
        req = urllib.request.Request(
            f"{self.host}/api/chat",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                payload = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Ollama chat failed ({self.model} @ {self.host}): {e}") from e
        content = (payload.get("message") or {}).get("content", "")
        try:
            data = json.loads(content)
        except Exception:
            # try to salvage the first {...} block
            m = re.search(r"\{.*\}", content, re.S)
            if not m:
                raise RuntimeError(f"Ollama returned non-JSON: {content[:300]}")
            data = json.loads(m.group(0))
        # accept {"answers": {...}} or flat
        if isinstance(data, dict) and isinstance(data.get("answers"), dict):
            data = data["answers"]
        out: Dict[str, float] = {}
        for n in qnames:
            try:
                v = float(data.get(n, 0.5))
            except Exception:
                v = 0.5
            out[n] = max(0.0, min(1.0, v))
        return out


class OpenAICompatAsker:
    """Same scorer over any OpenAI-compatible endpoint (LM Studio default).

    Tested on Goliath vs LM Studio @ localhost:1234 with qwen/qwen3.6-27b.
    Use when Ollama's llama-server is broken (2026-09-19: 500 on /api/chat,
    binary missing from the Ollama install dir).
    """

    def __init__(self, model: str = "qwen/qwen3.6-27b", host: str = "http://localhost:1234",
                 temperature: float = 0.0, timeout: int = 120):
        self.model = model
        self.host = host.rstrip("/")
        self.temperature = temperature
        self.timeout = timeout

    def ask(self, state: Dict[str, Any], questions: Dict[str, str]) -> Dict[str, float]:
        qnames = list(questions.keys())
        user = (
            f"GOAL:\n{state.get('goal') or '(none)'}"
            f"\n\nHISTORY (results omitted, oldest first):\n{json.dumps(state.get('history'), ensure_ascii=False)}"
            "\n\nQUESTIONS (score each 0..1):\n"
            + "\n".join(f"- {n}: {questions[n]}" for n in qnames)
            + '\n\nReturn JSON only, e.g. {"call_t1": 0.9, "result_t1": 0.2}. No prose.'
        )
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SCORER_SYSTEM},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "temperature": self.temperature,
        }
        req = urllib.request.Request(
            f"{self.host}/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                payload = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"LMStudio chat failed ({self.model} @ {self.host}): {e}") from e
        try:
            content = payload["choices"][0]["message"]["content"]
        except Exception:
            raise RuntimeError(f"unexpected chat payload: {str(payload)[:300]}")
        try:
            data = json.loads(content)
        except Exception:
            m = re.search(r"\{.*\}", content, re.S)
            if not m:
                raise RuntimeError(f"scorer returned non-JSON: {content[:300]}")
            data = json.loads(m.group(0))
        if isinstance(data, dict) and isinstance(data.get("answers"), dict):
            data = data["answers"]
        out: Dict[str, float] = {}
        for n in qnames:
            try:
                v = float(data.get(n, 0.5))
            except Exception:
                v = 0.5
            out[n] = max(0.0, min(1.0, v))
        return out


def heuristic_scores(calls: List[ToolCall]) -> Dict[str, float]:
    """Offline fallback when Ollama is unreachable. Keeps errors + small results."""
    out: Dict[str, float] = {}
    for c in calls:
        if c.is_error:
            out[f"call_{c.id}"], out[f"result_{c.id}"] = 1.0, 1.0
        elif c.result_chars <= 500:
            out[f"call_{c.id}"], out[f"result_{c.id}"] = 0.8, 0.7
        elif c.result_chars <= 4000:
            out[f"call_{c.id}"], out[f"result_{c.id}"] = 0.6, 0.3
        else:
            out[f"call_{c.id}"], out[f"result_{c.id}"] = 0.4, 0.1
    return out


def questions_for(call: ToolCall) -> Dict[str, str]:
    return {
        f"call_{call.id}": (
            f"Tool call {call.id} ({call.tool}) should stay: knowing this call was made, "
            "with its input, still matters for what the assistant does next"
        ),
        f"result_{call.id}": (
            f"Full output of {call.id} ({call.tool}, {call.result_chars} chars) should stay verbatim: "
            "still needed AND re-running would not do"
        ),
    }


def batch_calls(calls: List[ToolCall], state_tokens: int, opt: Options) -> List[List[ToolCall]]:
    budget = opt.max_request_tokens - state_tokens - REQUEST_OVERHEAD_TOKENS
    batches: List[List[ToolCall]] = []
    cur: List[ToolCall] = []
    cur_tok = 0
    for c in calls:
        tok = estimate_tokens(json.dumps(questions_for(c), ensure_ascii=False))
        if cur and cur_tok + tok > budget:
            batches.append(cur)
            cur, cur_tok = [], 0
        if not cur and tok > budget:
            raise ValueError(f"state leaves no room for questions (~{state_tokens} of {opt.max_request_tokens})")
        cur.append(c)
        cur_tok += tok
    if cur:
        batches.append(cur)
    return batches


def decide_call(call: ToolCall, keep_call: float, keep_result: float, opt: Options) -> Dict[str, Any]:
    base = {"id": call.id, "tool": call.tool, "keepCall": keep_call, "keepResult": keep_result}
    if call.pinned:
        return {**base, "action": "keep", "reason": "pinned"}
    if keep_result >= opt.keep_threshold:
        return {**base, "action": "keep", "reason": "kept"}
    if keep_call >= opt.keep_threshold:
        return {**base, "action": "drop_result", "reason": "result_dropped"}
    return {**base, "action": "drop_call", "reason": "call_dropped"}


def _truncated_result(text: str, is_error: bool, head: int) -> str:
    if len(text) <= head + 120:
        return text
    h = f"{text[:head]}\n" if head > 0 else ""
    return f"{h}[verbatim-compaction truncated {len(text) - head} chars of this tool result{' (error)' if is_error else ''}; re-run the tool if needed]"


def apply_decisions(messages, decisions, calls, head_chars: int):
    by_id = {c.id: c for c in calls}
    actions = {}
    for d in decisions:
        c = by_id.get(d["id"])
        if c and d["action"] != "keep":
            actions[c.tool_use_id] = d["action"]
    kept = []
    for m in messages:
        touched = any(t["tool_use_id"] in actions for t in m.get("toolUses") or []) or any(
            r["tool_use_id"] in actions for r in m.get("toolResults") or []
        )
        if not touched:
            kept.append(m)
            continue
        tool_uses = []
        for t in m.get("toolUses") or []:
            a = actions.get(t["tool_use_id"])
            if a == "drop_call":
                continue
            if a == "drop_result":
                nt = dict(t)
                nt["text"] = _truncated_result(t.get("text", ""), bool(t.get("isError", False)), head_chars)
                tool_uses.append(nt)
            else:
                tool_uses.append(t)
        tool_results = []
        for r in m.get("toolResults") or []:
            a = actions.get(r["tool_use_id"])
            if a == "drop_call":
                continue
            if a == "drop_result":
                nr = dict(r)
                nr["text"] = _truncated_result(r.get("text", ""), bool(r.get("isError", False)), head_chars)
                tool_results.append(nr)
            else:
                tool_results.append(r)
        if not (m.get("text") or "").strip() and not tool_uses and not tool_results:
            continue
        nm = {"role": m.get("role"), "text": m.get("text", ""), "toolUses": tool_uses}
        if tool_results:
            nm["toolResults"] = tool_results
        kept.append(nm)
    return kept


def msg_chars(m) -> int:
    total = len(m.get("text", ""))
    for t in m.get("toolUses") or []:
        try:
            total += len(json.dumps(t.get("input", {}), ensure_ascii=False))
        except Exception:
            total += 20
    for r in m.get("toolResults") or []:
        total += len(r.get("text", ""))
    return total


def compact(messages: List[Dict[str, Any]], asker: Optional[OllamaAsker] = None,
           opt: Optional[Options] = None, max_workers: int = 4,
           fallback_heuristic: bool = True) -> Dict[str, Any]:
    """Compact transcript. Returns {messages, decisions, stats}."""
    started = time.time()
    opt = opt or Options()
    calls = collect_tool_calls(messages, opt.preserve_recent_messages)
    cands = [c for c in calls if not c.pinned]
    chars_before = sum(msg_chars(m) for m in messages)
    state, state_tokens, stage = ({"context": STATE_CONTEXT, "goal": "", "history": []}, 0, "")
    batches: List[List[ToolCall]] = []
    answers: Dict[str, float] = {}
    if cands:
        state, state_tokens, stage = fit_state(messages, calls, opt)
        batches = batch_calls(cands, state_tokens, opt)
        if asker is None and fallback_heuristic:
            answers = heuristic_scores(cands)
        elif asker is None:
            raise ValueError("no asker and fallback_heuristic=False")
        else:
            try:
                with cf.ThreadPoolExecutor(max_workers=min(max_workers, len(batches))) as ex:
                    futs = []
                    for b in batches:
                        q: Dict[str, str] = {}
                        for c in b:
                            q.update(questions_for(c))
                        futs.append(ex.submit(asker.ask, state, q))
                    for f in cf.as_completed(futs):
                        answers.update(f.result())
            except Exception as e:
                if not fallback_heuristic:
                    raise
                print(f"[verbatim-compaction] Ollama failed ({e}), using heuristic fallback")
                answers = heuristic_scores(cands)
    decisions = [
        decide_call(c, answers.get(f"call_{c.id}", 1.0), answers.get(f"result_{c.id}", 1.0), opt)
        for c in calls
    ]
    kept = apply_decisions(messages, decisions, calls, opt.truncate_head_chars)
    chars_after = sum(msg_chars(m) for m in kept)

    def count(reason: str) -> int:
        return sum(1 for d in decisions if d["reason"] == reason)

    return {
        "messages": kept,
        "decisions": decisions,
        "stats": {
            "messagesBefore": len(messages),
            "messagesAfter": len(kept),
            "charsBefore": chars_before,
            "charsAfter": chars_after,
            "reduction": (chars_before - chars_after) / chars_before if chars_before else 0.0,
            "calls": len(calls),
            "kept": count("kept"),
            "resultsDropped": count("result_dropped"),
            "callsDropped": count("call_dropped"),
            "pinned": count("pinned"),
            "stateTokens": state_tokens,
            "stateStage": stage,
            "requests": len(batches),
            "ms": int((time.time() - started) * 1000),
        },
    }


# --------------------------------------------------------------------------
# Demo transcript: 1 user goal + 8 tool calls (reads, searches, one error)
# --------------------------------------------------------------------------

def demo_transcript() -> List[Dict[str, Any]]:
    def tu(i, tool, inp, txt=""):
        return {"tool_use_id": f"toolu_{i}", "tool": tool, "input": inp, "text": txt}

    def tr(i, txt, err=False):
        d: Dict[str, Any] = {"tool_use_id": f"toolu_{i}", "text": txt}
        if err:
            d["isError"] = True
        return d

    big_listing = "file1.ts\n" * 2000  # ~18k chars stale listing
    return [
        {"role": "user", "text": "Fix the failing test. Never edit src/generated.", "toolUses": []},
        {"role": "assistant", "text": "", "toolUses": [tu(1, "Read", {"file_path": "src/a.ts"})]},
        {"role": "user", "text": "", "toolUses": [], "toolResults": [tr(1, "export const a = 1;\n" * 50)]},
        {"role": "assistant", "text": "checking generated", "toolUses": [tu(2, "Read", {"file_path": "src/generated/b.ts"})]},
        {"role": "user", "text": "", "toolUses": [], "toolResults": [tr(2, "DO NOT EDIT\n" * 100)]},
        {"role": "assistant", "text": "", "toolUses": [tu(3, "Glob", {"pattern": "src/**/*.ts"})]},
        {"role": "user", "text": "", "toolUses": [], "toolResults": [tr(3, big_listing)]},
        {"role": "assistant", "text": "", "toolUses": [tu(4, "Grep", {"pattern": "failing_test", "path": "tests"})]},
        {"role": "user", "text": "", "toolUses": [], "toolResults": [tr(4, "tests/x.test.ts:42 AssertionError: expected 1 got 2")]},
        {"role": "assistant", "text": "", "toolUses": [tu(5, "Bash", {"command": "pytest tests/x.test.ts"})]},
        {"role": "user", "text": "", "toolUses": [], "toolResults": [tr(5, "FAILED tests/x.test.ts::test_x - assert 1 == 2", True)]},
        {"role": "assistant", "text": "recent work", "toolUses": [tu(6, "Read", {"file_path": "src/fix.ts"})]},
        {"role": "user", "text": "", "toolUses": [], "toolResults": [tr(6, "fix in progress\n" * 20)]},
        {"role": "user", "text": "Keep going, the error at tests/x.test.ts:42 is what matters", "toolUses": []},
    ]


def main():
    ap = argparse.ArgumentParser(description="Verbatim compaction demo (local scorer, no API key)")
    ap.add_argument("--backend", default="lmstudio", choices=["ollama", "lmstudio", "heuristic"])
    ap.add_argument("--model", default="", help="scorer model (default per backend)")
    ap.add_argument("--host", default="", help="override scorer host")
    ap.add_argument("--keep-threshold", type=float, default=0.5)
    ap.add_argument("--preserve", type=int, default=4)
    ap.add_argument("--heuristic", action="store_true", help="shorthand for --backend heuristic")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    msgs = demo_transcript()
    opt = Options(keep_threshold=args.keep_threshold, preserve_recent_messages=args.preserve)
    backend = "heuristic" if args.heuristic else args.backend
    if backend == "heuristic":
        asker = None
        label = "heuristic"
    elif backend == "ollama":
        asker = OllamaAsker(model=args.model or "mistral-nemo:12b", host=args.host or "http://localhost:11434")
        label = f"ollama/{asker.model}"
    else:
        asker = OpenAICompatAsker(model=args.model or "qwen/qwen3.6-27b", host=args.host or "http://localhost:1234")
        label = f"lmstudio/{asker.model}"
    result = compact(msgs, asker, opt)  # type: ignore[arg-type]
    s = result["stats"]
    print(f"model={label} "
          f"msgs {s['messagesBefore']}->{s['messagesAfter']} "
          f"chars {s['charsBefore']}->{s['charsAfter']} "
          f"reduction={s['reduction']:.2f} calls={s['calls']} "
          f"kept={s['kept']} resDrop={s['resultsDropped']} callDrop={s['callsDropped']} "
          f"pinned={s['pinned']} stage={s['stateStage']} req={s['requests']} ms={s['ms']}")
    for d in result["decisions"]:
        print(f"  {d['id']} {d['tool']:8} {d['action']:11} kc={d['keepCall']:.2f} kr={d['keepResult']:.2f} ({d['reason']})")
    if s["reduction"] < 0.25:
        print("note: reduction < 0.25 -> upstream would fall back to built-in summary")


if __name__ == "__main__":
    main()
