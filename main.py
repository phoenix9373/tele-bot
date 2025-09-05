from flask import Flask
import threading, os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Flask 서버
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot running!"

# 텔레그램 봇 코드
TOKEN = os.getenv("BOT_TOKEN")  # Replit 환경변수로 설정

async def everyone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    admins = await context.bot.get_chat_administrators(chat_id)
    mentions = []
    for admin in admins:
        user = admin.user
        if user.username:
            mentions.append(f"@{user.username}")
        else:
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")
    message = " ".join(context.args) or "전체 알림!"
    text = f"{message}\n\n" + " ".join(mentions)
    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("everyone", everyone))

# 봇을 백그라운드에서 실행
threading.Thread(target=lambda: bot_app.run_polling()).start()

# Flask 서버 실행
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

