

# # server.py
# import os
# from dotenv import load_dotenv

# from autogen import ConversableAgent
# from autogen.agentchat import ReplyResult
# from autogen.a2a import A2aAgentServer

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # optional
# GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # pick your default


# llm_config = {
#     "config_list": [
#         {"model": GEMINI_MODEL, "api_key": GEMINI_API_KEY, "api_type": "google"}
#     ],
#     "cache_seed": 42,
# }

# agent = ConversableAgent(
#     name="python_coder",
#     system_message="You are an expert Python developer...",
#     llm_config=llm_config,
#     human_input_mode="NEVER",
# )

# # Create A2A server
# server = A2aAgentServer(
#     agent,
#     url="http://127.0.0.1:8000"
# ).build()



# # # simple a2a speakable agent 

# # from autogen import ConversableAgent, LLMConfig
# # from autogen.a2a import A2aAgentServer
# # import os
# # from dotenv import load_dotenv
# # load_dotenv()

# # # Create your regular agent

# # llm_config = {
# #     "config_list": [{"model": "gpt-4o-mini", "api_key":os.getenv('OPENAI_API_KEY') }],
# #     "cache_seed": 42
# # }


# # agent = ConversableAgent(
# #     name="python_coder",
# #     system_message="You are an expert Python developer...",
# #     llm_config=llm_config,
# # )

# # # Create A2A server
# # server = A2aAgentServer(agent, url="http://localhost:9000").build()

# #python -m uvicorn server:server --host 127.0.0.1 --port 9000



# #webScraper

import sys
import os

# truststore is Windows-only; skip on Linux (e.g. Render)

from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from typing import Annotated

from autogen import ConversableAgent
from autogen.a2a import A2aAgentServer

# ENV

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "OPENAI_API_KEY not set."

llm_config = {
    "config_list": [
        {"model": "gpt-4o-mini", "api_key": OPENAI_API_KEY}
    ],
    "cache_seed": 42,
}

# TERMINATION DETECTOR
def is_done(msg):
    text = (msg or {}).get("content") or ""
    return text.strip().endswith("TERMINATE")


# ASSISTANT (THE A2A AGENT)
assistant = ConversableAgent(
    name="web_reader",
    system_message=(
        "You summarize pages using two tools:\n"
        "- fetch_article_html\n"
        "- fetch_article_wiki_api\n\n"
        "If the URL is from Wikipedia, prefer fetch_article_wiki_api.\n"
        "After producing the final summary, end with: TERMINATE"
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=is_done,
    max_consecutive_auto_reply=1,
)


#TOOL 1 — HTML scraper

def fetch_article_html(url: Annotated[str, "HTTP/HTTPS URL"]) -> str:
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        return "\n".join(p.get_text() for p in soup.find_all("p"))[:3000]
    except Exception as e:
        return f"[HTML ERROR] {e}"

assistant.register_for_llm(
    name="fetch_article_html",
    description="Scrape <p> tags from HTML.",
)(fetch_article_html)

assistant.register_for_execution(name="fetch_article_html")(fetch_article_html)

# WIKI API scraper

def fetch_article_wiki_api(url: Annotated[str, "Wikipedia URL"]) -> str:
    from urllib.parse import urlparse, unquote, quote

    if "wikipedia.org/wiki/" not in url:
        return "[WIKI API ERROR] Not a Wikipedia page."

    parsed = urlparse(url)
    host = parsed.hostname or "en.wikipedia.org"
    lang = host.split(".")[0] if host.endswith("wikipedia.org") else "en"

    path = parsed.path or ""
    if "/wiki/" not in path:
        return "[WIKI API ERROR] Could not parse title."

    title = unquote(path.split("/wiki/", 1)[-1])
    encoded = quote(title, safe="")

    try:
        plain_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/plain/{encoded}"
        r1 = requests.get(plain_url, headers={"User-Agent": "Mozilla/5.0"})
        if r1.status_code == 200 and r1.text.strip():
            return r1.text[:3000]

        summary_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        r2 = requests.get(summary_url, headers={"User-Agent": "Mozilla/5.0"})
        if r2.status_code == 200:
            extract = (r2.json().get("extract") or "").strip()
            if extract:
                return extract[:3000]

        return "[WIKI API ERROR] No content."
    except Exception as e:
        return f"[WIKI API ERROR] {e}"

assistant.register_for_llm(
    name="fetch_article_wiki_api",
    description="Fetch text using Wikipedia REST API.",
)(fetch_article_wiki_api)

assistant.register_for_execution(name="fetch_article_wiki_api")(fetch_article_wiki_api)

PORT = int(os.getenv("PORT", 9000))
HOST = os.getenv("HOST", "0.0.0.0")
server = A2aAgentServer(assistant, url=f"http://{HOST}:{PORT}").build()

