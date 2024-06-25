from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import assets.config.cfg as config

config_variables = {
    "BOT_TOKEN": config.BOT_TOKEN,
    "a_chat_id": config.a_chat_id,
    "admin_id": config.admin_id,
    "tech_chat_id": config.tech_chat_id,
    "channel_id": config.channel_id
}

missing_variables = [k for k, v in config_variables.items() if not v]
if missing_variables:
    exit(f"Відсутні конфігураційні змінні: {', '.join(missing_variables)}")

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())