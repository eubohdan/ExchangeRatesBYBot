from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cur_types = {'💵Доллар США': 'usd', '💶Евро': 'eur', '🇷🇺Российский рубль': 'rub', '🇵🇱Польский злотый': 'pln'}
cur_list = list(cur_types.keys())

start_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=cur_list[0]), KeyboardButton(text=cur_list[1])],
                                         [KeyboardButton(text=cur_list[2]), KeyboardButton(text=cur_list[3])]],
                               input_field_placeholder='Для выбора нажмите на кнопку',
                               resize_keyboard=True)
