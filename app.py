import assets.handlers.handler_import
from assets.dispatcher.dispatcher import dp
from aiogram import executor

executor.start_polling(dp)