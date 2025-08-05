import streamlit as st
from scholarly import scholarly
import random
import re

st.set_page_config(page_title="APA6 Academic Writer", layout="wide")
st.markdown("<h1 style='text-align: center;'>📚 APA 6 Academic Background Generator</h1>", unsafe_allow_html=True)

# --- Google Scholar Fetcher ---
def fetch_scholar_articles(query, num_results=5):
    search_results = scholarly.search_pubs(query)
    papers = []
    for _ in range(num_results):
        try:
            paper = next(search_results)
            papers.append({
                "title": paper.get("bib", {}).get("title", ""),
                "author": paper.get("bib", {}).get("author", ""),
                "year": paper.get("bib", {}).get("pub_year", ""),
                "summary": paper.get("bib", {}).get("abstract", ""),
                "venue": paper.get("bib", {}).get("venue", "")
            })
        except StopIteration:
            break
    return papers

# --- Format APA 6 in-text citation ---
def format_intext(authors, year):
    if not authors or not year:
        return "(n.d.)"
    
    authors_list = [name.strip() for name in authors.split(" and ")]
    if len(authors_list) == 1:
        return f"({authors_list[0]}, {year})"
    elif len(authors_list) == 2:
        return f"({authors_list[0]} & {authors_list[1]}, {year})"
    else:
        return f"({authors_list[0]} et al., {year})"

# --- Generate Background Paragraphs with Citations ---
def generate_background(paragraphs, papers):
    background = ""
    cited_papers = []

    for _ in range(paragraphs):
        if not papers:
            break

        paper = random.choice(papers)
        papers.remove(paper)

        citation = format_intext(paper["author"], paper["year"])
        paragraph = f"{paper['summary']} {citation}."
        background += paragraph + "\n\n"
        cited_papers.append(paper)

    return background.strip(), cited_papers

# --- Format APA 6 Reference List ---
def format_reference_apa6(paper):
    authors = paper['author']
    year = paper['year']
    title = paper['title']
    venue = paper['venue'] or "n.p."

    return f"{authors} ({year}). {title}. *{venue}*."

# --- Streamlit App ---
st.write("Ask a research question to generate academic-style background with APA 6 references.")

query = st.text_input("🔍 Enter your research question or topic")

paragraphs = st.slider("How many background paragraphs?", 3, 20, 6)

if st.button("🧠 Generate Academic Background"):
    if query:
        with st.spinner("🔍 Searching Google Scholar..."):
            articles = fetch_scholar_articles(query, num_results=paragraphs + 5)

        if articles:
            st.subheader("📖 Background of the Study")
            background, cited = generate_background(paragraphs, articles.copy())
            st.write(background)

            st.subheader("📚 References (APA 6th Edition)")
            for p in cited:
                st.markdown(f"- {format_reference_apa6(p)}")
        else:
            st.warning("No articles found.")
    else:
        st.warning("Please enter a research question.")
