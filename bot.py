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

# Клавиатура для выбора темы
def get_tema_markup():
    markup = types.InlineKeyboardMarkup()
    topics = [
        ("ПР 1", "tema_1"),
        ("Тема 2", "tema_2"),
        ("Тема 3. Интернет", "tema_3"),
        ("Тема 4. Защита информации", "tema_4"),
        ("Тема 5. Текстовый процессор", "tema_5"),
        ("Тема 6. Компьютерная графика", "tema_6")
    ]
    for text, callback in topics:
        markup.add(types.InlineKeyboardButton(text, callback_data=callback))
    return markup

# === ОБРАБОТЧИКИ TELEGRAM ===
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        user_text = message.text  # Без .lower() для корректной работы с русским текстом

        if user_text == 'Скачать учебник':
            bot.send_message(
                message.chat.id,
                "Скачай учебник по ссылке: https://drive.google.com/drive/folders/1xtdAFfIx6cx53-kR5yBHthxasW5M3h7g?usp=drive_link"
            )
            return  # Важно добавить return после отправки сообщения

        elif user_text == 'Практические занятия':
            bot.send_message(
                message.chat.id,
                "Выберите номер ПР:",
                reply_markup=get_pr_markup()
            )
            return

        elif user_text == 'Итоговый тест':
            bot.send_message(
                message.chat.id,
                "Пройди тест по ссылке: https://docs.google.com/forms/d/e/1FAIpQLSe0_EXyRZjFMBH3tMmrzoVPltpmNXgRnsSczDkFhjT5dIlbxg/viewform?usp=sf_link"
            )
            return

        elif user_text == 'Пройти тесты':
            bot.send_message(
                message.chat.id,
                "Данный раздел в разработке. Скоро все появится!",
                reply_markup=main_markup
            )
            return

        else:
            bot.send_message(
                message.chat.id,
                "Не понял ваш запрос. Воспользуйтесь клавиатурой ниже.",
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

# === ОБРАБОТЧИКИ CALLBACK ===
@bot.callback_query_handler(func=lambda call: call.data.startswith('dz_'))
def handle_dz_callback(call):
    dz_number = call.data[3:]
    assignments = {
        '1': (
            "ДЗ 1: Системы счисления\n"
            "Задание: Реши самостоятельную в тетради, а результат покажи учителю.\n"
            "Вариант узнай у меня\n"
            "Ссылка на материалы: https://disk.yandex.ru/d/APQE4mDwBTSbkA"
        ),
        '2': (
            "ДЗ 2: Алгебра логики\n"
            "Задание: Реши самостоятельно по учебнику, а решение покажи учителю:\n"
            "с. 3 Вариант 4, Задача №1,2\n"
            "с. 4 Вариант 3, Задача №1\n"
            "с.11 Вариант 4, Задача 2.\n"
            "Ссылка на материалы: https://disk.yandex.ru/d/BPjzUvFeiSOvVw"
        ),
        '3': (
            "ДЗ 3: Интернет\n"
            "Задание: Для этого задания используй MS Visio или Draw.io\n"
            "Результат выполнения отправь преподавателю на почту polinavladimirovn@yandex.ru\n"
            "Ссылка на материалы: https://disk.yandex.ru/d/w_85PUK6rneizQ"
        ),
        '4': (
            "ДЗ 4: Защита информации\n"
            "Задание: Для этого задания используй MS Word\n"
            "Результат выполнения отправь преподавателю на почту polinavladimirovn@yandex.ru\n"
            "Ссылка на материалы: https://disk.yandex.ru/d/JycaZ67-mUxadQ"
        ),
        '5': (
            "ДЗ 5: Текстовый процессор\n"
            "Задание: Для этого задания используй MS Word\n"
            "с. 31 Практическая работа №9\n"
            "с. 37 Практическая работа №10\n"
            "с. 41 Практическая работа №11\n"
            "с. 46 Практическая работа №12\n"
            "Результат выполнения отправь преподавателю на почту polinavladimirovn@yandex.ru\n"
            "Ссылка на материалы: https://disk.yandex.ru/d/aiykc237nTqJBg"
        ),
        '6': (
            "ДЗ 6: Компьютерная графика\n"
            "Задание: Для этого задания используй MS Publisher или LO Impress\n"
            "Результат выполнения отправь преподавателю на почту polinavladimirovn@yandex.ru\n"
            "Ссылка на материалы: https://disk.yandex.ru/d/qKQ3ZFQHg59wGQ"
        )
    }

    if dz_number in assignments:
        bot.send_message(
            call.message.chat.id,
            assignments[dz_number]
        )
    else:
        bot.send_message(call.message.chat.id, "ДЗ не найдено. Обратитесь к преподавателю.")

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('tema_'))
def handle_tema_callback(call):
    tema_number = call.data[5:]
    topics = {
        '1': "Системы счисления",
        '2': "Алгебра логики",
        '3': "Интернет",
        '4': "Защита информации",
        '5': "Текстовый процессор",
        '6': "Компьютерная графика"
    }

    if tema_number in topics:
        link = f"https://disk.yandex.ru/d/{['APQE4mDwBTSbkA', 'BPjzUvFeiSOvVw', 'w_85PUK6rneizQ', 'JycaZ67-mUxadQ', 'aiykc237nTqJBg', 'qKQ3ZFQHg59wGQ'][int(tema_number)-1]}"
        bot.send_message(
            call.message.chat.id,
            f"Тема {tema_number}: {topics[tema_number]}. Задание: Напиши конспект Лекции по ссылке в тетрадь. Не забудь про ДЗ! {link}"
        )
    else:
        bot.send_message(call.message.chat.id, "Тема не найдена.")

    bot.answer_callback_query(call.id)

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
