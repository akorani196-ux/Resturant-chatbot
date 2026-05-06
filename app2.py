# =============================================================================
# app.py — Savory Spot RAG Chatbot (Final Premium Visible Version)
# =============================================================================

# ── STEP 1: IMPORTS ───────────────────────────────────────────────────────────
import streamlit as st
import os
import numpy as np
import faiss
from groq import Groq
from sentence_transformers import SentenceTransformer
from restaurant_data import restaurant_chunks

# ── STEP 2: CONFIGURATION ─────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_MODEL   = "llama3-70b-8192"
EMBED_MODEL  = "all-MiniLM-L6-v2"
TOP_K        = 3

# ── STEP 3: PAGE CONFIG ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Savory Spot 🍴",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── STEP 4: PREMIUM CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #2a1a00 0%, #3b2200 50%, #2a1a00 100%);
}
h1 {
    color: #ffd700 !important;
    text-align: center;
    font-family: Georgia, serif;
}
p, .stMarkdown p {
    color: #ffffff !important;
    font-family: Georgia, serif;
    font-size: 18px !important;
    font-weight: 700 !important;
}
.stChatMessage {
    background: rgba(35, 18, 0, 1) !important;
    border: 2px solid #ffb84d !important;
    border-radius: 16px !important;
    margin-bottom: 10px !important;
    padding: 14px !important;
}
.stChatMessage p,
.stChatMessage div,
.stChatMessage span,
.stChatMessage .stMarkdown {
    color: #ffffff !important;
    font-size: 19px !important;
    font-weight: 800 !important;
    line-height: 1.8 !important;
}
.stChatInput textarea {
    background: #2a1a00 !important;
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 2px solid #ffb84d !important;
    border-radius: 12px !important;
}
section[data-testid="stSidebar"] {
    background: rgba(20, 8, 0, 0.98) !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] span {
    color: #ffffff !important;
    font-weight: bold !important;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffd700 !important;
}
.stButton button {
    background: linear-gradient(135deg, #ffb84d, #ffd700) !important;
    color: #000000 !important;
    font-weight: bold !important;
    font-size: 16px !important;
    border-radius: 10px !important;
    border: none !important;
    width: 100%;
    margin-bottom: 6px;
}
hr {
    border-color: #ffb84d !important;
}
</style>
""", unsafe_allow_html=True)

# ── STEP 5: LOAD MODELS & FAISS ───────────────────────────────────────────────
@st.cache_resource
def load_models_and_index():
    embedder = SentenceTransformer(EMBED_MODEL)
    embeddings = embedder.encode(
        restaurant_chunks,
        show_progress_bar=False,
        convert_to_numpy=True
    ).astype(np.float32)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return embedder, index

with st.spinner("🍴 Preparing restaurant AI..."):
    embedder, faiss_index = load_models_and_index()

# ── STEP 6: GROQ CLIENT ───────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)

groq_client = get_groq_client()

# ── STEP 7: SYSTEM PROMPT ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a friendly restaurant assistant for Savory Spot.
Only answer from the restaurant knowledge.
If unrelated, politely say you are only for restaurant questions.
Use warm restaurant tone with emojis.
"""

# ── STEP 8: SEMANTIC SEARCH ───────────────────────────────────────────────────
def retrieve_relevant_chunks(question: str, top_k: int = TOP_K):
    vector = embedder.encode([question], convert_to_numpy=True).astype(np.float32)
    distances, indices = faiss_index.search(vector, top_k)
    retrieved = [restaurant_chunks[i] for i in indices[0] if i != -1]
    return "\n\n---\n\n".join(retrieved)

# ── STEP 9: MAIN UI ───────────────────────────────────────────────────────────
st.markdown("# 🍴 Savory Spot")
st.markdown(
    "<p style='text-align:center;'>Your virtual restaurant assistant 🍽️</p>",
    unsafe_allow_html=True
)
st.divider()

# ── STEP 10: SIDEBAR ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍽️ Quick Questions")
    questions = [
        "🥗 What appetizers do you have?",
        "🍝 Show main course menu",
        "🍰 Dessert options?",
        "🕐 Opening hours?",
        "🚗 Delivery available?",
        "📶 WiFi available?",
        "🎉 Can I book events?"
    ]
    for q in questions:
        if st.button(q):
            st.session_state["quick_question"] = q

# ── STEP 11: SESSION ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "quick_question" not in st.session_state:
    st.session_state["quick_question"] = None

# ── STEP 12: SHOW HISTORY ─────────────────────────────────────────────────────
for msg in st.session_state["messages"]:
    avatar = "🍴" if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── STEP 13: INPUT ────────────────────────────────────────────────────────────
user_input = None
if st.session_state["quick_question"]:
    user_input = st.session_state["quick_question"]
    st.session_state["quick_question"] = None

typed_input = st.chat_input("Ask anything about the restaurant...")
if typed_input:
    user_input = typed_input

# ── STEP 14: RESPONSE ─────────────────────────────────────────────────────────
if user_input:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.spinner("🍴 Preparing your answer..."):
        context = retrieve_relevant_chunks(user_input)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{context}\n\nQuestion: {user_input}"}
        ]
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.4,
            max_tokens=500
        )
        reply = response.choices[0].message.content

    with st.chat_message("assistant", avatar="🍴"):
        st.markdown(reply)

    st.session_state["messages"].append({"role": "assistant", "content": reply})
