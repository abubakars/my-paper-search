import streamlit as st
import requests
import textwrap
import random

st.set_page_config(page_title="Peer-Reviewed Q&A Assistant", layout="wide")
st.title("🎓 Peer-reviewed Q&A Generator")

# --- User input ---
question = st.text_area("Ask a research question", placeholder="e.g., What are the effects of climate change on agricultural productivity in West Africa?")
num_sources = st.slider("How many peer-reviewed sources?", min_value=5, max_value=30, value=10)

# --- API Fetch ---
def fetch_papers(query, limit):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,authors,year,venue,url"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

# --- Format citation & references ---
def format_citation(paper):
    authors = paper.get("authors", [])
    last_name = authors[0]["name"].split()[-1] if authors else "Unknown"
    year = paper.get("year", "n.d.")
    return f"({last_name}, {year})"

def format_reference(paper):
    authors = ", ".join([a["name"] for a in paper["authors"]])
    title = paper["title"]
    venue = paper.get("venue", "No Journal")
    year = paper.get("year", "n.d.")
    url = paper["url"]
    return f"{authors} ({year}). *{title}*. {venue}. [Link]({url})"

# --- Generate Answer ---
def generate_answer(question, papers):
    intro = f"The question **\"{question}\"** has been the subject of scholarly discussion across multiple disciplines. "

    middle = ""
    for p in papers[:num_sources]:
        summary = p.get("abstract") or p.get("title")
        citation = format_citation(p)
        middle += f"{summary.strip()} {citation}. "

    conclusion = (
        "In summary, while various studies provide insights into this question, there remain gaps in the literature that call for more interdisciplinary, localized, and data-driven investigations. "
        "Future research should prioritize context-specific interventions and long-term tracking to better inform policy and practice."
    )

    return "\n\n".join([
        textwrap.fill(intro, 120),
        textwrap.fill(middle, 120),
        textwrap.fill(conclusion, 120)
    ])

# --- Main output ---
if question:
    with st.spinner("Fetching peer-reviewed answers..."):
        papers = fetch_papers(question, num_sources)

    if papers:
        st.markdown("## 📖 Peer-reviewed Response")
        st.write(generate_answer(question, papers))

        st.markdown("## 📚 References")
        for p in papers:
            st.markdown(f"- {format_reference(p)}")
    else:
