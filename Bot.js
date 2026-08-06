const TelegramBot = require('node-telegram-bot-api');

// Render Environment Variables से टोकन लोड होगा
const token = process.env.TELEGRAM_TOKEN;

if (!token) {
  console.error("Error: TELEGRAM_TOKEN not found in environment variables!");
  process.exit(1);
}

// बॉट चालू करें
const bot = new TelegramBot(token, { polling: true });

// /start कमांड का जवाब
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'नमस्ते! आपका टेलीग्राम बॉट Render पर 24/7 सफलतापूर्वक काम कर रहा है।');
});

// सामान्य मैसेज का जवाब
bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;

  if (text && !text.startsWith('/start')) {
    bot.sendMessage(chatId, `आपने कहा: ${text}`);
  }
});

console.log("बॉट सफलतापूर्वक चालू हो गया है...");
