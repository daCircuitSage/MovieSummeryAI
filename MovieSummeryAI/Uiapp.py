import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineAI · Movie Analyzer",
    page_icon="🎬",
    layout="centered",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0D0D0D !important;
    color: #E8E8E8;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }

.hero {
    text-align: center;
    padding: 3rem 0 1.5rem;
    border-bottom: 1px solid #2A2A2A;
    margin-bottom: 2.5rem;
}
.hero-badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #C9A84C;
    border: 1px solid #C9A84C;
    padding: 4px 14px;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 6vw, 4rem);
    font-weight: 900;
    color: #F5EFE0;
    line-height: 1.1;
    margin: 0 0 0.5rem;
    letter-spacing: -0.02em;
}
.hero-title span { color: #C9A84C; }
.hero-sub { font-size: 0.95rem; color: #888; font-weight: 300; }

textarea {
    background: #161616 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 12px !important;
    color: #E8E8E8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}
textarea:focus {
    border-color: #C9A84C !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #C9A84C 0%, #E8C97A 100%) !important;
    color: #0D0D0D !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.5rem !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    font-size: 0.75rem;
    color: #444;
    letter-spacing: 0.05em;
}
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by Mistral AI</div>
    <h1 class="hero-title">Cine<span>AI</span></h1>
    <p class="hero-sub">Paste any movie description — get a complete cinematic breakdown instantly.</p>
</div>
""", unsafe_allow_html=True)

# ─── Input ────────────────────────────────────────────────────────────────────
paragraph = st.text_area(
    label="Movie Description",
    placeholder="Paste a movie synopsis, plot description, or any paragraph about a film…",
    height=160,
    label_visibility="collapsed",
)

analyze_btn = st.button("Analyze Film →")

# ─── Prompt ───────────────────────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ('system', """
You are an advanced AI that analyzes and summarizes movie descriptions.

Your task is to extract structured and meaningful information from the given paragraph and enrich it with general knowledge if needed.

Extract the following fields:

1. Title (if mentioned)
2. Release Year
3. Main Characters
4. Setting (location, world, or environment)
5. Main Goal or Objective
6. Main Conflict (external and internal if applicable)
7. Key Plot Summary (short and clear)
8. Core Theme(s)
9. Genre
10. Tone (e.g., dark, emotional, suspenseful, inspiring)
11. Key Concepts (e.g., dream, time travel, space, crime, etc.)
12. IMDb Rating (approximate if known)
13. Rotten Tomatoes Score (if known)
14. Overall Review Summary (1-2 sentences about critical reception)

Rules:
- Keep each field concise (1 sentence max).
- Do NOT copy text directly; rewrite in simple words.
- If any field is not clearly available, use general knowledge OR write "Not specified".
- Ratings can be approximate but should be realistic.
- Avoid unnecessary explanation.
- Output must be clean and structured.

Output strictly in this format (no extra text):

Title: ...
Release Year: ...
Main Characters: ...
Setting: ...
Goal: ...
Conflict: ...
Plot: ...
Theme: ...
Genre: ...
Tone: ...
Key Concepts: ...
IMDb Rating: ...
Rotten Tomatoes: ...
Review: ..."""),
    ('human', "Extract information from the paragraph:\n{paragraph}")
])

# ─── Field config ─────────────────────────────────────────────────────────────
FIELDS = [
    ("Title",           "Title",              True,  True,  False),
    ("Release Year",    "Release Year",       False, False, False),
    ("Genre",           "Genre",              False, False, False),
    ("Tone",            "Tone",               False, False, False),
    ("Setting",         "Setting",            False, False, False),
    ("Main Characters", "Main Characters",    True,  False, False),
    ("Goal",            "Goal / Objective",   True,  False, False),
    ("Conflict",        "Conflict",           True,  False, False),
    ("Plot",            "Plot Summary",       True,  False, False),
    ("Theme",           "Core Themes",        False, False, False),
    ("Key Concepts",    "Key Concepts",       False, False, False),
    ("IMDb Rating",     "IMDb Rating",        False, False, True),
    ("Rotten Tomatoes", "Rotten Tomatoes",    False, False, True),
    ("Review",          "Critical Reception", True,  False, False),
]

def parse_response(text: str) -> dict:
    result = {}
    for line in text.strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result

def build_result_html(data: dict) -> str:
    items_html = ""
    for key, label, full, is_title, is_rating in FIELDS:
        val = data.get(key, "—")
        css_class = "field-item full-width" if full else "field-item"

        if is_title:
            val_html = f'<div class="field-value title-val">{val}</div>'
        elif is_rating:
            val_html = f'<span class="rating-pill">{val}</span>'
        else:
            val_html = f'<div class="field-value">{val}</div>'

        items_html += f"""
        <div class="{css_class}">
            <div class="field-label">{label}</div>
            {val_html}
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: transparent; font-family: 'DM Sans', sans-serif; padding: 4px 2px 12px; }}
  .result-wrapper {{
    border: 1px solid #2A2A2A;
    border-radius: 16px;
    overflow: hidden;
    background: #161616;
  }}
  .result-header {{
    display: flex; align-items: center; gap: 10px;
    padding: 0.9rem 1.4rem;
    background: #1A1A1A;
    border-bottom: 1px solid #2A2A2A;
    font-size: 0.72rem; letter-spacing: 0.16em;
    text-transform: uppercase; color: #C9A84C; font-weight: 500;
  }}
  .dot {{
    width: 7px; height: 7px; border-radius: 50%;
    background: #C9A84C; flex-shrink: 0;
    animation: pulse 1.8s infinite;
  }}
  @keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.25; }} }}
  .fields-grid {{ display: grid; grid-template-columns: 1fr 1fr; }}
  .field-item {{
    padding: 0.85rem 1.3rem;
    border-bottom: 1px solid #2A2A2A;
    border-right: 1px solid #2A2A2A;
  }}
  .field-item.full-width {{ grid-column: 1 / -1; border-right: none; }}
  .field-item:not(.full-width):nth-child(even) {{ border-right: none; }}
  .field-label {{
    font-size: 0.62rem; letter-spacing: 0.18em;
    text-transform: uppercase; color: #C9A84C;
    font-weight: 500; margin-bottom: 5px;
  }}
  .field-value {{ font-size: 0.9rem; color: #E8E8E8; line-height: 1.55; font-weight: 300; }}
  .title-val {{
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem; font-weight: 700;
    color: #F5EFE0; line-height: 1.2;
  }}
  .rating-pill {{
    display: inline-block;
    background: rgba(201,168,76,0.12);
    border: 1px solid rgba(201,168,76,0.3);
    color: #E8C97A; border-radius: 6px;
    padding: 3px 12px; font-size: 0.88rem;
    font-weight: 500; margin-top: 2px;
  }}
</style>
</head>
<body>
  <div class="result-wrapper">
    <div class="result-header"><div class="dot"></div>Analysis Complete</div>
    <div class="fields-grid">{items_html}</div>
  </div>
</body>
</html>"""

# ─── Run ──────────────────────────────────────────────────────────────────────
if analyze_btn:
    if not paragraph.strip():
        st.warning("Please enter a movie description first.")
    else:
        with st.spinner("Analyzing…"):
            model = ChatMistralAI(model='mistral-small-2506', temperature=0.3)
            final_prompt = prompt.invoke({'paragraph': paragraph})
            response = model.invoke(final_prompt)
            data = parse_response(response.content)

        # Use components.html (iframe) to bypass Streamlit's HTML sanitizer
        result_html = build_result_html(data)
        components.html(result_html, height=700, scrolling=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">CineAI · Film Intelligence Engine</div>', unsafe_allow_html=True)