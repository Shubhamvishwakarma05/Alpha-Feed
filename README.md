# 🐺 Alpha Feed: Elite AI News Intelligence

**Alpha Feed** is a high-performance news aggregation engine built with Python and Streamlit. It leverages Large Language Models (LLMs) via the Groq API to provide real-time intelligence summaries, sentiment-driven news feeds, and vocal briefings. Designed for professionals who need high-density information without the clutter.

---

## 🚀 Features

- **AI-Powered Summarization:** Uses `Llama-3.1-8b` to distill multiple news articles into two sharp, actionable sentences.
- **Dynamic Data Interception:** Real-time fetching of news across multiple global targets using the NewsAPI.
- **Vocal Intelligence:** Integrated Text-to-Speech (TTS) to generate audio reports for hands-free consumption.
- **Premium UI/UX:** A sleek "Deep Ocean & Lava Gold" theme with responsive grid layouts and interactive card scaling.
- **Custom Targets:** Users can define specific interest areas (e.g., AI, SpaceX, Markets) via the Command Center.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) (Python-based Web Framework)
- **AI/LLM:** [Groq Cloud](https://groq.com/) (Llama 3.1 Model)
- **Data Source:** [NewsAPI](https://newsapi.org/)
- **Audio Engine:** Groq Audio (Orpheus-v1)
- **Styling:** Custom CSS (Glassmorphism & Radial Gradients)

---

**Alpha Feed** asaliyat mein Llama 3.1 ko ek **"Engine"** ki tarah use karta hai, jisme logic ka flow kuch is tarah chalta hai:

### 1. The API Bridge (Groq)
Llama 3.1 ek bahut bada model hai, jise local machine par chalana mushkil hai. Isliye hum **Groq Cloud** use karte hain. Groq ke paas **LPU (Language Processing Unit)** hota hai, jo Llama 3.1 ko "Bijli ki raftaar" (ultra-fast speed) par chalata hai. Jab tu "Trigger" button dabata hai, toh Python code Groq ko ek request bhejta hai.

### 2. Context Injection (The Secret Sauce)
Llama 3.1 ko ye nahi pata ki aaj duniya mein kya ho raha hai (kyunki uska data purana ho sakta hai). Hum kya karte hain?
* Pehle hum **NewsAPI** se fresh news nikalte hain.
* Phir hum us news text ko Llama 3.1 ke **Prompt** (input) mein "chipka" dete hain.
* Ise kehte hain **In-Context Learning**. Hum model ko bolte hain: *"Bhai, teri purani knowledge side mein rakh, ye dekh aaj ki news aur iske basis par jawab de."*

### 3. Systematic Prompting
Humne code mein Llama 3.1 ko do tarah se instruct kiya hai:

* **Summarizer Mode:** Ismein hum Llama ko `temperature=0.4` par rakhte hain taaki wo "Creative" na ho aur sirf factual summary de.
* **Agent Mode:** Ismein hum Llama ko ek **System Message** dete hain: *"You are an Alpha Wolf Agent."* Ye instruction Llama ki puri personality aur decision-making style badal deta hai.



### 4. Zero-Shot & Few-Shot Reasoning
Llama 3.1 ki khaas baat ye hai ki ye bina kisi training ke (Zero-shot) samajh jata hai ki use summarize karna hai ya analyze. Wo saari news ke beech ka **Correlation** (rishta) dhund leta hai.
* *Example:* Agar ek news Elon Musk ki hai aur dusri Crypto ki, toh Llama 3.1 khud dimag laga lega ki Musk ke tweet se Crypto par kya asar padega.

### 5. Managing States (Memory)
Jab tu Agent se chat karta hai, toh hum Llama 3.1 ko sirf tera current message nahi bhejte, balki `st.session_state.messages` ke zariye poori **Conversation History** bhejte hain. Isse Llama ko lagta hai ki wo tere saath ek lambi baatchit kar raha hai.

**Technical Summary:**
Tera Python code **Orchestrator** hai, NewsAPI **Data Provider** hai, aur Llama 3.1 wo **High-IQ Processor** hai jo saare dots ko connect karke tujhe output deta hai.

Bhai, ye architecture samajh gaya toh tu Interview mein kisi ko bhi hila dega! 🐺🔥 Kuch aur deep-dive karna hai ismein?

## 📦 Installation & Setup

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/alpha-feed.git](https://github.com/your-username/alpha-feed.git)
   cd alpha-feed
