import asyncio
from aiogram import Bot, Dispatcher, filters, types


bot = Bot("")
dp = Dispatcher()


start_kb = [
    [types.InlineKeyboardButton(text="Открыть конструктор", web_app=types.WebAppInfo(url="http://construcotr.plydev.ru:3000"))]
]

@dp.message(filters.Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать в конструктор чат-ботов. Чтобы продолжить работу, откройте WebApp приложение",
        reply_markup=types.InlineKeyboardMarkup())

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())