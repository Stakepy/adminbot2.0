import telegram
from telegram.ext import Updater, MessageHandler, Filters
import time

def handle_message(update, context):
    message = update.message
    user_id = message.from_user.id
    chat_id = message.chat_id
    if message.text.lower() == context.user_data.get(user_id, {}).get('last_message', None):
        if context.user_data.get(user_id, {}).get('count', 0) >= 4: # Если пользователь отправил одно и тоже сообщение более 5 раз подряд
            permissions = telegram.ChatPermissions(send_messages=False)
            context.bot.restrict_chat_member(chat_id, user_id, permissions=permissions, until_date=time.time() + 300) # Ограничить отправку сообщений на 5 минут (300 секунд)
            context.bot.send_message(chat_id=chat_id, text='Вы были заблокированы на 5 минут за спам')
            context.user_data[user_id]['count'] = 0 # Обнулить счетчик сообщений
        else:
            context.user_data[user_id]['count'] += 1 # Увеличить счетчик сообщений
    else:
        context.user_data[user_id] = {'last_message': message.text.lower(), 'count': 1} # Новое сообщение - сбросить счетчик

updater = Updater(token='5856175367:AAEkhw1xhW_CldHfOzZoMvwM5-0Au_mLmxM', use_context=True)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
updater.dispatcher.add_handler(message_handler)
updater.start_polling()
updater.idle()
