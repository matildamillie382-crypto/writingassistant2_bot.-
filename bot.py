import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

# Retrieve environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    print("Error: Missing environment variables.")
    sys.exit(1)

# Initialize OpenAI client
ai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I am your AI Writing Assistant.\n\n"
        "Send me any text, draft, or prompt, and I will help you expand, rewrite, or polish it!"
    )

# Text message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Send a placeholder typing action to look natural
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Call the OpenAI API
        response = await ai_client.chat.completions.create(
            model="gpt-4o-mini", # Cost-effective and fast for a writing bot
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert AI Writing Assistant. Your job is to help users improve their grammar, vocabulary, tone, and structure. Provide polished text or constructive writing suggestions based on what they send."
                },
                {"role": "user", "content": user_text}
            ]
        )
        
        ai_reply = response.choices[0].message.content
        await update.message.reply_text(ai_reply)

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        await update.message.reply_text("⚠️ Sorry, I encountered an error processing your request.")

if __name__ == "__main__":
    # Build and start the Telegram bot application using polling
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling()
