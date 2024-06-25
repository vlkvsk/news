from assets.data.db import add_post, add_user, check_ban, get_code
from assets.keyboard.keyboard_inline_all import delete
from assets.keyboard.keyboard_main import send
from .handler_imports import *
from assets.states.settings_state import add
from assets.config.cfg import tech_chat_id, a_chat_id, main_link
import time

last_error_times = {}

@dp.callback_query_handler(text='delete_message', state='*')
async def deletex(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer("Повідомлення видалено.", show_alert=False)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@dp.message_handler(state=add.code)
async def deletex(message: Message, state: FSMContext):
    if await check_ban(message.from_user.id) == 1 or message.from_user.id not in get_admins(): return
    code = message.text
    if await get_code(code):
        await add_user(message.from_user.id, message.from_user.username)
        await bot.send_message(message.from_user.id, "<b>Ви успішно додані до бази даних.</b>", reply_markup=delete())
    else:
        await bot.send_message(message.from_user.id, "<b>Код невірний.</b>", reply_markup=delete())
    await state.finish()

async def send_message_in_tech(error_text, user_id, username):
    global last_error_times
    current_time = time.time()

    if error_text in last_error_times and current_time - last_error_times[error_text] < 30:
        return

    await bot.send_message(chat_id=tech_chat_id, text=f'⚠️⚠️⚠️\n<b>Помилка від @{username}, ID: {user_id}</b>\n\n<code>{error_text}</code>', reply_markup=delete())
    last_error_times[error_text] = current_time

async def send_post_to_confirm(p_title, p_link, p_text, redak):
    words = p_title.split()
    first_word, second_word = words[0], words[1] if len(words) > 1 else ""
    remaining_text = ' '.join(words[2:]) if len(words) > 2 else ""

    g = await bot.send_photo(
        chat_id=a_chat_id,
        photo=p_link,
        caption=f'''
{first_word} <a href="{p_link}">{second_word}</a> {remaining_text}

{p_text}

<a href="{main_link}">🇺🇦 Україна понад усе</a>'''
    )
    await bot.send_message(a_chat_id, text='Нажміть кнопку "Відправити" щоб відправити пост в канал.', reply_markup=send(g.message_id))
    await add_post(
        post_id=0,
        post_title=p_title,
        post_link=p_link,
        post_text=p_text,
        m_id=g.message_id
    )
    return g.message_id