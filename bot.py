import time
import telebot
from telebot import types
from static_text import pre_statement_the_problem
import datetime
import re
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from connector import ConnectorCreateTask, ConnectorNotification


#TOKEN = ""
bot = telebot.TeleBot(TOKEN, parse_mode=None)
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")
chat_id = -941273178

"""
# Оповещения
def infinite_loop():
    while True:
        active_tasks = ConnectorNotification.get_task_active()
        for task in active_tasks:
            print(task)
            now = datetime.datetime.now()
            if now.hour == 15:
                if now.year == task.date.year and now.month == task.date.month and now.day == task.date.day - 1:
                    text = f"<b>НАПОМИНАНИЕ ЗА СУТКИ</b>\n" \
                           f"<b>ОТВЕТСТВЕННЫЙ:</b>\n@{task.responsible}\n" \
                           f"<b>СРОК ЗАДАЧИ:</b>\n{task.time.strftime('%H:%M')} {task.date.strftime('%d.%m.%y')}\n" \
                           f"<b>ОПИСАНИЕ ЗАДАЧИ:</b>\n{task.description}\n" \
                           f"\nЗадача выполнена?"
                    menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
                    menu_keyboard.add(
                        types.InlineKeyboardButton(text='Да', callback_data=f'completed_yes_{task.id}'))
                    menu_keyboard.add(
                        types.InlineKeyboardButton(text='Нет', callback_data=f'completed_no_{task.id}'))
                    bot.send_message(chat_id, text, reply_markup=menu_keyboard, parse_mode="HTML")
            if now.year == task.date.year and now.month == task.date.month and\
                    now.day == task.date.day and now.hour == task.time.hour - 1:
                text = f"<b>НАПОМИНАНИЕ ЗА ЧАС</b>\n" \
                       f"<b>ОТВЕТСТВЕННЫЙ:</b>\n@{task.responsible}\n" \
                       f"<b>СРОК ЗАДАЧИ:</b>\n{task.time.strftime('%H:%M')} {task.date.strftime('%d.%m.%y')}\n" \
                       f"<b>ОПИСАНИЕ ЗАДАЧИ:</b>\n{task.description}\n" \
                       f"\nЗадача выполнена?"
                menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
                menu_keyboard.add(
                    types.InlineKeyboardButton(text='Да', callback_data=f'completed_yes_{task.id}'))
                menu_keyboard.add(
                    types.InlineKeyboardButton(text='Нет', callback_data=f'completed_no_{task.id}'))
                bot.send_message(chat_id, text, reply_markup=menu_keyboard, parse_mode="HTML")

        time.sleep(60)


@bot.callback_query_handler(func=lambda call: call.data.startswith('completed_yes'))
def change_status(call):
    result = call.data.split('_')
    id_task = int(result[2])
    if ConnectorNotification.check_responsible_in_task(id_task, call.from_user.username):
        ConnectorNotification.update_active_status(id_task)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text="<b>ЗАДАЧА ВЫПОЛНЕНА</b>", parse_mode="HTML")
    else:
        bot.send_message(chat_id=chat_id,
                         text=f"@{call.from_user.username} следите за своими задачами!")


@bot.callback_query_handler(func=lambda call: call.data.startswith('completed_no'))
def change_status(call):
    result = call.data.split('_')
    id_task = int(result[2])
    if ConnectorNotification.check_responsible_in_task(id_task, call.from_user.username):
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text="До конечного срока осталось мало времени!", parse_mode="HTML")
    else:
        bot.send_message(chat_id=chat_id,
                         text=f"@{call.from_user.username} следите за своими задачами!")


loop_thread = threading.Thread(target=infinite_loop)
loop_thread.start()"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('completed_yes'))
def change_status(call):
    result = call.data.split('_')
    id_task = int(result[2])
    if ConnectorNotification.check_responsible_in_task(id_task, call.from_user.username):
        ConnectorNotification.update_active_status(id_task)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text="<b>ЗАДАЧА ВЫПОЛНЕНА</b>", parse_mode="HTML")
    else:
        bot.send_message(chat_id=chat_id,
                         text=f"@{call.from_user.username} вы не являетесь ответственным по этой задаче!")


@bot.callback_query_handler(func=lambda call: call.data.startswith('completed_no'))
def change_status(call):
    result = call.data.split('_')
    id_task = int(result[2])
    if ConnectorNotification.check_responsible_in_task(id_task, call.from_user.username):
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text="До конечного срока осталось мало времени!", parse_mode="HTML")
    else:
        bot.send_message(chat_id=chat_id,
                         text=f"@{call.from_user.username} вы не являетесь ответственным по этой задаче!")


# Модуль создания задачи
@bot.message_handler(commands=['create_task'])
def send_menu(message):
    bot.reply_to(message, pre_statement_the_problem)

    menu_keyboard = types.InlineKeyboardMarkup()
    menu_keyboard.add(
        types.InlineKeyboardButton(text='Выбрать ответственного', callback_data='select_responsible'))
    bot.send_message(message.chat.id, 'Шаг 1:', reply_markup=menu_keyboard)

    ConnectorCreateTask.create_task_add_producer(message.from_user.username)


# Кнопки с выбором ответственного
@bot.callback_query_handler(func=lambda call: call.data.startswith('select_responsible'))
def select_responsible_keyboard(call):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    keyboard.add(types.InlineKeyboardButton(text="Кучеренко И.", callback_data=f"responsible_kecherenkoivan"))
    keyboard.add(types.InlineKeyboardButton(text="Ананьев И.", callback_data=f"responsible_IP_Ananiev"))
    keyboard.add(types.InlineKeyboardButton(text="Асанов А.", callback_data=f"responsible_asanov"))  # change
    keyboard.add(types.InlineKeyboardButton(text="Смирнова Л.", callback_data=f"responsible_smirnova"))  # change
    keyboard.add(types.InlineKeyboardButton(text="Антипов А.", callback_data=f"responsible_antipov"))  # change
    keyboard.add(types.InlineKeyboardButton(text="Гарев К.", callback_data=f"responsible_garevkv"))
    keyboard.add(types.InlineKeyboardButton(text="Таргонская А.", callback_data=f"responsible_targonskaya"))  # change

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Нажмите на кнопку для выбора ответственного руководителя:', reply_markup=keyboard)


# Выбор ответственного
@bot.callback_query_handler(func=lambda call: call.data.startswith('responsible_'))
def select_responsible(call):
    trash, responsible = call.data.split('_')

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'Вы выбрали ответственного: @{responsible}')
    ConnectorCreateTask.create_task_add_responsible(call.from_user.username, responsible)

    menu_keyboard = types.InlineKeyboardMarkup()
    menu_keyboard.add(
        types.InlineKeyboardButton(text='Выберите дату срока задачи', callback_data='select_date'))
    bot.send_message(call.message.chat.id, 'Шаг 2:', reply_markup=menu_keyboard)


# Открытие календаря
@bot.callback_query_handler(func=lambda call: call.data.startswith('select_date'))
def select_date_keyboard(call):
    now = datetime.datetime.now()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Если вы выберите прошедшую дату, то она перенесется на следующий год')
    bot.send_message(
        call.message.chat.id,
        "Выберите дату",
        reply_markup=calendar.create_calendar(
            name=calendar_1_callback.prefix,
            year=now.year,
            month=now.month,
        ),
    )


# Выбор даты
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1_callback.prefix))
def select_date(call: types.CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date_choice = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    if action == "DAY":
        now = datetime.datetime.now()
        if now.day > date_choice.day or now.month > date_choice.month:
            date_choice = now.replace(year=now.year + 1)
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"Вы выбрали дату: {date_choice.strftime('%d.%m.%Y')}",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        ConnectorCreateTask.create_task_add_date(call.from_user.username, date_choice)
        menu_keyboard = types.InlineKeyboardMarkup()
        menu_keyboard.add(
            types.InlineKeyboardButton(text='Определите время срока задачи', callback_data='select_time'))
        bot.send_message(call.message.chat.id, 'Шаг 3:', reply_markup=menu_keyboard)

    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Дата не выбрана",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        menu_keyboard = types.InlineKeyboardMarkup()
        menu_keyboard.add(
            types.InlineKeyboardButton(text='Выберите дату', callback_data='select_date'))
        bot.send_message(call.message.from_user.id, 'Шаг 2:', reply_markup=menu_keyboard)
        print(f"{calendar_1_callback}: Cancellation")


# Модули для выбора времени
@bot.callback_query_handler(func=lambda call: call.data.startswith('select_time'))
def select_time(call):
    sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text='Введите время в формате ЧЧ:ММ')
    bot.register_next_step_handler(sent, input_time)


def input_time(message):
    if re.match(r'^\d{1,2}:\d{2}$', message.text):
        hours, minutes = map(int, message.text.split(':'))
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            bot.send_message(
                chat_id=message.from_user.id,
                text=f"Вы выбрали время: {message.text}",
            )
            add_time = datetime.datetime.strptime(message.text, "%H:%M").time()

            ConnectorCreateTask.create_task_add_time(message.from_user.username, add_time)

            menu_keyboard = types.InlineKeyboardMarkup()
            menu_keyboard.add(
                types.InlineKeyboardButton(text='Описание задачи', callback_data='select_description'))
            bot.send_message(message.chat.id, 'Шаг 4:', reply_markup=menu_keyboard)
        else:
            sent = bot.send_message(chat_id=message.chat.id,
                                    text='Время введено неверно!\nВведенные значения должны соответствовать формату:\n'
                                         'ЧЧ - от 0 до 23\n'
                                         'ММ - от 00 до 59')
            bot.register_next_step_handler(sent, input_time)
    else:
        sent = bot.send_message(chat_id=message.chat.id,
                                text='Время введено неверно!\nВведите время в формате ЧЧ:ММ')
        bot.register_next_step_handler(sent, input_time)


# Модули для написания задачи
@bot.callback_query_handler(func=lambda call: call.data.startswith('select_description'))
def select_description(call):
    sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text='Обратите внимание, что постановка должна содержать образ результата!')
    bot.register_next_step_handler(sent, input_description)


def input_description(message):
    ConnectorCreateTask.create_task_add_description(message.from_user.username, message.text)

    task = ConnectorCreateTask.get_created_task(message.from_user.username)

    text = f"<i>Новая задача!</i>\n" \
           f"<b>Ответственный:</b>\n" \
           f"@{task.responsible}\n"\
           f"<b>Срок задачи:</b>\n"\
           f"{task.time.strftime('%H:%M')} {task.date.strftime('%d.%m.%Y')}\n"\
           f"<b>Описание задачи:</b>\n"\
           f"{task.description}"

    bot.send_message(message.chat.id, text, parse_mode="HTML")

    try:
        bot.send_message(chat_id, text, parse_mode="HTML")
    except Exception:
        bot.send_message(message.chat.id, "Отправка в чат не работает, обратитесь к разработчику", parse_mode="HTML")


bot.set_my_commands([
    telebot.types.BotCommand("/create_task", "Поставить задачу")
])


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
