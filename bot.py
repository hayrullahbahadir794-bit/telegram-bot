import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# TOKEN Render'da Environment Variable olarak eklenecek
TOKEN = os.getenv("BOT_TOKEN")

# Basit hafıza (küçük botlar için yeterli)
users = {}  # user_id: {"ref": ref_id, "count": 0}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # Referans parametresi var mı?
    ref_id = None
    if context.args:
        try:
            ref_id = int(context.args[0])
        except:
            ref_id = None

    # Kullanıcı ilk kez giriyorsa
    if user_id not in users:
        users[user_id] = {"ref": ref_id, "count": 0}

        # Referans varsa ve geçerliyse
        if ref_id and ref_id in users and ref_id != user_id:
            users[ref_id]["count"] += 1

    my_ref_link = f"https://t.me/{context.bot.username}?start={user_id}"

    await update.message.reply_text(
        f"👋 Hoş geldin {user.first_name}!\n\n"
        f"🔗 Senin referans linkin:\n{my_ref_link}\n\n"
        f"👥 Toplam referansın: {users[user_id]['count']}"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    count = users.get(user_id, {}).get("count", 0)
    await update.message.reply_text(f"👥 Toplam referansın: {count}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.run_polling()

if __name__ == "__main__":
    main()
