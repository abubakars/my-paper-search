import streamlit as st
import requests
import random

st.set_page_config(page_title="Academic Writer", layout="wide")
st.title("📘 Academic Background & Problem Statement Generator")

topic = st.text_input("Enter your research topic (e.g., Impact of Urbanization on Flood Risk):")

# Semantic Scholar fetch function
def fetch_papers(query, limit=6):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,venue,url"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

# Citation formatter
def format_citation(paper):
    authors = paper.get("authors", [])
    if not authors:
        return "(Unknown, n.d.)"
    last_name = authors[0]["name"].split()[-1]
    year = paper.get("year", "n.d.")
    return f"({last_name}, {year})"

# Reference formatter
def format_reference(paper):
    authors = ", ".join([a["name"] for a in paper["authors"]])
    title = paper["title"]
    venue = paper.get("venue", "No Journal")
    year = paper.get("year", "n.d.")
    url = paper["url"]
    return f"{authors} ({year}). *{title}*. {venue}. [Link]({url})"

# Academic text generators
def generate_background(topic, papers):
    intro = f"The topic of **{topic}** has gained significant academic attention over the years. "
    body = ""
    for p in papers:
        sentence = f"{p['title']} contributes to this understanding {format_citation(p)}. "
        body += sentence
    context = (
        f"Scholars have examined the various dimensions, causes, and impacts of {topic.lower()}, "
        "highlighting both theoretical and practical implications. "
    )
    conclusion = "This growing body of literature underscores the need for further investigation into context-specific realities."
    background = intro + body + context + conclusion
    return background

def generate_problem_statement(topic, papers):
    context = f"Despite increasing interest in **{topic}**, certain gaps remain in both theoretical exploration and practical application. "
    issues = "Existing studies have focused largely on general perspectives, with less emphasis on local, data-driven analysis. "
    examples = ""
    for p in papers[:3]:
        examples += f"For instance, {p['title']} identifies limitations in current research {format_citation(p)}. "
    gap = (
        "The absence of targeted investigations, especially in under-represented regions or sub-topics, "
        "creates a significant challenge for policy formulation and implementation. "
    )
    conclusion = "Therefore, this study seeks to address this gap by exploring the topic in greater depth."
    problem = context + issues + examples + gap + conclusion
    return problem

# Main app logic
if topic:
    with st.spinner("Fetching related literature and generating content..."):
        papers = fetch_papers(topic)

    if papers:
        st.markdown("## 📝 Background of the Study")
        st.write(generate_background(topic, papers))

        st.markdown("## 🛑 Statement of the Problem")
        st.write(generate_problem_statement(topic, papers))

        st.markdown("## 📚 References")
        for p in papers:
            st.markdown(f"- {format_reference(p)}")
    else:
        st.warning("No papers found. Try a broader topic.")
