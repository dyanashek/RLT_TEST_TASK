import asyncio
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


import config
import text
from functions import aggregate_data
from validators import input_validator


bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(text.START_MESSAGE)


@dp.message(F.text)
async def cmd_reply(message: types.Message):
    start_date, end_date, group_type = await input_validator(message.text)

    if start_date and end_date and group_type:
        reply = await aggregate_data(start_date, end_date, group_type)

        replies = [reply[i:i + config.MAX_LEN] for i in range(0, len(reply), config.MAX_LEN)]

        for reply in replies:
            await message.answer(reply)
    
    else:
        await message.answer(text.INPUT_ERROR)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())