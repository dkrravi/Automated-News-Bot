import requests
import time
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
TOPIC = "India Pakistan Conflict"
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP_NUMBER = "whatsapp:+14155238886"
TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def get_latest_news():
    url = (
        f"https://newsapi.org/v2/everything?q={TOPIC}&from=2025-04-09"
        f"&sortBy=publishedAt&apiKey={NEWSDATA_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "ok" and data.get("articles"):
        messages = []
        for article in data["articles"][:3]:
            title = article["title"]
            source = article.get("source", {}).get("name", "Unknown")
            pub_date = article["publishedAt"]
            link = article["url"]
            messages.append(f"🗞️ *{title}*\n📍{source} | 🕒 {pub_date}\n🔗 {link}")
        return "\n\n".join(messages)
    return "⚠️ No news found."

def send_whatsapp_message(message):
    client.messages.create(
        from_=FROM_WHATSAPP_NUMBER,
        body=message,
        to=TO_WHATSAPP_NUMBER
    )

if __name__ == "__main__":
    while True:
        try:
            news = get_latest_news()
            send_whatsapp_message(news)
            print("WhatsApp message sent!")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(3600)
