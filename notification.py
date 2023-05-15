import time
from telebot import types
import datetime
from connector import ConnectorNotification
from bot import bot
chat_id = -941273178


def infinite_loop():
    while True:
        active_tasks = ConnectorNotification.get_task_active()
        print("Активные задачи")
        for task in active_tasks:
            now = datetime.datetime.now()
            print(now.hour)
            if now.hour == 10:
                print(task.description)
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

        time.sleep(3600)


if __name__ == '__main__':
    infinite_loop()
