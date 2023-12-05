import telebot
from telebot import types
import subprocess
import os
import sqlite3

TOKEN = '6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w'
bot = telebot.TeleBot(TOKEN)

user_state = {}


# Подключение к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        premka INTEGER
    )
''')

# Сохранение изменений
conn.commit()

# Закрытие соединения
conn.close()


lessons_cpp = {
    '1': {
        'title': 'Introduction to C++',
        'images': ['lesson_cpp_1.jpg', 'lesson_cpp_2.jpg'],
        'task': 'lesson_cpp_task.jpg',
        'answer': 'lesson_cpp_answer.jpg',
        'code': 'Hello, World!',
    },
    '2': {
        'title': 'Working with Arrays in C++',
        'images': ['lesson_cpp_1.jpg', 'lesson_cpp_2.jpg'],
        'task': 'lesson_cpp_task.jpg',
        'answer': 'lesson_cpp_answer.jpg',
        'code': 'Hello, World!',
    },
    # Add more lessons_cpp as needed
}


lessons_py = {
    '1': {
        'title': 'Introduction to Python',
        'images': ['lesson_1_ter_kar_1.jpg', 'lesson_1_ter_kar_2.jpg'],
        'task': 'lesson_1_task.jpg',
        'answer': 'lesson_1_otv.jpg',
        'code': 'hallo word',
    },
    '2': {
        'title': 'Working with Lists in Python',
        'images': ['lesson_1_ter_kar_3.jpg', 'lesson_1_ter_kar_4.jpg'],
        'task': 'lesson_1_task.jpg',
        'answer': 'lesson_2_otv.jpg',
        'code': 'dogs',
    },
    '3': {
        'title': 'след хуйня',
        'images': ['lesson_1_ter_kar_3.jpg', 'lesson_1_ter_kar_4.jpg'],
        'task': 'lesson_1_task.jpg',
        'answer': 'lesson_3_otv.jpg',
        'code': 'cats', #####################################################################
    },
    # Add more lessons_py as needed
}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    username = message.from_user.username if message.from_user.username else message.from_user.first_name

    # Добавление нового пользователя в базу данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, premka)
        VALUES (?, ?, ?)
    ''', (user_id, username, 1))  # По умолчанию начинаем с первого урока
    conn.commit()
    conn.close()

    # Остальной код обработки старта
    user_state[message.chat.id] = 1
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row('Начало', 'ТП', 'Как', 'Я')
    bot.send_message(user_id, "Привет! Я бот для изучения языков программирования. Выбери раздел:", reply_markup=user_markup)

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

def choose_language(message):
    user_state[message.chat.id] = 'choose_language'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Python', 'C++', 'Назад')
    bot.send_message(message.chat.id, "Выбери язык программирования:", reply_markup=markup)
    bot.register_next_step_handler(message, choose_option)

def choose_option(message):
    if message.text == 'Python':
        user_state[message.chat.id] = 'choose_option_py'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Начать', 'Выбор урока', 'Назад')
        bot.send_message(message.chat.id, "Отлично! Теперь выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_option_py)
    elif message.text == 'C++':
        user_state[message.chat.id] = 'choose_option_cpp'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Начать', 'Выбор урока', 'Назад')
        bot.send_message(message.chat.id, "Отлично! Теперь выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_option_cpp)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")


def handle_option_py(message):
    if message.text == 'Начать':
        user_state[message.chat.id] = 'handle_option_py'
        lesson_number = '1'
        show_lesson_py(message, lesson_number)
    elif message.text == 'Выбор урока':
        show_lesson_pys_py(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lesson_pys_py(message):
    user_state[message.chat.id] = 'show_lesson_pys_py'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for lesson_number, lesson_info in lessons_py.items():
        markup.row(f'Урок {lesson_number}: {lesson_info["title"]}')

    markup.row('Назад')
    bot.send_message(message.chat.id, "Выбери урок:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_lesson_py)

def handle_lesson_py(message):
    lesson_number = message.text.split(' ')[-1]
    if lesson_number in lessons_py:
        show_lesson_py(message, lesson_number)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lesson_py(message, lesson_number):
    user_state[(message.chat.id, 'lesson_number')] = lesson_number ##############################################################
    lesson_info = lessons_py[lesson_number]

    bot.send_message(message.chat.id, f"Урок {lesson_number}: {lesson_info['title']}")###############################################

    for image_path in lesson_info['images']:
        if os.path.exists(image_path):
            image = open(image_path, 'rb')
            bot.send_photo(message.chat.id, image)
        else:
            bot.send_message(message.chat.id, f"Image file not found: {image_path}")

    task_image = open(lesson_info['task'], 'rb')
    bot.send_photo(message.chat.id, task_image)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Ввести код', 'Далее', 'Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_action_py)

def handle_action_py(message):
    if message.text == 'Ввести код':
        user_state[message.chat.id] = 'handle_action_py'
        bot.send_message(message.chat.id, "Пожалуйста, введите свой код:")
        bot.register_next_step_handler(message, handle_user_code_py)
    elif message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson_py(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def handle_next_lesson_py(message):
    try:
        # Получаем текущий номер урока из user_state
        current_lesson_number = int(user_state.get((message.chat.id, 'lesson_number'), 1)) 

        # Увеличиваем номер урока
        next_lesson_number = current_lesson_number + 1

        # Проверяем, существует ли информация о следующем уроке
        if str(next_lesson_number) in lessons_py:
            # Обновляем user_state
            user_state[(message.chat.id, 'lesson_number')] = next_lesson_number

            # Отображаем следующий урок
            show_lesson_py(message, str(next_lesson_number))
        else:
            bot.send_message(message.chat.id, "Урок не найден.")
            handle_back(message)

    except ValueError:
        bot.send_message(message.chat.id, "Error: Lesson number is not a valid integer.")
        handle_back(message)


def handle_user_code_py(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons_py.get(str(lesson_number))
        if lesson_info is None:
            bot.send_message(message.chat.id, "Error: Lesson information not found.")
            handle_back(message)
            return

        expected_code = lesson_info.get('code')
        if expected_code is None:
            bot.send_message(message.chat.id, "Error: Expected code not found.")
            handle_back(message)
            return

        user_code = message.text

        # Compare the user's code with the expected code

        # Установка ограничения времени выполнения и объема памяти
        process = subprocess.run(['python', '-c', user_code], capture_output=True, text=True, timeout=5)
        if process.returncode != 0:
            raise Exception(f"Произошла ошибка при выполнении кода. Код завершился с кодом возврата {process.returncode}.")

        # Проверка результата выполнения кода
        if expected_code in process.stdout:
            bot.send_message(message.chat.id, "Код выполнен верно!")
            show_answer_py(message)
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


def show_buttons(message):
    user_state[message.chat.id] = 'show_buttons'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Показать ответ', 'Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_buttons_after_code_py)

def handle_buttons_after_code_py(message):
    if message.text == 'Показать ответ':
        show_answer_py(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_answer_py(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons_py.get(str(lesson_number))
        if lesson_info is None:
            bot.send_message(message.chat.id, "Error: Lesson information not found.")
            handle_back(message)
            return

        answer_image_path = lesson_info.get('answer')
        if answer_image_path is None:
            bot.send_message(message.chat.id, "Error: Answer image not found.")
            handle_back(message)
            return

        # Replace this with your logic to show the answer image
        answer_image = open(answer_image_path, 'rb')
        bot.send_photo(message.chat.id, answer_image)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Далее', 'Назад')
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_buttons_after_answer_py)

    except Exception as e:
        # Handle any exceptions that may occur during the process
        bot.send_message(message.chat.id, f"Error while showing answer:\n{str(e)}")
        handle_back(message)

def handle_buttons_after_answer_py(message):
    if message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson_py(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")



#########################################################################

def handle_option_cpp(message):
    if message.text == 'Начать':
        user_state[message.chat.id] = 'handle_option_cpp'
        lesson_number = '1'
        show_lesson_cpp(message, lesson_number)
    elif message.text == 'Выбор урока':
        show_lesson_pys_cpp(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lesson_pys_cpp(message):
    user_state[message.chat.id] = 'show_lesson_pys_cpp'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for lesson_number, lesson_info in lessons_cpp.items():
        markup.row(f'Урок {lesson_number}: {lesson_info["title"]}')

    markup.row('Назад')
    bot.send_message(message.chat.id, "Выбери урок:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_lesson_cpp)

def handle_lesson_cpp(message):
    lesson_number = message.text.split(' ')[-1]
    if lesson_number in lessons_cpp:
        show_lesson_cpp(message, lesson_number)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lesson_cpp(message, lesson_number):
    user_state[(message.chat.id, 'lesson_number')] = lesson_number
    lesson_info = lessons_cpp[lesson_number]

    bot.send_message(message.chat.id, f"Урок {lesson_number}: {lesson_info['title']}")

    for image_path in lesson_info['images']:
        if os.path.exists(image_path):
            image = open(image_path, 'rb')
            bot.send_photo(message.chat.id, image)
        else:
            bot.send_message(message.chat.id, f"Image file not found: {image_path}")

    task_image = open(lesson_info['task'], 'rb')
    bot.send_photo(message.chat.id, task_image)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Ввести код', 'Далее', 'Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_action_cpp)


def handle_action_cpp(message):
    if message.text == 'Ввести код':
        user_state[message.chat.id] = 'handle_action_cpp'
        bot.send_message(message.chat.id, "Пожалуйста, введите свой код:")
        bot.register_next_step_handler(message, handle_user_code_cpp)
    elif message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson_cpp(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def handle_user_code_cpp(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons_cpp.get(str(lesson_number))
        if lesson_info is None:
            bot.send_message(message.chat.id, "Error: Lesson information not found.")
            handle_back(message)
            return

        expected_code = lesson_info.get('code')
        if expected_code is None:
            bot.send_message(message.chat.id, "Error: Expected code not found.")
            handle_back(message)
            return

        user_code = message.text

        # Сравнение кода пользователя с ожидаемым кодом

        # Установка ограничения времени выполнения и объема памяти
        process = subprocess.run(['g++', '-x', 'c++', '-'], input=user_code, capture_output=True, text=True, timeout=5)
        if process.returncode != 0:
            raise Exception(f"Произошла ошибка при выполнении кода. Код завершился с кодом возврата {process.returncode}.")

        # Проверка результата выполнения кода
        if expected_code in process.stdout:
            bot.send_message(message.chat.id, "Код выполнен верно!")
            show_answer_cpp(message)
        else:
            bot.send_message(message.chat.id, "Код выполнен, но результат не соответствует ожидаемому.")
            show_buttons_cpp(message)
    except subprocess.TimeoutExpired:
        bot.send_message(message.chat.id, "Превышено ограничение времени выполнения кода.")
        show_buttons_cpp(message)
    except Exception as e:
        # Если произошла ошибка при выполнении кода, сообщаем об этом пользователю
        bot.send_message(message.chat.id, f"Произошла ошибка при выполнении кода:\n{str(e)}")
        show_buttons_cpp(message)

def show_buttons_cpp(message):
    user_state[message.chat.id] = 'show_buttons_cpp'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Показать ответ', 'Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_buttons_after_code_cpp)

def handle_buttons_after_code_cpp(message):
    if message.text == 'Показать ответ':
        show_answer_cpp(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_answer_cpp(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons_cpp.get(str(lesson_number))
        if lesson_info is None:
            bot.send_message(message.chat.id, "Error: Lesson information not found.")
            handle_back(message)
            return

        answer_image_path = lesson_info.get('answer')
        if answer_image_path is None:
            bot.send_message(message.chat.id, "Error: Answer image not found.")
            handle_back(message)
            return

        # Замените это своей логикой для отображения изображения ответа
        answer_image = open(answer_image_path, 'rb')
        bot.send_photo(message.chat.id, answer_image)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Далее', 'Назад')
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_buttons_after_answer_cpp)

    except Exception as e:
        # Обработка любых исключений, которые могут возникнуть в процессе
        bot.send_message(message.chat.id, f"Error while showing answer:\n{str(e)}")
        handle_back(message)

def handle_buttons_after_answer_cpp(message):
    if message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson_cpp(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def handle_next_lesson_cpp(message):
    try:
        current_lesson_number = int(user_state.get((message.chat.id, 'lesson_number'), 1)) 
        next_lesson_number = current_lesson_number + 1

        if str(next_lesson_number) in lessons_cpp:
            user_state[(message.chat.id, 'lesson_number')] = next_lesson_number
            show_lesson_cpp(message, str(next_lesson_number))
        else:
            bot.send_message(message.chat.id, "Урок не найден.")
            handle_back(message)

    except ValueError:
        bot.send_message(message.chat.id, "Error: Lesson number is not a valid integer.")
        handle_back(message)

# Добавьте аналогичные функции для C++, как вы сделали для Python, с учетом особенностей каждого языка.




def handle_back(message):
    if message.chat.id in user_state:
        current_state = user_state[message.chat.id]
        user_state.pop(message.chat.id, None)

        if current_state == 'choose_language':
            handle_start(message)
        elif current_state == 'choose_option_py':
            choose_language(message)
        elif current_state == 'choose_option_cpp':
            choose_language(message)
        elif current_state == 'handle_option_py':
            choose_option(message)
        elif current_state == 'handle_option_cpp':
            choose_option(message)
        elif current_state == 'handle_action_py':
            handle_option_py(message)
        elif current_state == 'handle_action_cpp':
            handle_option_cpp(message)
        elif current_state == 'show_lesson_pys_py':
            choose_option(message)
        elif current_state == 'show_lesson_pys_cpp':
            choose_option(message)
        elif current_state == 'handle_lesson_py':
            show_lesson_pys_py(message)
        elif current_state == 'handle_lesson_cpp':
            show_lesson_pys_cpp(message)
        elif current_state == 'handle_next':
            handle_action_py(message)  # Можно заменить на handle_action_cpp, в зависимости от текущего языка
        else:
            handle_start(message)
    else:
        handle_start(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
