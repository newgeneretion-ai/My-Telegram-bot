import telebot
import requests
import os

# चाबियाँ
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)

def get_ai_response(text):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        data = {
            "model": "llama-3.3-70b-versatile", # मैंने मॉडल अपडेट कर दिया है
            "messages": [{"role": "user", "content": text}]
        }
        res = requests.post(url, headers=headers, json=data).json()
        
        # सुरक्षा के लिए चेक
        if 'choices' in res:
            return res['choices'][0]['message']['content']
        else:
            return f"Bhai, AI ne ye error diya hai: {res.get('error', {}).get('message', 'Unknown Error')}"
    except Exception as e:
        return f"System Error: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "नमस्ते भाई! इंटेल नेक्सस एआई अब पूरी तरह तैयार है। कुछ भी पूछें!")

@bot.message_handler(func=lambda message: True)
def chat(message):
    ans = get_ai_response(message.text)
    bot.reply_to(message, ans)

print("Bot Restarting...")
bot.polling(none_stop=True)
