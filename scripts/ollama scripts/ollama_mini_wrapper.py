# 1️⃣ pip install ollama requests python-dotenv
# 2️⃣ set SERPAPI_KEY in a .env file

import json
import os

import requests
from dotenv import load_dotenv
from ollama import Chat

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def web_search(query):
    resp = requests.get(
        "https://serpapi.com/search",
        params={"q": query, "api_key": SERPAPI_KEY, "engine": "google"},
    )
    return resp.json()


def parse_action(msg):
    """Detects {"action":"search","query":"..."} in the model’s reply."""
    try:
        data = json.loads(msg)
        if data.get("action") == "search":
            return data["query"]
    except Exception:
        pass
    return None


chat = Chat(model="codellama:34b-codeinstruct")

while True:
    user = input("\nYou: ")
    if user.lower() in {"exit", "quit"}:
        break

    # 1️⃣ Ask the model
    reply = chat.send(user, format="json")
    action = parse_action(reply)

    if action:
        print(f"\n🔍 Searching for: {action}")
        results = web_search(action)

        # Build a short context from the top 3 hits
        context = "\n\n".join(
            f"{r['title']}\n{r['link']}\n{r.get('snippet', '')}"
            for r in results.get("organic_results", [])[:3]
        )
        # 2️⃣ Feed back to the model
        final = chat.send(
            f"The user asked for: {action}. Here are the top results:\n{context}",
            format="json",
        )
        print("\nAssistant:", json.loads(final))
    else:
        print("\nAssistant:", json.loads(reply))
