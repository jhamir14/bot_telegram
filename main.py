import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURACIÓN DE FLASK (Para Render) ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot de Telegram en funcionamiento 🚀"

def run_flask():
    # Render asigna un puerto automáticamente en la variable de entorno PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- LÓGICA DEL BOT ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot en Render. Envíame un mensaje y te responderé.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # El bot repite lo que el usuario dice
    await update.message.reply_text(f"Me dijiste: {update.message.text}")

if __name__ == '__main__':
    # 1. Iniciar el servidor Flask en un hilo separado
    Thread(target=run_flask).start()

    # 2. Configurar el bot de Telegram
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Manejadores de comandos y mensajes
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    print("Bot iniciado...")
    application.run_polling()