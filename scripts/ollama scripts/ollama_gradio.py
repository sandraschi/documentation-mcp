#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Ollama + 4‑bit CodeLlama (search‑enabled, DuckDuckGo) – Gradio demo
# ----------------------------------------------------------------------------
# Dependencies (install once):
#   pip install ollama gradio requests python-dotenv huggingface_hub orjson
# ----------------------------------------------------------------------------

import gradio as gr
import ollama
import requests
from dotenv import load_dotenv

# ---------- Load env vars (none required for DuckDuckGo) ----------
load_dotenv()


# ---------- Search helper (DuckDuckGo only) ----------
def duckduckgo_search(query: str, max_results: int = 3) -> list[dict]:
    """
    Return a list of dicts:
        {title, link, snippet}
    """
    resp = requests.get(
        "https://api.duckduckgo.com/",
        params={"q": query, "format": "json", "no_html": 1},
    )
    resp.raise_for_status()
    data = resp.json()

    # DuckDuckGo returns a flat list under `RelatedTopics`
    topics = data.get("RelatedTopics", [])
    results = []
    for t in topics:
        # `t` can be a dict with `Text`/`FirstURL` or a nested dict
        if "Text" in t and "FirstURL" in t:
            results.append({"title": t["Text"], "link": t["FirstURL"], "snippet": ""})
        elif "Topics" in t:  # nested
            for sub in t["Topics"]:
                if "Text" in sub and "FirstURL" in sub:
                    results.append({"title": sub["Text"], "link": sub["FirstURL"], "snippet": ""})
    return results[:max_results]


# ---------- Helper: Detect if the model wants us to search ----------
def parse_action(message: dict) -> str | None:
    """
    If the model’s reply contains {"action":"search","query":"…"},
    return the query string; otherwise None.
    """
    try:
        if message.get("action") == "search":
            return message["query"]
    except Exception:
        pass
    return None


# ---------- Helper: Send a message to the LLM ----------
# def ask(user_msg: str, model: str = "codellama:34b-codeinstruct") -> dict:
def ask(user_msg: str, model: str = "codellama") -> dict:
    """
    Send a user message to Ollama and return the parsed JSON response.
    """
    resp = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": user_msg}],
        format="json",  # get a dict instead of raw text
    )
    return resp  # already a dict


# ---------- Gradio callback ----------
def respond(message: str, history: list | None = None):
    """
    Gradio callback that:
        1. Sends the user message to the LLM.
        2. If the LLM requests a search, performs it.
        3. Feeds the search results back to the LLM.
        4. Returns the final answer and updated history.
    """
    if history is None:
        history = []

    # 1️⃣ Ask the model
    reply = ask(message)

    # 2️⃣ Does the model want us to search?
    query = parse_action(reply)
    if query:
        # Perform the search
        results = duckduckgo_search(query)

        # Build a concise context from top 3 hits
        context = "\n\n".join(f"{r['title']}\n{r['link']}\n{r.get('snippet', '')}" for r in results)
        # 3️⃣ Feed the context back to the LLM
        reply = ask(
            f"The user asked for: {query}. Here are the top results:\n{context}",
            model="codellama:34b-codeinstruct",
        )

    # 4️⃣ Return the answer (string) and updated chat history
    answer = reply["message"]["content"]
    return answer, [*history, (message, answer)]


# ---------- Gradio UI ----------
demo = gr.ChatInterface(
    respond,
    title="Ollama + 4‑bit CodeLlama (DuckDuckGo search)",
    description=(
        "Chat with your 4090‑hosted model.  When it needs up‑to‑date info, "
        "it will automatically call DuckDuckGo and return real results."
    ),
)

# ---------- Launch ----------
if __name__ == "__main__":
    # Default host: 127.0.0.1:7860
    demo.launch(share=False)
