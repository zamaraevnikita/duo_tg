<<<<<<< HEAD
# 6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w
import telebot
from telebot import types
import psutil
import subprocess

TOKEN = '6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояний пользователя
user_state = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_state[message.chat.id] = 'start'
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row('Начало', 'ТП', 'Как', 'Я')
    bot.send_message(message.from_user.id, "Привет! Я бот для изучения языков программирования. Выбери раздел:", reply_markup=user_markup)

# Обработчик для кнопок "Начало", "ТП", "Как", "Я"
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'Начало':
        choose_language(message)
    elif message.text == 'Как':
        show_instructions(message)
    elif message.text == 'ТП' or message.text == 'Я':
        bot.send_message(message.chat.id, "Функционал этой кнопки еще не реализован.")
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")


def show_instructions(message):
    user_state[message.chat.id] = 'show_instructions'
    instructions_text = "Для использования бота, следуйте этим шагам:\n\n1. Выберите раздел 'Начало', 'ТП', 'Как', 'Я'.\n2. Следуйте инструкциям, выбирая язык программирования и действия.\n3. Введите свой код, используя кнопку 'Ввести код'.\n4. После ввода кода, выберите 'Показать ответ' для проверки.\n5. Выберите 'Далее' для перехода к следующему уроку.\n6. В любой момент можно вернуться назад, используя кнопку 'Назад'."
    bot.send_message(message.chat.id, instructions_text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_back)


# Функция для выбора языка программирования
def choose_language(message):
    user_state[message.chat.id] = 'choose_language'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Python', 'C++', 'Назад')
    bot.send_message(message.chat.id, "Выбери язык программирования:", reply_markup=markup)
    bot.register_next_step_handler(message, choose_option)

# Функция для выбора опции после выбора языка
def choose_option(message):
    if message.text == 'Python' or message.text == 'C++':
        user_state[message.chat.id] = 'choose_option'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Начать', 'Выбор урока', 'Назад')
        bot.send_message(message.chat.id, "Отлично! Теперь выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_option)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Обработчик для кнопок "Начать" и "Выбор урока"
def handle_option(message):
    if message.text == 'Начать':
        user_state[message.chat.id] = 'handle_option'
        bot.send_photo(message.chat.id, open('your_image.jpg', 'rb'))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Ввести код', 'Дальше', 'Назад')
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_action)
    elif message.text == 'Выбор урока':
        show_lessons(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Обработчик для кнопок "Показать ответ" и "Дальше"
def handle_action(message):
    if message.text == 'Ввести код':
        user_state[message.chat.id] = 'handle_action'
        bot.send_message(message.chat.id, "Пожалуйста, введите свой код:")
        bot.register_next_step_handler(message, handle_user_code)
    elif message.text == 'Дальше':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        # Добавьте ваш код для перехода к следующему уроку
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Функция для показа уроков
def show_lessons(message):
    user_state[message.chat.id] = 'show_lessons'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Добавьте кнопки для каждого урока
    markup.row('Урок 1', 'Урок 2', 'Урок 3', 'Назад')
    bot.send_message(message.chat.id, "Выбери урок:", reply_markup=markup)

# Обработчик для выбора урока
@bot.message_handler(func=lambda message: True)
def handle_lesson(message):
    if message.text.startswith('Урок'):
        bot.send_message(message.chat.id, f"Вы выбрали урок {message.text}.")
        # Добавьте ваш код для работы с выбранным уроком
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Обработчик для кнопки "Дальше" после показа ответа
def handle_next(message):
    bot.send_message(message.chat.id, "Переход к следующему уроку.")
    # Добавьте ваш код для перехода к следующему уроку

# Обработчик для кнопки "Назад"
def handle_back(message):
    if message.chat.id in user_state:
        current_state = user_state[message.chat.id]
        # Remove the current state from user_state to avoid recursive loop
        user_state.pop(message.chat.id, None)

        if current_state == 'choose_language':
            handle_start(message)
        elif current_state == 'choose_option':
            choose_language(message)
        elif current_state == 'handle_option':
            choose_option(message)
        elif current_state == 'handle_action':
            handle_option(message)
        elif current_state == 'show_lessons':
            choose_option(message)
        elif current_state == 'handle_lesson':
            show_lessons(message)
        elif current_state == 'handle_next':
            handle_action(message)
        else:
            handle_start(message)
    else:
        handle_start(message)

# Обработчик для ввода кода пользователем
def handle_user_code(message):
   
    user_code = message.text

    try:
        # Установка ограничения времени выполнения и объема памяти
        process = subprocess.run(['python', '-c', user_code], capture_output=True, text=True, timeout=5)
        if process.returncode != 0:
            raise Exception(f"Произошла ошибка при выполнении кода. Код завершился с кодом возврата {process.returncode}.")

        # Проверка результата выполнения кода
        expected_output = "Hello, World!"
        if expected_output in process.stdout:
            bot.send_message(message.chat.id, "Код выполнен верно!")
            show_answer(message)
        else:
            bot.send_message(message.chat.id, "Код выполнен, но результат не соответствует ожидаемому.")
            show_buttons(message)
    except subprocess.TimeoutExpired:
        bot.send_message(message.chat.id, "Превышено ограничение времени выполнения кода.")
        show_buttons(message)
    except Exception as e:
        # Если произошла ошибка при выполнении кода, сообщаем об этом пользователю
        bot.send_message(message.chat.id, f"Произошла ошибка при выполнении кода:\n{str(e)}")
        show_buttons(message)

# Функция для показа кнопок "Показать ответ" и "Назад"
def show_buttons(message):
    user_state[message.chat.id] = 'show_buttons'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Показать ответ', 'Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_buttons_after_code)

# Обработчик для кнопок "Показать ответ" и "Назад" после ввода кода
def handle_buttons_after_code(message):
    if message.text == 'Показать ответ':
        show_answer(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Функция для показа ответа (изображения)
def show_answer(message):
    user_state[message.chat.id] = 'show_answer'
    bot.send_photo(message.chat.id, open('your_answer_image.jpg', 'rb'))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Далее', 'Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_buttons_after_answer)
  
# Обработчик для кнопок "Далее" и "Назад" после показа ответа
def handle_buttons_after_answer(message):
    if message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        # Добавьте ваш код для перехода к следующему уроку
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

if __name__ == '__main__':
    bot.polling(none_stop=True)

=======
# import telebot
# import random
# from telebot import types
# # Загружаем список интересных фактов
# f = open('data/facts.txt', 'r', encoding='UTF-8')
# facts = f.read().split('\n')
# f.close()
# # Загружаем список поговорок
# f = open('data/thinks.txt', 'r', encoding='UTF-8')
# thinks  = f.read().split('\n')
# f.close()
# # Создаем бота
# bot = telebot.TeleBot('6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w')
# # Команда start
# @bot.message_handler(commands=["start"])
# def start(m, res=False):
#         # Добавляем две кнопки
#         markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
#         item1=types.KeyboardButton("Факт")
#         item2=types.KeyboardButton("Поговорка")
#         markup.add(item1)
#         markup.add(item2)
#         bot.send_message(m.chat.id, 'Нажми: \nФакт для получения интересного факта\nПоговорка — для получения мудрой цитаты ',  reply_markup=markup)
# # Получение сообщений от юзера
# @bot.message_handler(content_types=["text"])
# def handle_text(message):
#     # Если юзер прислал 1, выдаем ему случайный факт
#     if message.text.strip() == 'Факт' :
#             answer = random.choice(facts)
#     # Если юзер прислал 2, выдаем умную мысль
#     elif message.text.strip() == 'Поговорка':
#             answer = random.choice(thinks)
#     # Отсылаем юзеру сообщение в его чат
#     bot.send_message(message.chat.id, answer)
# # Запускаем бота
# bot.polling(none_stop=True, interval=0)



# import telebot
# import os

# bot = telebot.TeleBot('6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w')

# def get_lessons(language):
#     lessons = []
#     directory = f'data/{language}'
#     lessons = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.startswith('lesson')]
#     return lessons

# @bot.message_handler(commands=['start'])
# def start(message):
#     user = message.from_user
#     bot.send_message(message.chat.id, f"Привет, {user.first_name}! Я бот для изучения языков программирования.")
#     keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.row('Python', 'JavaScript')
#     keyboard.row('Java', 'C++')
#     bot.send_message(message.chat.id, 'Выберите язык программирования:', reply_markup=keyboard)

# @bot.message_handler(func=lambda message: message.text in ['Python', 'JavaScript', 'Java', 'C++'])
# def handle_lessons(message):
#     lessons = get_lessons(message.text)
#     keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#     for lesson in lessons:
#         keyboard.add(telebot.types.KeyboardButton(lesson))
#     bot.send_message(message.chat.id, f'Доступные уроки по {message.text}:', reply_markup=keyboard)

# bot.polling(none_stop=True, interval=0)




# import telebot
# import os

# bot = telebot.TeleBot('6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w')

# def get_lessons():
#     directory = 'data/python'
#     lessons = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.startswith('lesson')]
#     return lessons

# @bot.message_handler(commands=['start'])
# def start(message):
#     user = message.from_user
#     bot.send_message(message.chat.id, f"Привет, {user.first_name}! Я бот для изучения языков программирования.")
#     keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#     lessons = get_lessons()
#     for lesson in lessons:
#         keyboard.row(lesson)
#     bot.send_message(message.chat.id, 'Выберите урок:', reply_markup=keyboard)

# bot.polling()

# import telebot
# from telebot import types

# TOKEN = '6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w'
# bot = telebot.TeleBot(TOKEN)

# # Обработчик команды /start
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     user_markup.row('Начало', 'ТП', 'Как', 'Я')
#     bot.send_message(message.from_user.id, "Привет! Я бот для изучения языков программирования. Выбери раздел:", reply_markup=user_markup)

# # Обработчик для кнопок "Начало", "ТП", "Как", "Я"
# @bot.message_handler(func=lambda message: True)
# def handle_buttons(message):
#     if message.text == 'Начало':
#         choose_language(message)
#     elif message.text == 'ТП' or message.text == 'Как' or message.text == 'Я':
#         bot.send_message(message.chat.id, "Функционал этой кнопки еще не реализован.")
#     else:
#         bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# # Функция для выбора языка программирования
# def choose_language(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     markup.row('Python', 'C++')
#     bot.send_message(message.chat.id, "Выбери язык программирования:", reply_markup=markup)
#     bot.register_next_step_handler(message, choose_option)

# # Функция для выбора опции после выбора языка
# def choose_option(message):
#     if message.text == 'Python' or message.text == 'C++':
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.row('Начать', 'Выбор урока')
#         bot.send_message(message.chat.id, "Отлично! Теперь выбери действие:", reply_markup=markup)
#         bot.register_next_step_handler(message, handle_option)
#     else:
#         bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# # Обработчик для кнопок "Начать" и "Выбор урока"
# def handle_option(message):
#     if message.text == 'Начать':
#         bot.send_photo(message.chat.id, open('your_image.jpg', 'rb'))
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.row('Показать ответ', 'Дальше')
#         bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
#         bot.register_next_step_handler(message, handle_action)
#     elif message.text == 'Выбор урока':
#         show_lessons(message)
#     else:
#         bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# # Обработчик для кнопок "Показать ответ" и "Дальше"
# def handle_action(message):
#     if message.text == 'Показать ответ':
#         bot.send_photo(message.chat.id, open('your_answer_image.jpg', 'rb'))
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.row('Дальше')
#         bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
#         bot.register_next_step_handler(message, handle_next)
#     elif message.text == 'Дальше':
#         bot.send_message(message.chat.id, "Переход к следующему уроку.")
#         # Добавьте ваш код для перехода к следующему уроку
#     else:
#         bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# # Функция для показа уроков
# def show_lessons(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     # Добавьте кнопки для каждого урока
#     markup.row('Урок 1', 'Урок 2', 'Урок 3')
#     bot.send_message(message.chat.id, "Выбери урок:", reply_markup=markup)
#     bot.register_next_step_handler(message, handle_lesson)

# # Обработчик для выбора урока
# def handle_lesson(message):
#     bot.send_message(message.chat.id, f"Вы выбрали урок {message.text}.")
#     # Добавьте ваш код для работы с выбранным уроком

# # Обработчик для кнопки "Дальше" после показа ответа
# def handle_next(message):
#     bot.send_message(message.chat.id, "Переход к следующему уроку.")
#     # Добавьте ваш код для перехода к следующему уроку

# if __name__ == '__main__':
#     bot.polling(none_stop=True)

import telebot
from telebot import types

TOKEN = '6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояний пользователя
user_state = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_state[message.chat.id] = 'start'
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row('Начало', 'ТП', 'Как', 'Я')
    bot.send_message(message.from_user.id, "Привет! Я бот для изучения языков программирования. Выбери раздел:", reply_markup=user_markup)

# Обработчик для кнопок "Начало", "ТП", "Как", "Я"
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'Начало':
        choose_language(message)
    elif message.text == 'ТП' or message.text == 'Как' or message.text == 'Я':
        bot.send_message(message.chat.id, "Функционал этой кнопки еще не реализован.")
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Функция для выбора языка программирования
def choose_language(message):
    user_state[message.chat.id] = 'choose_language'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Python', 'C++', 'Назад')
    bot.send_message(message.chat.id, "Выбери язык программирования:", reply_markup=markup)
    bot.register_next_step_handler(message, choose_option)

# Функция для выбора опции после выбора языка
def choose_option(message):
    if message.text == 'Python' or message.text == 'C++':
        user_state[message.chat.id] = 'choose_option'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Начать', 'Выбор урока', 'Назад')
        bot.send_message(message.chat.id, "Отлично! Теперь выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_option)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Обработчик для кнопок "Начать" и "Выбор урока"
def handle_option(message):
    if message.text == 'Начать':
        user_state[message.chat.id] = 'handle_option'
        bot.send_photo(message.chat.id, open('your_image.jpg', 'rb'))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Показать ответ', 'Дальше', 'Назад')
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_action)
    elif message.text == 'Выбор урока':
        show_lessons(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Обработчик для кнопок "Показать ответ" и "Дальше"
def handle_action(message):
    if message.text == 'Показать ответ':
        user_state[message.chat.id] = 'handle_action'
        bot.send_photo(message.chat.id, open('your_answer_image.jpg', 'rb'))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Дальше', 'Назад')
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_next)
    elif message.text == 'Дальше':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        # Добавьте ваш код для перехода к следующему уроку
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Функция для показа уроков
def show_lessons(message):
    user_state[message.chat.id] = 'show_lessons'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Добавьте кнопки для каждого урока
    markup.row('Урок 1', 'Урок 2', 'Урок 3', 'Назад')
    bot.send_message(message.chat.id, "Выбери урок:", reply_markup=markup)

# Обработчик для выбора урока
@bot.message_handler(func=lambda message: True)
def handle_lesson(message):
    if message.text.startswith('Урок'):
        bot.send_message(message.chat.id, f"Вы выбрали урок {message.text}.")
        # Добавьте ваш код для работы с выбранным уроком
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

# Обработчик для выбора урока
def handle_lesson(message):
    bot.send_message(message.chat.id, f"Вы выбрали урок {message.text}.")
    # Добавьте ваш код для работы с выбранным уроком

# Обработчик для кнопки "Дальше" после показа ответа
def handle_next(message):
    bot.send_message(message.chat.id, "Переход к следующему уроку.")
    # Добавьте ваш код для перехода к следующему уроку

# Обработчик для кнопки "Назад"
def handle_back(message):
    if message.chat.id in user_state:
        current_state = user_state[message.chat.id]
        # Remove the current state from user_state to avoid recursive loop
        user_state.pop(message.chat.id, None)

        if current_state == 'choose_language':
            handle_start(message)
        elif current_state == 'choose_option':
            choose_language(message)
        elif current_state == 'handle_option':
            choose_option(message)
        elif current_state == 'handle_action':
            handle_option(message)
        elif current_state == 'show_lessons':
            choose_option(message)
        elif current_state == 'handle_lesson':
            show_lessons(message)
        elif current_state == 'handle_next':
            handle_action(message)
        else:
            handle_start(message)
    else:
        handle_start(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
>>>>>>> 1fab133a8aa11bc5da69ef47642e6090a68674f1
