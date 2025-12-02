
# Импортируем необходимые библиотеки
try:
    from dotenv import load_dotenv # type: ignore
except ImportError:
    print("Библиотека python-dotenv не установлена. Установите её командой: pip install python-dotenv")
    exit(1)

import os
import telebot
from telebot import types

# Загружаем переменные из .env файла
load_dotenv()

# Получаем токен из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверяем наличие токена
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Токен бота не найден в .env файле!")

# Создаем экземпляр бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Основная клавиатура
markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
markup.add(
    types.KeyboardButton('👋 Привет'),
    types.KeyboardButton('📓 Я пропустил занятие:('),
    types.KeyboardButton('📚 Сдать ДЗ'), 
    types.KeyboardButton('🎲 Какой у меня вариант?')
)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Ты что-то пропустил?", reply_markup=markup)

# ══════════════════════════════════════════════════
# ║  ОСНОВНОЙ ОБРАБОТЧИК - обрабатывает ВСЕ сообщения  ║
# ╚═════════════════════════════════════════════════
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text.lower()
    
    # Обработка основных кнопок
    if user_text == '👋 привет' or 'привет' in user_text:
        bot.send_message(message.chat.id, "И тебе привет! 😊")
    
    elif user_text == '📓 я пропустил занятие:(':
        show_tema_subjects(message)
    
    elif user_text == '📚 сдать дз' in user_text:
        show_dz_subjects(message)
    
    elif user_text == '🎲 какой у меня вариант?':
        import random
        bot.send_message(message.chat.id, f"Ваше число: {random.randint(1, 10)}")

# ══════════════════════════════════════════════════
# ║  ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ (не обработчики!)       ║
# ╚═════════════════════════════════════════════════
def show_dz_subjects(message):
    """Функция показывает кнопки выбора ДЗ"""
    markup_dz = types.InlineKeyboardMarkup(row_width=6)
    
    btn_1 = types.InlineKeyboardButton("ДЗ 1", callback_data='dz_1')
    btn_2 = types.InlineKeyboardButton("ДЗ 2", callback_data='dz_2')
    btn_3 = types.InlineKeyboardButton("ДЗ 3", callback_data='dz_3')
    btn_4 = types.InlineKeyboardButton("ДЗ 4", callback_data='dz_4')  # Исправлено: было dz_1
    btn_5 = types.InlineKeyboardButton("ДЗ 5", callback_data='dz_5')
    btn_6 = types.InlineKeyboardButton("ДЗ 6", callback_data='dz_6')
    
    markup_dz.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6)
    bot.send_message(message.chat.id, "Выберите номер ДЗ:", reply_markup=markup_dz)


def show_tema_subjects(message):
    markup_tema = types.InlineKeyboardMarkup()  # row_width можно не указывать

    
    btn_1 = types.InlineKeyboardButton("Системы счисления", callback_data='tema_1')
    btn_2 = types.InlineKeyboardButton("Алгебра логики", callback_data='tema_2')
    btn_3 = types.InlineKeyboardButton("Интернет", callback_data='tema_3')
    btn_4 = types.InlineKeyboardButton("Защита информации", callback_data='tema_4')
    btn_5 = types.InlineKeyboardButton("Текстовый процессор", callback_data='tema_5')
    btn_6 = types.InlineKeyboardButton("Компьютерная графика", callback_data='tema_6')
    
    # Добавляем каждую кнопку ОТДЕЛЬНО — по одной в строке
    markup_tema.add(btn_1)
    markup_tema.add(btn_2)
    markup_tema.add(btn_3)
    markup_tema.add(btn_4)
    markup_tema.add(btn_5)
    markup_tema.add(btn_6)
    
    bot.send_message(message.chat.id, "Выберите пропущенную тему:", reply_markup=markup_tema)

# ══════════════════════════════════════════════════
# ║  ОБРАБОТЧИК INLINE-КНОПОК (отдельный!)          ║
# ╚═════════════════════════════════════════════════

@bot.callback_query_handler(func=lambda call: call.data.startswith('dz_'))
def handle_dz_callback(call):
    # Словарь с заданиями для каждого ДЗ
    ASSIGNMENTS = {
        '1': (
            "ДЗ 1: Системы счисления\n"
            "Задание: Реши самостоятельную в тетради, а результат покажи учителю.\n"
            "Вариант узнай у меня\n"
            "Ссылка на материалы: https://disk.yandex.ru/d/APQE4mDwBTSbkA\n"
        ),
        '2': (
            "ДЗ 2: Алгебра логики\n"
            "Задание: Реши самостоятельно по учебнику, а решение покажи учителю:\n"
            "с. 3 Вариант 4, Задача №1,2\n"
            "с. 4 Вариант 3, Задача №1\n"
            "с.11 Вариант 4, Задача 2.\n"
            "Ссылка на материалы: https://disk.yandex.ru/d/BPjzUvFeiSOvVw\n"
        ),
        '3': ( "ДЗ 3: Интернет\n"
            "Задание: Для этого задания используй MS Visio или Draw.io\n"
            "Результат выполнения отправь преподавателю на почту polinavladimirovn@yandex.ru \n"
            "Ссылка на материалы: https://disk.yandex.ru/d/w_85PUK6rneizQ\n"
         ),
        '4': ( "ДЗ 4: Защита информации.\n "
        "Задание: Для этого задания используй MS Word\n"
        "Результат выполнения отправь преподавателю на почту polinavladimirovn@yandex.ru \n"
        "Ссылка на материалы: https://disk.yandex.ru/d/JycaZ67-mUxadQ\n"
        ),
        '5': ( "ДЗ 5: Текстовый процессор \n"
        "Задание: Для этого задания используй MS Word\n"
        "с. 31 Практическая работа №9\n"
        "с. 37 Практическая работа №10\n"
        "с. 41 Практическая работа №11\n"
        "с. 46 Практическая работа №12\n"
        "Результат выполнения отправь преподавателю на почту polinavladimirovn@yandex.ru \n"
        "Ссылка на материалы: https://disk.yandex.ru/d/aiykc237nTqJBg\n"
        ),
        '6': ( "ДЗ 6: Компьютерная графика \n"
        "Задание: Для этого задания используй MS Publisher или LO Impress\n"
        "Результат выполнения отправь преподавателю на почту polinavladimirovn@yandex.ru \n"
        "Ссылка на материалы: https://disk.yandex.ru/d/qKQ3ZFQHg59wGQ\n" )
    }
    
    dz_number = call.data[3:]  # Извлекаем номер ДЗ (после 'dz_')
    
    
    # Проверяем, есть ли ДЗ в словаре
    if dz_number in ASSIGNMENTS:
        bot.send_message(
            call.message.chat.id,
            ASSIGNMENTS[dz_number],
            parse_mode='Markdown'  # если нужно форматирование
        )
    else:
        bot.send_message(
            call.message.chat.id,
            "ДЗ не найдено. Обратитесь к преподавателю."
        )
    
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('tema_'))
def handle_tema_callback(call):
    tema_number = call.data[5:]
    
    # Вызываем функцию по номеру темы
    if tema_number == '1':
        send_theme_1(call.message.chat.id)
    elif tema_number == '2':
        send_theme_2(call.message.chat.id)
    elif tema_number == '3':
        send_theme_3(call.message.chat.id)
    elif tema_number == '4':
        send_theme_4(call.message.chat.id)
    elif tema_number == '5':
        send_theme_5(call.message.chat.id)
    elif tema_number == '6':
        send_theme_6(call.message.chat.id)
   
    else:
        bot.send_message(call.message.chat.id, "Тема не найдена.")
    
    bot.answer_callback_query(call.id)

def send_theme_1(chat_id):
    bot.send_message(chat_id, "Тема 1: Системы счисления. Задание: Напиши конспект Лекции по ссылке в тетрадь. Не забудь про ДЗ! https://disk.yandex.ru/d/APQE4mDwBTSbkA")

def send_theme_2(chat_id):
    bot.send_message(chat_id, "Тема 2: Алгебра логики. Задание: Напиши конспект Лекции по ссылке в тетрадь. Не забудь про ДЗ! https://disk.yandex.ru/d/BPjzUvFeiSOvVw")

def send_theme_3(chat_id):
    bot.send_message(chat_id, "Тема 3: Интернет. Задание: Напиши конспект Лекции по ссылке в тетрадь. Не забудь про ДЗ! https://disk.yandex.ru/d/w_85PUK6rneizQ")

def send_theme_4(chat_id):
    bot.send_message(chat_id, "Тема 4: Защита информации. Задание: Напиши конспект Лекции по ссылке в тетрадь. Не забудь про ДЗ! https://disk.yandex.ru/d/JycaZ67-mUxadQ")

def send_theme_5(chat_id):
    bot.send_message(chat_id, "Тема 5: Текстовый процессор. Задание: Напиши конспект Лекции по ссылке в тетрадь. Не забудь про ДЗ! https://disk.yandex.ru/d/aiykc237nTqJBg")

def send_theme_6(chat_id):
    bot.send_message(chat_id, "Тема 6: Компьютерная графика. Задание: Напиши конспект Лекции по ссылке в тетрадь. Не забудь про ДЗ! https://disk.yandex.ru/d/qKQ3ZFQHg59wGQ")



bot.polling()