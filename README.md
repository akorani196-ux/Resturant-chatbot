# 🍴 Savory Spot — Advanced RAG Restaurant Chatbot

> A smart, interactive restaurant assistant powered by **Groq LLaMA 3.3**, **FAISS semantic search**, and **Streamlit** — built with RAG (Retrieval Augmented Generation) technology.

---

## 📸 What It Looks Like

```
┌─────────────────────────────────────────────────────────┐
│  🍽️  Savory Spot — Virtual Assistant                    │
│─────────────────────────────────────────────────────────│
│  💬 Chat  │  📖 Full Menu  │  🛒 Order Builder  │  ℹ️   │
│─────────────────────────────────────────────────────────│
│                                                         │
│  🍴  Welcome to Savory Spot!                            │
│      Ask about menu, hours, delivery, offers...         │
│                                                         │
│  📚 Source: 🍝 Main Course ● 🥗 Appetizers ●           │
│  💡 You might also ask: [🍷 Drinks] [🍰 Desserts]      │
│                                                         │
│  [ Ask anything about the restaurant...        ] Send   │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| ⚡ **FAQ Instant Answers** | Common questions (WiFi, hours, parking) answered instantly — no AI call needed |
| 🔍 **Hybrid Search** | Semantic (meaning) + Keyword (exact match) combined for best accuracy |
| 📚 **Source Badges** | Every answer shows exactly where the info came from |
| 🟢 **Confidence Scoring** | High / Medium / Low confidence shown on every answer |
| 💡 **Follow-up Suggestions** | Clickable chips after every answer to explore related topics |
| 📖 **Menu Explorer** | Browse full menu with search + vegetarian/vegan/GF filters |
| 🛒 **Order Builder** | Add items, adjust qty, see running total, send order to chat |
| ⌨️ **Typing Animation** | Replies stream character by character like a real person typing |
| 👍👎 **Feedback Buttons** | Rate every answer — helpful or not |
| 📥 **Export Chat** | Download full conversation as a `.txt` file |
| 📊 **Session Stats** | Track total questions asked and instant answers used |
| 🗑️ **Clear Chat** | Reset conversation any time from the sidebar |

---

## 📁 Project Files

```
Restaurant_Chatbot/
│
├── app.py                 ← Main Streamlit UI (run this file)
├── restaurant_data.py     ← All restaurant knowledge + menu + FAQs
├── rag_engine.py          ← AI logic (search, LLM, RAG pipeline)
└── README.md              ← This file
```

### What Each File Does

**`app.py`**
- Streamlit web interface
- Gold/dark premium theme (your original style kept)
- 4 tabs: Chat, Full Menu, Order Builder, How It Works
- Sidebar with quick questions, cart preview, session stats

**`restaurant_data.py`**
- `CHUNKS` — 15 knowledge chunks (menu, hours, services, policy, etc.)
- `MENU_ITEMS` — Structured menu for Menu Explorer and Order Builder
- `FAQ_PAIRS` — 15 instant answers for common questions
- `FOLLOW_UP_SUGGESTIONS` — Topic-aware clickable suggestions

**`rag_engine.py`**
- `build_index()` — Converts chunks to vectors, builds FAISS index
- `hybrid_search()` — Semantic + keyword combined search
- `check_faq()` — Instant FAQ answer checker
- `get_follow_ups()` — Picks relevant follow-up suggestions
- `ask_groq()` — Sends context + question to Groq LLM
- `chat()` — Master function that runs the full pipeline

---

## 🚀 How to Run

### Step 1 — Install Required Libraries

Open your terminal and run:

```bash
pip install streamlit
pip install groq
pip install sentence-transformers
pip install faiss-cpu
pip install numpy
```

> ✅ Run these one by one. If any says "already installed" — that's fine, skip it.

### Step 2 — Add Your Groq API Key

Open `app.py` and find **line 42**:

```python
GROQ_API_KEY = "your_groq_api_key_here"
```

Replace with your actual key. Get a **free key** at:
👉 https://console.groq.com → Sign up → API Keys → Create Key

### Step 3 — Put All Files in One Folder

Make sure all 3 files are in the **same folder**:

```
D:\LangChain\Restaurant_Chatbot\
    ├── app.py
    ├── restaurant_data.py
    └── rag_engine.py
```

### Step 4 — Run the App

```bash
cd D:\LangChain\Restaurant_Chatbot
streamlit run app.py
```

Then open your browser at: **http://localhost:8501**

---

## 🧠 How RAG Works (Simple Explanation)

```
User asks: "Do you have vegetarian pasta?"
              │
              ▼
    ⚡ Step 1: FAQ Check
    (Is this a known instant question? No → continue)
              │
              ▼
    🔍 Step 2: Hybrid Search
    ┌─────────────────────────────────┐
    │ Semantic Search (FAISS/vectors) │  ← understands MEANING
    │ + Keyword Search (tag matching) │  ← catches EXACT words
    │ Combined: 70% semantic +        │
    │           30% keyword           │
    └─────────────────────────────────┘
              │
              ▼
    📄 Top 3 most relevant knowledge
       chunks retrieved from database
              │
              ▼
    🤖 Step 3: Groq LLaMA 3.3 called
    (Only those 3 chunks + question sent — NOT the whole database)
              │
              ▼
    💬 Answer shown with source badges + confidence score
    💡 Follow-up suggestions displayed
```

**Why RAG is better than regular chatbot:**
- Regular chatbot: Makes up answers ❌
- RAG chatbot: Only answers from real restaurant data ✅
- Regular chatbot: Sends everything to AI (slow, expensive) ❌
- RAG chatbot: Sends only relevant parts (fast, accurate) ✅

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.11 |
| **UI Framework** | Streamlit |
| **LLM** | Groq API — LLaMA 3.3 70B Versatile |
| **Embeddings** | sentence-transformers `all-MiniLM-L6-v2` |
| **Vector Search** | FAISS (Facebook AI Similarity Search) |
| **Search Type** | Hybrid (Semantic + Keyword) |

---

## 📖 Restaurant Knowledge Base

The chatbot knows about **15 topics**:

| # | Topic | What It Covers |
|---|---|---|
| 1 | 🏠 General Info | Address, phone, email, about us |
| 2 | 🕐 Opening Hours | Daily hours, holidays, kitchen close time |
| 3 | 🥗 Appetizers | Full starter menu with prices |
| 4 | 🍝 Main Courses | Full main menu with prices |
| 5 | 🍰 Desserts | Full dessert menu with prices |
| 6 | 🍷 Drinks | Wines, cocktails, mocktails, coffee |
| 7 | 🌱 Dietary Info | Vegan, vegetarian, GF, halal, allergens |
| 8 | 📋 Reservations | Booking policy, deposits, cancellation |
| 9 | 🚗 Delivery | Delivery zones, fees, hours, takeaway |
| 10 | 📶 WiFi & Facilities | Password, parking, wheelchair access |
| 11 | 🎉 Private Events | Venue hire, corporate, birthday packages |
| 12 | 💳 Loyalty & Offers | Rewards, happy hour, student discount |
| 13 | 🌟 Chef's Specials | Seasonal dishes, tasting menu |
| 14 | 👨‍🍳 Our Team | Founders, head chef, pastry chef, story |
| 15 | 💰 Payment & Service | Cards, tips, service charge, bill split |

---

## ⚡ FAQ Instant Answers (No AI Needed)

These questions get instant answers without calling the LLM:

- "WiFi password" → Shows network + password immediately
- "Opening hours" → Shows full schedule
- "Where are you" → Shows address
- "Delivery fee" → Shows fee + minimum order
- "Happy hour" → Shows times and discount
- "Student discount" → Shows percentage
- "Parking" → Shows parking info
- "Dress code" → Shows dress code
- "Is food halal" → Shows halal info
- "Vegan options" → Lists vegan dishes

---

## ❓ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: streamlit` | Run `pip install streamlit` |
| `ModuleNotFoundError: faiss` | Run `pip install faiss-cpu` |
| `ModuleNotFoundError: restaurant_data` | All 3 files must be in the **same folder** |
| `AuthenticationError` from Groq | Check your API key in `app.py` line 42 |
| Port already in use | Run `streamlit run app.py --server.port 8502` |
| Slow first load | Normal — embedding model downloads ~90MB once, then cached |
| White screen in browser | Wait 10 seconds and refresh |

---

## 📞 Restaurant Contact Info

| | |
|---|---|
| 📍 Address | 22 Golden Avenue, Maplewood City |
| 📞 Phone | +1 (555) 310-9900 |
| 📧 Email | hello@savoryspot.com |
| 🌐 Website | savoryspot.com |
| 📸 Instagram | @savoryspot |

---

## 👨‍💻 Project Info

- **Built with:** Python + Streamlit + Groq + FAISS
- **Python version:** 3.11
- **Platform:** Windows (VS Code)
- **Project folder:** `D:\LangChain\Restaurant_Chatbot\`

---

*Made with ❤️ — Savory Spot Virtual Assistant*
