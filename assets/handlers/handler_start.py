import aiogram
from assets.checker.main_app import checker
from assets.config.cfg import add_id_to_settings, main_link, channel_id
from assets.data.db import add_post, check_ban, create_tables_if_not_exist, get_post_pid, get_user
from aiogram.types import InlineKeyboardMarkup
from assets.keyboard.keyboard_inline_all import delete
from assets.keyboard.keyboard_main import edit_post, send
from assets.states.edit_post import post
from assets.states.settings_state import add
from .handler_imports import *

@dp.message_handler(commands=['start'], state='*')
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username
    if check_ban(user_id) == 1: return
    await state.finish()

    text = """Головне меню"""

    if not user_name:
        await bot.send_message(user_id, "<b>На жаль, у вас немає username'а Телеграм.\nВстановіть його в налаштуваннях.</b>")
        return

    if get_user(user_id):
        #await bot.send_message(user_id, text, reply_markup=main(user_id))
        await bot.send_message(user_id, text)
    else:
        await bot.send_message(message.from_user.id, "<b>Вас не знайдено в базі даних, введіть код пропуску:</b>", reply_markup=delete())
        await add.code.set()

@dp.message_handler(commands=['add'])
async def add_command_handler(message: Message):
    args = message.get_args()
    if not args:
        await message.reply("Будь ласка, вкажіть ID для додавання.")
        return

    new_id = args.strip()

    add_id_to_settings(new_id)

    await message.reply(f"ID {new_id} додано в settings.ini.")

@dp.message_handler(commands=['go'], state='*')
async def gogo(message: Message):
    if message.from_user.id in get_admins():
        await create_tables_if_not_exist()
        await bot.send_message(message.from_user.id, "yesss")
    else: pass

@dp.message_handler(commands=['check'])
async def check_info(message: Message):
    info = checker()
    words = info[1].split()
    first_word, second_word = words[0], words[1] if len(words) > 1 else ""
    remaining_text = ' '.join(words[2:]) if len(words) > 2 else ""

    g = await bot.send_photo(
        chat_id=message.from_user.id,
        photo=info[2],
        caption=f'''
{first_word} <a href="{info[2]}">{second_word}</a> {remaining_text}

{info[3]} - <i>{info[4]}</i>

<a href="{main_link}">🇺🇦 Україна понад усе</a>'''
    )
    await bot.send_message(message.from_user.id, text='Нажміть кнопку "Відправити" щоб відправити пост в канал.', reply_markup=send(g.message_id))
    add_post(
        post_id=0,
        post_title=info[1],
        post_link=info[2],
        post_text=info[3],
        m_id=g.message_id
    )
    return

@dp.message_handler(content_types=types.ContentType.ANY)
async def handle_message(message: Message):
    if message.forward_from_chat and str(message.forward_from_chat.id) == channel_id:
        #forwarded_message_id = message.forward_from_message_id
        post = get_post_pid(message.forward_from_message_id)
        if post:
            await bot.send_message(message.from_user.id, "<b>Пост знайдено в базі даних. Виберіть що треба зробити з постом:</b>", reply_markup=edit_post(message.forward_from_message_id))
        else:
            await bot.send_message(message.from_user.id, "<b>Пост не знайдено в базі даних.</b>", reply_markup=delete())
            return
    else:
        pass