import streamlit as st
import requests
import smtplib
from datetime import datetime
from email.message import EmailMessage
from groq import Groq

# ─────────────────────────────────────────────
#  API KEYS (Fetching from Streamlit Secrets)
# ─────────────────────────────────────────────
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Alpha Feed | Premium AI News",
    page_icon="🐺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  VIBRANT COLORFUL UI WITH HERO IMAGE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');

[data-testid="stAppViewContainer"] {
    background-color: #0d1117;
}

/* Hero Section with Background Image */
.hero-section {
    background: linear-gradient(rgba(13, 17, 23, 0.8), rgba(13, 17, 23, 0.8)), 
                url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=2072');
    background-size: cover;
    background-position: center;
    padding: 80px 20px;
    text-align: center;
    border-bottom: 1px solid #1f2937;
    margin-bottom: 30px;
}

[data-testid="stSidebar"] {
    background-color: rgba(15, 20, 30, 0.95) !important;
    border-right: 1px solid #1f2937;
}

.ai-summary-container {
    background: #161b22;
    border-radius: 12px;
    border-left: 5px solid #ffa500;
    padding: 25px;
    margin-bottom: 25px;
}

.news-card {
    background: #161b22;
    border-radius: 12px;
    border: 1px solid #21262d;
    padding: 20px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.news-card:hover {
    border-color: #ffa500;
    transform: translateY(-3px);
    box-shadow: 0 8px 15px rgba(255, 165, 0, 0.15);
}

.masthead-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 5rem;
    font-weight: 900;
    color: #fff;
    letter-spacing: -2px;
    margin: 0;
}

.date-text {
    text-align: center;
    color: #ffa500;
    letter-spacing: 5px;
    font-weight: 700;
    font-size: 0.85rem;
    margin-top: 10px;
    text-transform: uppercase;
    background: rgba(0,0,0,0.3);
    display: inline-block;
    padding: 5px 20px;
    border-radius: 50px;
}

.stButton > button {
    background: linear-gradient(90deg, #ff8c00 0%, #ff4500 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    padding: 12px !important;
    text-transform: uppercase;
    width: 100%;
}

/* Footer Styling */
.footer {
    background-color: rgba(13, 17, 23, 0.6);
    color: #555;
    text-align: center;
    padding: 40px 20px;
    margin-top: 50px;
    border-top: 1px solid #222;
    font-family: 'Outfit', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO MASTHEAD
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
    <div class="masthead-title">ALPHA FEED</div>
    <div style="text-align:center;">
        <div class="date-text">
            ELITE DATA STREAM • {datetime.now().strftime("%d %b %Y").upper()}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_colorful_news(topics: list, count: int):
    results = {}
    for t in topics:
        try:
            r = requests.get("https://newsapi.org/v2/everything",
                             params={"q": t, "pageSize": count, "apiKey": NEWS_API_KEY}).json()
            articles = []
            for a in r.get("articles", []):
                if a.get("title") and "[Removed]" not in a["title"]:
                    articles.append({
                        "title": a["title"],
                        "desc": a["description"] or "Click source to read full story.",
                        "url": a["url"],
                        "img": a["urlToImage"],
                        "src": a["source"]["name"]
                    })
            results[t] = articles
        except:
            results[t] = []
    return results


def summarize_with_groq(articles_by_topic: dict) -> list:
    client = Groq(api_key=GROQ_API_KEY)
    summary_list = []
    for topic, articles in articles_by_topic.items():
        if not articles: continue
        titles = "\n".join([f"- {a['title']}" for a in articles[:3]])
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "Summarize this news in two sharp sentences."},
                      {"role": "user", "content": f"Topic: {topic}\nNews: {titles}"}],
            temperature=0.4,
        )
        summary_list.append((topic, response.choices[0].message.content))
    return summary_list


def generate_alpha_audio(text: str, voice_id: str):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        response = client.audio.speech.create(model="canopylabs/orpheus-v1-english", voice=voice_id, input=text,
                                              response_format="wav")
        f = "alpha_audio_stream.wav"
        response.write_to_file(f)
        return f
    except:
        return None


def send_alpha_email(report_text, receiver_email):
    msg = EmailMessage()
    msg.set_content(
        f"🐺 ALPHA INTELLIGENCE REPORT\n{'=' * 30}\n\n{report_text}\n\n{'=' * 30}\nSent via Alpha Feed Agent")
    msg['Subject'] = f"🐺 ALPHA INTEL | {datetime.now().strftime('%d %b %Y')}"
    msg['From'] = st.secrets["EMAIL_USER"]
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASS"])
            smtp.send_message(msg)
        return True
    except Exception as e:
        return False


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🐺 News Controls")
    topics_raw = st.text_area(
        "Targets",
        value="Artificial Intelligence\nStock Market\nIndian Startups",
        height=150,
        placeholder="Yahan apne topics likhein (Example: Cricket, SpaceX, Tesla)..."
    )
    articles_per_topic = st.slider("Signal Density", 3, 10, 5)

    st.markdown("---")
    st.markdown("### 🎙️ Voice Settings")
    voice_map = {"Male (Troy)": "troy", "Female (Hannah)": "hannah"}
    selected_voice_label = st.selectbox("Narrator", list(voice_map.keys()))
    selected_voice_id = voice_map[selected_voice_label]

    st.markdown("---")
    run_btn = st.button("🚀 EXECUTE ALPHA SCAN")
    st.caption("Authorized by: Shubham Vishwakarma")

# ─────────────────────────────────────────────
#  MAIN LOGIC
# ─────────────────────────────────────────────
if run_btn:
    topics = [t.strip() for t in topics_raw.strip().split("\n") if t.strip()]
    with st.spinner("🌌 Scanning global networks..."):
        data = fetch_colorful_news(topics, articles_per_topic)
        st.session_state['news'] = data
        st.session_state['summaries'] = summarize_with_groq(data)

if 'summaries' in st.session_state:
    st.markdown(
        '<div style="color:#ffa500; font-weight:700; letter-spacing:4px; font-size:0.8rem; margin-bottom:20px; padding: 0 20px;">🤖 ALPHA INTELLIGENCE</div>',
        unsafe_allow_html=True)

    combined_summary_text = ""
    for topic, summary in st.session_state['summaries']:
        st.markdown(f"""
        <div style="padding: 0 20px;">
            <div class="ai-summary-container">
                <div style="color: #ffa500; font-weight: 900; letter-spacing: 2px; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 10px;">{topic.upper()}</div>
                <div style="color:#e6edf3; font-size:1.05rem; line-height:1.7;">{summary}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        combined_summary_text += f" News for {topic}. {summary} "

    # ─── DISPATCH UI (Updated) ───
    st.markdown('<div style="padding: 0 20px;">', unsafe_allow_html=True)

    col_audio, col_email = st.columns([1, 1.5])

    with col_audio:
        st.markdown("### 🔊 Audio Feed")
        if st.button("PLAY AUDIO REPORT"):
            with st.spinner("🎙️ Generating..."):
                audio_path = generate_alpha_audio(combined_summary_text, selected_voice_id)
                if audio_path:
                    st.audio(audio_path, format="audio/wav", autoplay=True)

    with col_email:
        st.markdown("### 📧 Email Dispatch")
        email_target = st.text_input("Enter Receiver Email", value="user@example.com")
        if st.button("🚀 DISPATCH TO MAIL"):
            with st.spinner("📤 Sending intelligence..."):
                if send_alpha_email(combined_summary_text, email_target):
                    st.success(f"✅ Intelligence sent to {email_target}")
                else:
                    st.error("❌ Dispatch failed! Verify Secrets.")

    st.markdown('</div>', unsafe_allow_html=True)
    # ─── End of Dispatch UI ───

    st.markdown(
        '<div style="color:#ffa500; font-weight:700; letter-spacing:4px; font-size:0.8rem; margin-top:50px; margin-bottom:20px; padding: 0 20px;">📰 DISCOVER FEED</div>',
        unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 10px;">', unsafe_allow_html=True)
    cols = st.columns(2)
    idx = 0
    for topic, articles in st.session_state['news'].items():
        for a in articles:
            with cols[idx % 2]:
                img_html = f'<img src="{a["img"]}" style="width:100%; border-radius:10px; margin-bottom:15px; border:1px solid #333;">' if a.get(
                    "img") else ""
                st.markdown(f"""
                <div class="news-card">
                    <div style="color:#ff8c00; font-size:0.6rem; font-weight:700; letter-spacing:2px; margin-bottom:10px; text-transform:uppercase;">{topic.upper()}</div>
                    {img_html}
                    <div style="font-size:1.25rem; font-weight:700; color:#fff; margin-bottom:10px; line-height:1.3;">{a['title']}</div>
                    <p style="color:#8b949e; font-size:0.95rem; line-height:1.6;">{a['desc']}</p>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:20px; border-top:1px solid #222; padding-top:10px;">
                        <span style="color:#555; font-size:0.8rem;">{a['src']}</span>
                        <a href="{a['url']}" target="_blank" style="color:#ffa500; text-decoration:none; font-weight:700; font-size:0.85rem;">ACCESS →</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            idx += 1
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ALPHA INTELLIGENCE AGENT (The Brain)
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("<h2 style='text-align:center;'>🐺 CONSULT ALPHA AGENT</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Analyze today's intelligence..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = Groq(api_key=GROQ_API_KEY)
        context_data = ""
        if 'news' in st.session_state:
            for topic, arts in st.session_state['news'].items():
                context_data += f"\nTopic: {topic}\n" + "\n".join([f"- {a['title']}" for a in arts[:3]])

        system_prompt = f"You are ALPHA AGENT. Context: {context_data}. Be sharp and insightful."
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
        )
        ans = response.choices[0].message.content
        st.markdown(ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})

# ─────────────────────────────────────────────
#  PROFESSIONAL FOOTER
# ─────────────────────────────────────────────
st.markdown("""
    <div class="footer">
        <div style="font-size: 0.85rem; letter-spacing: 1px;">
            COPYRIGHT © 2026 | <span style="color: #ffa500; font-weight: 700;">ALPHA FEED</span> | ALL RIGHTS RESERVED
        </div>
        <div style="font-size: 0.7rem; margin-top: 10px; color: #444; letter-spacing: 2px;">
            DEVELOPED BY <span style="color: #888;">SHUBHAM VISHWAKARMA</span>
        </div>
        <div style="font-size: 0.6rem; margin-top: 15px; color: #333; font-style: italic;">
            Disclaimer: Content generated by AI. Cross-verify critical intelligence before action.
        </div>
    </div>
""", unsafe_allow_html=True)
