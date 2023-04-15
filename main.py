import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ChatPermissions
import datetime
import threading

def reset_counters(context, user_id):
    context.user_data[user_id]["text_count"] = 0
    context.user_data[user_id]["sticker_count"] = 0

def handle_message(update, context):
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id

    # Проверяем, является ли сообщение ответом на сообщение другого пользователя
    if message.reply_to_message and message.reply_to_message.from_user.id != user_id:
        context.user_data[user_id]["text_count"] = 0
        context.user_data[user_id]["sticker_count"] = 0

    # Проверяем, является ли сообщение текстом или стикером
    if message.text:
        context.user_data.setdefault(user_id, {"text_count": 0, "sticker_count": 0})
        context.user_data[user_id]["text_count"] += 1
    elif message.sticker:
        context.user_data.setdefault(user_id, {"text_count": 0, "sticker_count": 0})
        context.user_data[user_id]["sticker_count"] += 1

    # Проверяем, превышает ли количество текстовых сообщений или стикеров
    if context.user_data[user_id]["text_count"] > 8 or context.user_data[user_id]["sticker_count"] > 8:
        # Запрещаем пользователю печатать сообщения на 10 минут
        until_date = message.date + datetime.timedelta(seconds=600)
        permissions = ChatPermissions()
        permissions.can_send_messages = False
        context.bot.restrict_chat_member(chat_id, user_id, until_date=until_date, permissions=telegram.ChatPermissions())

        # Отправляем сообщение о блокировке
        context.bot.send_message(chat_id=chat_id,
                                 text=f"Пользователь {message.from_user.first_name} заблокирован на 10 минут.")

        # Сбрасываем счетчики сообщений
        context.user_data[user_id]["text_count"] = 0
        context.user_data[user_id]["sticker_count"] = 0

    # Создаем таймер, чтобы счетчики обнулялись каждые 12 секунд
    timer = threading.Timer(12.0, reset_counters, [context, user_id])
    timer.start()

updater = Updater(token="5856175367:AAEjtX5_wjkt8NhuwBnUhBediloa14X5U6A", use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.all, handle_message))

updater.start_polling()
updater.idle()


