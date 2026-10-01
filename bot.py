from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import os
TOKEN = os.getenv("BOT_TOKEN")

NOMBRE = "ANGELO MARTIN FLORES QUISPE"
MENSAJE_REGISTRO = "📌 ¡Todo listo! Ya estás registrado y recibirás las notificaciones de asistencia de tus hijos."

# Personas que hicieron /start
usuarios = set()

# Zona horaria de Perú
ZONA = ZoneInfo("America/Lima")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios.add(update.effective_chat.id)
    await update.message.reply_text(MENSAJE_REGISTRO)


async def cualquier_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENSAJE_REGISTRO)


async def enviar_entrada():
    ahora = datetime.now(ZONA)
    fecha = ahora.strftime("%d/%m/%Y")

    mensaje = (
        f"✅ Entrada registrada a tiempo\n"
        f"👤 {NOMBRE}\n"
        f"⏰ {fecha} 07:51 — A tiempo"
    )

    for chat_id in list(usuarios):
        try:
            await app.bot.send_message(chat_id=chat_id, text=mensaje)
        except Exception as e:
            print(f"Error enviando a {chat_id}: {e}")


async def enviar_salida():
    ahora = datetime.now(ZONA)
    fecha = ahora.strftime("%d/%m/%Y")

    mensaje = (
        f"🚪 Salida registrada\n"
        f"👤 {NOMBRE}\n"
        f"⏰ {fecha} 15:39"
    )

    for chat_id in list(usuarios):
        try:
            await app.bot.send_message(chat_id=chat_id, text=mensaje)
        except Exception as e:
            print(f"Error enviando a {chat_id}: {e}")


async def programador():
    ultima_entrada = None
    ultima_salida = None

    while True:
        ahora = datetime.now(ZONA)
        fecha = ahora.date()

        # 10:00 a. m.
        if ahora.hour == 10 and ahora.minute == 0 and ultima_entrada != fecha:
            await enviar_entrada()
            ultima_entrada = fecha

        # 3:42 p. m.
        if ahora.hour == 15 and ahora.minute == 42 and ultima_salida != fecha:
            await enviar_salida()
            ultima_salida = fecha

        await asyncio.sleep(10)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cualquier_mensaje))


async def iniciar():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("🤖 Bot funcionando correctamente...")

    asyncio.create_task(programador())

    # Mantener el bot funcionando
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(iniciar())
