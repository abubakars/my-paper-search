import streamlit as st
import requests
import random
import textwrap

st.set_page_config(page_title="Academic Research Generator", layout="wide")
st.title("📘 Academic Writer: Background & Problem Statement Generator")

# --- User Input ---
topic = st.text_input("Enter your research topic:", placeholder="e.g., Climate Change and Agriculture")
num_sources = st.slider("Number of sources to include", min_value=5, max_value=50, value=15)

# --- Semantic Scholar fetch ---
def fetch_papers(query, limit):
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

# --- Format citation ---
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

# --- Generate academic sections ---
def generate_background(topic, papers):
    intro = f"The topic of **{topic}** has received considerable scholarly attention, reflecting its relevance to both academic and practical domains. "
    paragraphs = [intro]

    # Group in 5-paper batches to structure paragraphs
    for i in range(0, len(papers), 5):
        group = papers[i:i+5]
        text = ""
        for p in group:
            text += f"{p['title']} provides valuable insights into this topic {format_citation(p)}. "
        para = (
            f"Research in this area explores various dimensions including theoretical foundations, empirical observations, and policy implications. "
            f"{text}These studies collectively emphasize the complexity and multidisciplinary nature of {topic.lower()}."
        )
        paragraphs.append(para)

    closing = (
        f"Despite this growing body of work, the literature still reflects significant variation in approaches and findings. "
        f"This suggests a need for context-specific studies that can bridge theory and practice. "
        f"The continued interest in {topic.lower()} underscores its critical importance across various sectors."
    )
    paragraphs.append(closing)

    # Join all into one long-form academic paragraph
    return "\n\n".join(textwrap.fill(p, 120) for p in paragraphs)

def generate_problem_statement(topic, papers):
    intro = (
        f"Although several studies have examined **{topic}**, significant gaps and inconsistencies remain. "
        f"These gaps hinder comprehensive understanding and evidence-based decision-making. "
    )
    issues = (
        "Many of the existing works focus broadly on global or generalized contexts, leaving out region-specific variables and indicators. "
        "This has made it difficult to translate findings into actionable strategies or policies. "
    )
    examples = ""
    for p in papers[:5]:
        examples += f"{p['title']} illustrates some of these limitations {format_citation(p)}. "

    conclusion = (
        f"Therefore, it is essential to conduct more in-depth, focused studies on {topic.lower()}, "
        "especially within underrepresented or complex local environments. "
        "This study seeks to fill this critical research gap."
    )

    return "\n\n".join([
        textwrap.fill(intro, 120),
        textwrap.fill(issues, 120),
        textwrap.fill(examples, 120),
        textwrap.fill(conclusion, 120)
    ])

# --- App Output ---
if topic:
    with st.spinner("Fetching papers and generating content..."):
        papers = fetch_papers(topic, num_sources)

    if papers:
        st.markdown("## 📝 Background of the Study")
        st.write(generate_background(topic, papers))

        st.markdown("## 🛑 Statement of the Problem")
        st.write(generate_problem_statement(topic, papers))

        st.markdown("## 📚 References")
        for p in papers:
            st.markdown(f"- {format_reference(p)}")
    else:
        st.error("No papers found. Try using simpler or broader topic wording.")
