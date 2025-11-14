# file: infobot.py (Render.com-এর জন্য আপডেটেড)
import logging
import os # ⭐️ Render-এর জন্য এটি যোগ করা হয়েছে
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# --- ⭐️ টোকেন এখন Render থেকে লোড হবে ---
# কোডের ভেতর টোকেন নেই, এটি এখন সুরক্ষিত
TOKEN = os.environ.get("TOKEN")

# লগিং চালু করা
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(application: Application):
    """বট চালু হলে মেনু সেট করে।"""
    await application.bot.set_my_commands([
        BotCommand("start", "🚀 Get your IDs"),
        BotCommand("help", "💡 How to use this bot")
    ])
    print("[✓] ID Bot commands set successfully.")

# /start কমান্ড
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ /start কমান্ড দিলে বিভিন্ন আইডি দেখায়। """
    user = update.effective_user
    chat = update.effective_chat
    
    bot_id = context.bot.id # বটের নিজের আইডি
    
    reply_text = (
        f"👋 <b>Hello, {user.first_name}!</b>\n\n"
        f"Here are your details:\n\n"
        f"👤 <b>Your User ID:</b> <code>{user.id}</code>\n"
        f"💬 <b>This Chat ID:</b> <code>{chat.id}</code>\n"
        f"🤖 <b>My Bot ID:</b> <code>{bot_id}</code>\n\n"
    )
    
    if chat.type in ['group', 'supergroup']:
        reply_text += (
            f"👥 <b>This Group ID is:</b> <code>{chat.id}</code>\n\n"
            f"To get another user's ID, ask them to forward one of their messages to me."
        )
    else:
         reply_text += "To get a <b>Group ID</b>, add me to any group and type /start."
    
    await update.message.reply_html(reply_text)

# /help কমান্ড
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """কীভাবে বট ব্যবহার করতে হবে তা দেখায়।"""
    help_text = (
        "<b>💡 How to use this ID Bot</b>\n\n"
        "<b>1. To get your own User ID:</b>\n"
        "Just type /start.\n\n"
        "<b>2. To get a Group ID:</b>\n"
        "Add me to your group and type /start in that group.\n\n"
        "<b>3. To get another User's ID:</b>\n"
        "Ask that user to forward one of their messages to me. I will show you their original User ID.\n\n"
        "<b>4. To get a Channel ID:</b>\n"
        "Forward a message from that channel to me."
    )
    await update.message.reply_html(help_text)

# ফরোয়ার্ড করা মেসেজ হ্যান্ডল করার জন্য
async def handle_forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ফরোয়ার্ড করা মেসেজ থেকে আইডি বের করে।"""
    user = update.effective_user
    
    if update.message.forward_from:
        fwd_user = update.message.forward_from
        reply_text = (
            f"👤 <b>Forwarded User Info:</b>\n\n"
            f"<b>Name:</b> {fwd_user.full_name}\n"
            f"<b>User ID:</b> <code>{fwd_user.id}</code>"
        )
        if fwd_user.username:
            reply_text += f"\n<b>Username:</b> @{fwd_user.username}"
            
        await update.message.reply_html(reply_text)
        
    elif update.message.forward_from_chat:
        fwd_chat = update.message.forward_from_chat
        reply_text = (
            f"📢 <b>Forwarded Channel Info:</b>\n\n"
            f"<b>Name:</b> {fwd_chat.title}\n"
            f"<b>Channel ID:</b> <code>{fwd_chat.id}</code>"
        )
        if fwd_chat.username:
            reply_text += f"\n<b>Username:</b> @{fwd_chat.username}"
            
        await update.message.reply_html(reply_text)
        
    else:
        await update.message.reply_text("This user has hidden their account, so I cannot get their ID from a forwarded message.")

# মূল ফাংশন
def main() -> None:
    """বটটি চালু করে।"""
    
    if not TOKEN:
        logger.error("FATAL ERROR: TOKEN environment variable is not set.")
        return # টোকেন না পেলে বট চলবে না

    application = Application.builder().token(TOKEN).post_init(post_init).build()

    # কমান্ড হ্যান্ডলার
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # মেসেজ হ্যান্ডলার (শুধুমাত্র ফরোয়ার্ড করা মেসেজের জন্য)
    application.add_handler(MessageHandler(filters.FORWARDED, handle_forwarded_message))

    print(f"🤖 Bot @usarbotinfo_bot is now running as an ID Bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
