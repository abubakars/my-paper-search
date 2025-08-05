import streamlit as st
import requests
import random

st.set_page_config(page_title="Research Summary Generator", layout="wide")
st.title("📚 Generate a Research Summary with Real Citations (No AI)")

query = st.text_input("Enter a research question or topic:")

# Get papers from Semantic Scholar
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

# Format in-text citation
def format_citation(paper):
    authors = paper["authors"]
    if not authors:
        return "(Unknown, n.d.)"
    last_name = authors[0]["name"].split()[-1]
    year = paper.get("year", "n.d.")
    return f"({last_name}, {year})"

# Format reference
def format_reference(paper):
    authors = ", ".join([a["name"] for a in paper["authors"]])
    title = paper["title"]
    venue = paper.get("venue", "No Journal")
    year = paper.get("year", "n.d.")
    url = paper["url"]
    return f"{authors} ({year}). *{title}*. {venue}. [Link]({url})"

# Generate summary (mock but academic-style)
def generate_paragraph(topic, papers):
    intro = f"The topic of **{topic}** has attracted significant scholarly attention in recent years. "
    body = ""
    for paper in papers:
        sentence = f"{paper['title']} explores this issue in depth {format_citation(paper)}. "
        body += sentence
    filler = (
        "These studies collectively highlight the importance of ongoing research in this area. "
        "While the findings vary across disciplines, they offer insights into key mechanisms, challenges, "
        "and future opportunities. "
    )
    closing = "In conclusion, there is a growing body of literature that provides foundational knowledge and guidance for further exploration."

    paragraph = intro + body + filler + closing
    # Ensure paragraph has at least 250 words
    while len(paragraph.split()) < 250:
        paragraph += " " + random.choice([intro, filler, closing])
    return paragraph

if query:
    with st.spinner("Fetching papers and generating summary..."):
        papers = fetch_papers(query, limit=5)

    if papers:
        paragraph = generate_paragraph(query, papers)
        st.markdown("### 📝 Generated Research Summary")
        st.write(paragraph)

        st.markdown("### 📚 References")
        for p in papers:
            st.markdown(f"- {format_reference(p)}")
    else:
        st.warning("No papers found for this topic.")
