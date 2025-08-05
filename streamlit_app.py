import streamlit as st
import requests

st.set_page_config(page_title="Academic Paper Search", layout="wide")
st.title("📚 Academic Paper Search (No AI)")

query = st.text_input("Enter a research question or topic:")

def fetch_papers(query, limit=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,venue,url"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

def format_citation(paper):
    authors = paper["authors"]
    if not authors:
        return "(Unknown, n.d.)"
    last_name = authors[0]["name"].split()[-1]
    year = paper.get("year", "n.d.")
    return f"({last_name}, {year})"

def format_reference(paper):
    authors = ", ".join([a["name"] for a in paper["authors"]])
    title = paper["title"]
    venue = paper.get("venue", "No Journal")
    year = paper.get("year", "n.d.")
    url = paper["url"]
    return f"{authors} ({year}). *{title}*. {venue}. [Link]({url})"

if query:
    with st.spinner("Searching..."):
        papers = fetch_papers(query)

    if papers:
        st.markdown("### 🔍 Suggested Citations")
        citations = [format_citation(p) for p in papers]
        st.write("; ".join(citations))

        st.markdown("### 📚 References")
        for p in papers:
            st.markdown(f"- {format_reference(p)}")
    else:
        st.warning("No papers found.")
