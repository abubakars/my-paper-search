import streamlit as st
import requests
import openai

# Set your OpenAI API key
openai.api_key = "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"

st.title("📖 Research Answer with Citations")

question = st.text_input("Ask a research question:")

def fetch_papers(query):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=5&fields=title,authors,year,url,venue"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

def format_citation(paper):
    authors = paper["authors"]
    first_author = authors[0]["name"] if authors else "Unknown"
    year = paper.get("year", "n.d.")
    return f"({first_author}, {year})"

def format_reference(paper):
    authors = ", ".join([a["name"] for a in paper["authors"]])
    year = paper.get("year", "n.d.")
    title = paper["title"]
    venue = paper.get("venue", "No Journal")
    url = paper["url"]
    return f"{authors} ({year}). *{title}*. {venue}. [Link]({url})"

if question:
    # 1. Get papers
    papers = fetch_papers(question)

    # 2. Generate answer with citations
    citations = [format_citation(p) for p in papers]
    joined_citations = "; ".join(citations)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Answer this question in a paragraph and insert these citations at the end: {joined_citations}. Question: {question}"}
        ]
    )
    answer = response["choices"][0]["message"]["content"]
    st.markdown("### 📝 Answer")
    st.write(answer)

    st.markdown("### 📚 References")
    for paper in papers:
        st.markdown(f"- {format_reference(paper)}")
