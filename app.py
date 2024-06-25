import asyncio
from assets.checker.main_app import checker_tsn, checker_zt
import assets.handlers.handler_import
from assets.dispatcher.dispatcher import dp
from aiogram import executor


async def async_function():
    await checker_tsn()
    await asyncio.sleep(2)
    await checker_zt()

async def on_startup(_):
    asyncio.create_task(main())

async def main():
    while True:
        try:
            await async_function()
            await asyncio.sleep(120)
        except KeyboardInterrupt:
            print("Игнорирование KeyboardInterrupt")

try:
    executor.start_polling(dp, on_startup=on_startup)
except KeyboardInterrupt:
    print("Завершение программы")