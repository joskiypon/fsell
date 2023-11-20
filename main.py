from telegram.ext import Updater, CommandHandler 
import requests

# Список пользователей с доступом к боту
allowed_users = ['6417262719', '6411071359']
admins = {
    "admin1": 6417262719,
    "admin2": 6411071359
}

# Флаг, указывающий на то, имеет ли пользователь доступ к боту
has_access = False

# Обработчик команды /unlock
def unlock(update, context):
    global has_access
    user_id = str(update.message.from_user.id)
    if user_id in admins.values():
        user_to_grant_access = context.args[0]
        allowed_users.append(user_to_grant_access)
        update.message.reply_text(f"Доступ разрешен для пользователя {user_to_grant_access}")
    else:
        update.message.reply_text("У вас нет прав на разблокировку")

# Обработчик команды /lock
def lock(update, context):
    global has_access
    user_id = str(update.message.from_user.id)
    if user_id in admins.values():
        user_to_revoke_access = context.args[0]
        if user_to_revoke_access in allowed_users:
            allowed_users.remove(user_to_revoke_access)
            update.message.reply_text(f"Доступ запрещен для пользователя {user_to_revoke_access}")
        else:
            update.message.reply_text(f"Пользователь {user_to_revoke_access} не имеет доступа")
    else:
        update.message.reply_text("У вас нет прав на блокировку")

# Обработчик команды /exchange
def вал(update, context):
    global has_access
    user_id = str(update.message.from_user.id)
    if user_id in allowed_users:
        response = requests.get('https://api.exchangeratesapi.io/latest')
        data = response.json()
        exchange_rate = data['rates']['EUR']
        update.message.reply_text(f"Курс USD к EUR: {exchange_rate}")
    else:
        update.message.reply_text("У вас нет доступа")

# Обработчик команды /calc
def калк(update, context):
    global has_access
    user_id = str(update.message.from_user.id)
    if user_id in allowed_users:
        expression = ' '.join(context.args)
        result = eval(expression)
        update.message.reply_text(f"Результат: {result}")
    else:
        update.message.reply_text("У вас нет доступа")

# Токен бота
TOKEN = '6819265079:AAEDpZL7LPZVYZOUfdF6Jv6XaIWSCbApAZc'

# Создание объекта бота
updater = Updater(token=TOKEN, use_context=True)

# Получение диспетчера для регистрации обработчиков
dispatcher = updater.dispatcher

# Регистрация обработчиков команд
dispatcher.add_handler(CommandHandler("unlock", unlock))
dispatcher.add_handler(CommandHandler("lock", lock))
dispatcher.add_handler(CommandHandler("exchange", exchange))
dispatcher.add_handler(CommandHandler("calc", calculator))

# Запуск бота
updater.start_polling()
