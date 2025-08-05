import streamlit as st
from scholarly import scholarly
import random
import time

# ---- Config ----
st.set_page_config(page_title="Academic Writer", layout="wide")

# ---- Functions ----
def fetch_papers(query, max_results=5):
    search_results = scholarly.search_pubs(query)
    papers = []
    try:
        for _ in range(max_results):
            result = next(search_results)
            papers.append(result)
    except StopIteration:
        pass
    return papers

def generate_background(query, papers):
    intro = f"The topic of '{query}' has gained increasing attention in scholarly discourse. "
    body = ""
    for paper in papers:
        snippet = paper.get("bib", {}).get("abstract", "") or ""
        title = paper.get("bib", {}).get("title", "")
        author = paper.get("bib", {}).get("author", "")
        year = paper.get("bib", {}).get("pub_year", "n.d.")
        body += f"{snippet} ({author}, {year}). "

    filler = ("Furthermore, this topic intersects with multiple dimensions including policy, technology, and "
              "societal impacts. Recent studies emphasize its relevance in contemporary research. ") * 5
    conclusion = "In summary, the background of this topic is deeply rooted in both historical and emerging academic efforts."
    return intro + filler + body + conclusion

def format_reference(paper):
    bib = paper.get("bib", {})
    title = bib.get("title", "No title")
    author = bib.get("author", "Unknown author")
    year = bib.get("pub_year", "n.d.")
    journal = bib.get("venue", "")
    return f"{author} ({year}). {title}. *{journal}*."

# ---- UI ----
st.title("📚 Academic Background Generator (APA 6 Format)")
st.markdown("This tool generates a detailed academic background using peer-reviewed sources from Google Scholar.")

query = st.text_input("Enter your research topic or question:")
num_sources = st.slider("Number of sources", 3, 10, 5)

if st.button("🔍 Generate Background"):
    if not query:
        st.warning("Please enter a research topic or question.")
    else:
        with st.spinner("Searching and composing..."):
            papers = fetch_papers(query, max_results=num_sources)
            time.sleep(2)

            if papers:
                st.subheader("📄 Background of the Study")
                st.write(generate_background(query, papers))

                st.subheader("📚 APA 6 References")
                for paper in papers:
                    st.markdown(f"- {format_reference(paper)}")
            else:
                st.error("No papers found. Try a broader or clearer query.")
