from aiogram import types, Dispatcher
from aiogram.filters import Command

from create_bot import bot
import database as db
import keyboards as kb


async def command_start_handler(message: types.Message):
    try:
        await message.delete()
    finally:
        db.new_user(user_id=message.from_user.id, first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name, username=message.from_user.username,
                    reg_date=str(message.date))
        await message.answer(
            text=f"<b>{['Доброй ночи', 'Доброе утро', 'Добрый день', 'Добрый вечер'][(message.date.hour + 3) % 24 // 6]}, {message.from_user.first_name}!</b>\nБот поможет узнать лучшие курсы иностранных валют в банках Беларуси.\nЧтобы узнать курсы валют, воспользуйтесь кнопками ниже.\n\n@cur_by_bot",
            reply_markup=kb.start_kb)


async def set_commands_handler(message: types.Message):
    try:
        await message.delete()
    finally:
        await bot.set_my_commands(commands=[types.BotCommand(command="start", description="Перезапуск"),
                                            types.BotCommand(command="help", description="Помощь")])
        await message.answer(text='<b>Список команд успешно обновлён.</b>',
                             reply_markup=kb.start_kb)


async def command_help_handler(message: types.Message):
    try:
        await message.delete()
    finally:
        kb_help = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text='✍️Написать', url='https://t.me/id7489')]])
        await message.answer(
            text="<b>Если у Вас возникли проблемы при работе с ботом, вы можете связаться с разработчиком.</b>",
            reply_markup=kb_help)


async def other_messages(message: types.Message):
    try:
        await message.delete()
    finally:
        await message.answer(
            text=f"<b>Для работы с ботом, воспользуйтесь, пожалуйста, кнопками.</b>\nБот поможет узнать лучшие курсы иностранных валют в банках Беларуси.\nЧтобы узнать курсы валют, воспользуйтесь кнопками ниже.\n\n@cur_by_bot",
            reply_markup=kb.start_kb)


def register(dp: Dispatcher):
    dp.message.register(command_start_handler, Command(commands=["start"]))
    dp.message.register(command_help_handler, Command(commands=["help"]))
    dp.message.register(set_commands_handler, Command(commands=["set_commands"]))
    dp.message.register(other_messages)
