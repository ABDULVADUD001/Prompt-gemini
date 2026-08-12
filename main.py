import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Token va kalitlarni muhit o'zgaruvchilaridan (Environment Variables) olamiz
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

API_URL = (
    "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
)
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_prompt = update.message.text
  await update.message.reply_text(
      "🎨 Rasm yaratilmoqda, iltimos kuting (taxminan 10-20 soniya)..."
  )

  response = requests.post(
      API_URL, headers=headers, json={"inputs": user_prompt}
  )

  if response.status_code == 200:
    image_bytes = response.content
    await update.message.reply_photo(
        photo=image_bytes, caption=f"✨ So'rov: {user_prompt}"
    )
  else:
    await update.message.reply_text(
        "❌ Xatolik yuz berdi. API kalitingiz to'g'riligini yoki model"
        " yuklanayotganini tekshiring."
    )


def main():
  app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
  app.add_handler(
      MessageHandler(filters.TEXT & (~filters.COMMAND), generate_image)
  )
  print("Bot ishga tushdi...")
  app.run_polling()


if __name__ == "__main__":
  main()
  
