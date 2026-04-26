import os, requests, smtplib
from datetime import datetime
from groq import Groq
from email.message import EmailMessage

# GitHub Secrets se credentials lega
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def run_background_agent():
    # Topics ka mix: AI for your studies, Cricket for your YouTube channel
    topics = ["Artificial Intelligence", "IPL Cricket India"]
    combined_news = ""
    
    for t in topics:
        try:
            r = requests.get(f"https://newsapi.org/v2/everything?q={t}&pageSize=3&apiKey={NEWS_API_KEY}").json()
            articles = r.get("articles", [])
            for a in articles:
                if "[Removed]" not in a['title']:
                    combined_news += f"\n- {a['title']}"
        except:
            continue

    # 2. Summarizing with Llama 3.1
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are Alpha Agent. Summarize these news points into a sharp, 3-sentence intelligence briefing with a futuristic tone."},
            {"role": "user", "content": f"Intelligence Data: {combined_news}"}
        ]
    )
    report = response.choices[0].message.content

    # 3. Sending Email
    msg = EmailMessage()
    msg.set_content(f"🐺 ALPHA DAILY INTELLIGENCE DISPATCH\nDate: {datetime.now().strftime('%d %b %Y')}\n\n{report}\n\nStay Sharp,\nAlpha Agent")
    msg['Subject'] = f"🐺 ALPHA INTEL REPORT | {datetime.now().strftime('%d %b')}"
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER 

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
    print("Intelligence Dispatch Successful!")

if __name__ == "__main__":
    run_background_agent()
