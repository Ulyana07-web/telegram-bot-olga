import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

application = Application.builder().token(os.environ.get("TOKEN")).build()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Подписаться на канал", callback_data='subscribe'),
            InlineKeyboardButton("Я уже подписан(-а)", callback_data='subscribed')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я анонимный бот психолога Ольги Ведерниковой. "
                                    "Если вы запутались в проблеме и не готовы раскрывать свою личность, смело пишите свой вопрос в этот чат. "
                                    "Ольга в течении 7 дней выложит анонимизированный кейс с подробным ответом на ваш вопрос в свой телеграмм-канал, "
                                    "поэтому обязательно на него подписывайтесь!", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'subscribe':
        try:
            await query.edit_message_text(text=f"Подпишитесь на канал: https://t.me/kywlyspspysp2 и можете задавать свой вопрос")
        except Exception as e:
            await query.edit_message_text(text=f"Ошибка: {e}")
    elif query.data == 'subscribed':
        await query.edit_message_text(text="Спасибо за подписку! Теперь расскажите о своей проблеме")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text
    # Отправляем сообщение администратору (вам нужно указать ID администратора!)
    admin_id = 457042942
    await context.bot.send_message(chat_id=admin_id, text=f"Запрос от пользователя {user_id}:\n{message_text}") #Отправляем сообщение администратору
    await update.message.reply_text("Ваш запрос отправлен. В течении 7 дней Ольга выложит ответ на ваш вопрос, следите за постами и не забудьте включить уведомления, чтобы ничего не пропустить")


if __name__ == '__main__':  # Исправлено условие
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

    application.add_handler(start_handler)
    application.add_handler(button_handler)
    application.add_handler(message_handler)

    application.run_polling()
