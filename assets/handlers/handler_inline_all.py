from assets.data.db import add_user, check_ban, get_code
from assets.keyboard.keyboard_inline_all import delete
from .handler_imports import *
from assets.states.settings_state import add
from assets.config.cfg import tech_chat_id
import time

last_error_times = {}

@dp.callback_query_handler(text='delete_message', state='*')
async def deletex(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer("Повідомлення видалено.", show_alert=False)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@dp.message_handler(state=add.code)
async def deletex(message: Message, state: FSMContext):
    if check_ban(message.from_user.id) == 1: return
    code = message.text
    if get_code(code):
        add_user(message.from_user.id, message.from_user.username)
        await bot.send_message(message.from_user.id, "Успішно додані до бази даних.", reply_markup=delete())
    else:
        await bot.send_message(message.from_user.id, "Код невірний.", reply_markup=delete())
    await state.finish()

async def send_message_in_tech(error_text, user_id, username):
    global last_error_times
    current_time = time.time()

    if error_text in last_error_times and current_time - last_error_times[error_text] < 30:
        return

    await bot.send_message(chat_id=tech_chat_id, text=f'⚠️⚠️⚠️\n<b>Помилка від @{username}, ID: {user_id}</b>\n\n<code>{error_text}</code>', reply_markup=delete())
    last_error_times[error_text] = current_time