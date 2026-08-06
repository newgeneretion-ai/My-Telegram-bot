import telebot
import requests
import smtplib
import os
from email.mime.text import MIMEText

# Render के Environment Variables से चाबियाँ उठाना
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
MY_EMAIL = os.environ.get('EMAIL_USER')
MY_EMAIL_PASS = os.environ.get('EMAIL_PASS')

bot = telebot.TeleBot(BOT_TOKEN)

# AI से प्रोफेशनल ईमेल लिखवाने का फंक्शन
def generate_ai_email(client_info):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    prompt = f"Write a professional business proposal email for this client: {client_info}. The email should be persuasive and professional. Keep it concise."
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post(url, headers=headers, json=data).json()
    return res['choices'][0]['message']['content']

# ईमेल भेजने का फंक्शन
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
    except Exception as e:
        print(f"Error: {e}")
        return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 Intel Nexus AI Live! \n\nकाम कैसे करें:\n1. AI से बात करने के लिए सीधा मैसेज लिखें।\n2. AI से ऑटो-ईमेल भेजने के लिए लिखें: \n/automail [client_email] | [client_details]")

@bot.message_handler(commands=['automail'])
def handle_auto_mail(message):
    try:
        # फॉर्मेट: /automail test@gmail.com | Mumbai Hotel Owner
        parts = message.text.split('|')
        target_email = parts[0].replace('/automail', '').strip()
        details = parts[1].strip()

        bot.reply_to(message, "🤖 AI ईमेल लिख रहा है और भेज रहा है...")
        
        # 1. AI से ईमेल लिखवाएं
        ai_content = generate_ai_email(details)
        
        # 2. ईमेल भेजें
        subject = "Business Collaboration Proposal"
        success = send_email(target_email, subject, ai_content)
        
        if success:
            bot.send_message(message.chat.id, f"✅ ईमेल सफलतापूर्वक भेजा गया!\n\n**भेजा गया कंटेंट:**\n{ai_content}")
        else:
            bot.send_message(message.chat.id, "❌ ईमेल नहीं जा सका। अपना App Password चेक करें।")
    except:
        bot.reply_to(message, "गलत फॉर्मेट! ऐसे लिखें:\n/automail test@gmail.com | Digital Marketing service for gym")

@bot.message_handler(func=lambda message: True)
def chat(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": message.text}]
    }
    res = requests.post(url, headers=headers, json=data).json()
    bot.reply_to(message, res['choices'][0]['message']['content'])

print("System is Live on Render...")
bot.polling()
