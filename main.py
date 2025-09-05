from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")  # 환경변수에 Bot 토큰 저장

async def everyone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # 채팅 멤버 목록 가져오기 (관리자 포함)
    admins = await context.bot.get_chat_administrators(chat_id)
    
    mentions = []

    for admin in admins:
        user = admin.user
        if user.is_bot:  # 봇 제외
            continue
        if user.username:
            mentions.append(f"@{user.username}")
        else:
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")

    message = " ".join(context.args) or "전체 알림!"
    text = f"{message}\n\n" + " ".join(mentions)

    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

# 봇 실행
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("everyone", everyone))
app.run_polling()

