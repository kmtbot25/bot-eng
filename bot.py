# Telegram-бот «Отработочка» для студентов
import os
import telebot
from telebot import types
import random
from flask import Flask, request

# === FLASK APP FOR RENDER ===
app = Flask(__name__)

# === НАСТРОЙКИ И ИНИЦИАЛИЗАЦИЯ ===
# Токен берётся из переменных окружения Render
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "Токен бота не задан! Установите переменную окружения TELEGRAM_BOT_TOKEN в настройках Render."
    )

# Создаём экземпляр бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# === КЛАВИАТУРЫ ===
# Основная клавиатура
main_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_markup.add(
    types.KeyboardButton('Скачать учебник'),
    types.KeyboardButton('Практические занятия'),
    types.KeyboardButton('Итоговый тест'),
    types.KeyboardButton('Пройти тесты')
)

# Клавиатура для выбора практических работ (ПР 1-6)
def get_pr_markup():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('ПР 1'),
        types.KeyboardButton('ПР 2'),
        types.KeyboardButton('ПР 3'),
        types.KeyboardButton('ПР 4'),
        types.KeyboardButton('ПР 5'),
        types.KeyboardButton('ПР 6')
    )
    return markup

# === ОБРАБОТЧИКИ TELEGRAM ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для помощи с занятиями. Выберите опцию:",
        reply_markup=main_markup
    )

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        user_text = message.text

        # Обработка кнопки "Скачать учебник"
        if user_text == 'Скачать учебник':
            bot.send_message(
                message.chat.id,
                "Скачай учебник по ссылке: https://drive.google.com/drive/folders/1xtdAFfIx6cx53-kR5yBHthxasW5M3h7g?usp=drive_link",
                reply_markup=main_markup
            )

        # Обработка кнопки "Практические занятия"
        elif user_text == 'Практические занятия':
            bot.send_message(
                message.chat.id,
                "Выберите номер практической работы (ПР):",
                reply_markup=get_pr_markup()  # Показываем клавиатуру с ПР 1-6
            )

        # Обработка кнопки "Итоговый тест"
        elif user_text == 'Итоговый тест':
            bot.send_message(
                message.chat.id,
                "Пройди тест по ссылке: https://docs.google.com/forms/d/e/1FAIpQLSe0_EXyRZjFMBH3tMmrzoVPltpmNXgRnsSczDkFhjT5dIlbxg/viewform?usp=sf_link",
                reply_markup=main_markup
            )

        # Обработка кнопки "Пройти тесты"
        elif user_text == 'Пройти тесты':
            bot.send_message(
                message.chat.id,
                "В разработке. Скоро все появится",
                reply_markup=main_markup
            )

        # Обработка кнопок с практическими работами (ПР 1-6)
        elif user_text.startswith('ПР '):
            pr_number = user_text.split()[1]  # Получаем номер ПР (1, 2, 3, 4, 5, 6)
            
            # Информация о каждой практической работе
            pr_info = {
                '1': "ПР 1: Системы счисления\n\nЗадание: Реши самостоятельную работу в тетради\nРезультат покажи учителю\n\nМатериалы: https://disk.yandex.ru/d/APQE4mDwBTSbkA",
                '2': "ПР 2: Алгебра логики\n\nЗадание:\n• с.3 Вариант 4, Задачи №1,2\n• с.4 Вариант 3, Задача №1\n• с.11 Вариант 4, Задача №2\n\nРезультат покажи учителю\n\nМатериалы: https://disk.yandex.ru/d/BPjzUvFeiSOvVw",
                '3': "ПР 3: Интернет\n\nЗадание: Используй MS Visio или Draw.io\n\nРезультат отправь на почту: polinavladimirovn@yandex.ru\n\nМатериалы: https://disk.yandex.ru/d/w_85PUK6rneizQ",
                '4': "ПР 4: Защита информации\n\nЗадание: Используй MS Word\n\nРезультат отправь на почту: polinavladimirovn@yandex.ru\n\nМатериалы: https://disk.yandex.ru/d/JycaZ67-mUxadQ",
                '5': "ПР 5: Текстовый процессор\n\nЗадания из учебника:\n• с.31 Практическая работа №9\n• с.37 Практическая работа №10\n• с.41 Практическая работа №11\n• с.46 Практическая работа №12\n\nРезультат отправь на почту: polinavladimirovn@yandex.ru\n\nМатериалы: https://disk.yandex.ru/d/aiykc237nTqJBg",
                '6': "ПР 6: Компьютерная графика\n\nЗадание: Используй MS Publisher или LibreOffice Impress\n\nРезультат отправь на почту: polinavladimirovn@yandex.ru\n\nМатериалы: https://disk.yandex.ru/d/qKQ3ZFQHg59wGQ"
            }
            
            if pr_number in pr_info:
                bot.send_message(
                    message.chat.id,
                    pr_info[pr_number],
                    reply_markup=get_pr_markup()  # Остаемся в меню ПР
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "ПР не найдена. Выберите ПР от 1 до 6.",
                    reply_markup=get_pr_markup()
                )

        # Обработка кнопки "Назад в меню"
        elif user_text == '↩️ Назад в меню':
            bot.send_message(
                message.chat.id,
                "Вы вернулись в главное меню:",
                reply_markup=main_markup
            )

        else:
            bot.send_message(
                message.chat.id,
                "Не понял ваш запрос. Воспользуйтесь клавиатурой ниже.",
                reply_markup=main_markup
            )

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте ещё раз.")
        print(f"[ERROR] {e}")

# === WEBHOOK FOR TELEGRAM (OPTIONAL) ===
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

# === HEALTH CHECK FOR RENDER ===
@app.route('/')
def health_check():
    return 'Bot is running!', 200

# === MAIN ENTRY POINT ===
if __name__ == '__main__':
    # Choose ONE approach: Polling OR Webhook, not both
    
    # APPROACH 1: Use Polling (simpler)
    print("Бот запущен. Ожидание сообщений...")
    port = int(os.environ.get('PORT', 10000))
    
    # Start Flask in a separate thread for health checks
    import threading
    def start_flask():
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start bot polling
    bot.remove_webhook()
    bot.infinity_polling(timeout=60)
    
    # APPROACH 2: Use Webhook (uncomment below and comment the polling approach above)
    # port = int(os.environ.get('PORT', 8000))
    # bot.remove_webhook()
    # bot.set_webhook(url=f"https://your-render-app.onrender.com/webhook")
    # app.run(host='0.0.0.0', port=port, debug=False)
