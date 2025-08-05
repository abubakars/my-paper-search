import requests
import streamlit as st

# Search papers from Semantic Scholar
def search_semantic_scholar(query, limit=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,authors,year,url"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        return []

# Format APA 6 citation
def format_apa6(paper):
    authors = paper.get("authors", [])
    author_str = ""
    if authors:
        formatted_authors = [f"{a['name'].split()[-1]}, {a['name'].split()[0][0]}." for a in authors[:3]]
        author_str = ", ".join(formatted_authors)
        if len(authors) > 3:
            author_str += ", et al."
    year = paper.get("year", "n.d.")
    title = paper.get("title", "No title")
    url = paper.get("url", "")
    return f"{author_str} ({year}). *{title}*. Retrieved from {url}"

# Generate background text
def generate_background(papers):
    paragraphs = []
    for paper in papers:
        abstract = paper.get("abstract", "")
        citation = format_apa6(paper)
        if abstract:
            paragraphs.append(f"{abstract} ({citation})")
    return "\n\n".join(paragraphs)

# Streamlit UI
st.set_page_config(page_title="AI Academic Writer", layout="wide")
st.title("📚 AI Academic Writer with Citations")
st.markdown("Write a research question or topic. This tool will generate a scholarly background with APA 6 citations.")

query = st.text_input("Enter research topic or question:", placeholder="e.g. Effects of mobile phone usage on academic performance")
limit = st.slider("Number of references", 3, 20, 5)

if st.button("Generate Background of Study"):
    with st.spinner("Searching academic articles..."):
        results = search_semantic_scholar(query, limit)
        if results:
            background = generate_background(results)
            st.subheader("Generated Background of Study")
            st.markdown(background)
        else:
            st.error("No results found. Try a different topic.")
