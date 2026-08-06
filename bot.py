import telebot
import requests
import smtplib
import os
from email.mime.text import MIMEText

# चाबियाँ (Secrets)
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
MY_EMAIL = os.environ.get('EMAIL_USER')
MY_EMAIL_PASS = os.environ.get('EMAIL_PASS')

bot = telebot.TeleBot(BOT_TOKEN)

# AI से ईमेल लिखवाने का फंक्शन
def generate_ai_pitch(details):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    prompt = f"Write a killer business proposal email for: {details}. Make it professional, persuasive and short. The goal is to get a reply."
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post(url, headers=headers, json=data).json()
    return res['choices'][0]['message']['content']

# ईमेल भेजने का इंजन
def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = MY_EMAIL
        msg['To'] = to_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MY_EMAIL, MY_EMAIL_PASS)
            server.sendmail(MY_EMAIL, to_email, msg.as_string())
        return True
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 AI Hunter System Live!\n\n/hunt [Client Email] | [Client Service]\nउदाहरण: /hunt test@gmail.com | Digital Marketing for Hotel")

@bot.message_handler(commands=['hunt'])
def hunt(message):
    try:
        parts = message.text.split('|')
        target_email = parts[0].replace('/hunt', '').strip()
        service_name = parts[1].strip()

        bot.reply_to(message, "🎯 AI क्लाइंट के लिए पिच तैयार कर रहा है और ईमेल भेज रहा है...")
        
        # AI पिच बनाना
        pitch = generate_ai_pitch(service_name)
        # ईमेल भेजना
        status = send_email(target_email, "Business Opportunity", pitch)
        
        if status:
            bot.send_message(message.chat.id, f"✅ सफलता! ईमेल भेज दिया गया है।\n\n**AI द्वारा लिखी गई पिच:**\n{pitch}")
        else:
            bot.send_message(message.chat.id, "❌ ईमेल नहीं जा सका। Gmail App Password चेक करें।")
    except:
        bot.reply_to(message, "गलत फॉर्मेट! /hunt email | service लिखें।")

@bot.message_handler(func=lambda message: True)
def chat(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": message.text}]}
    res = requests.post(url, headers=headers, json=data).json()
    bot.reply_to(message, res['choices'][0]['message']['content'])

bot.polling(none_stop=True)
