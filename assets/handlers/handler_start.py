import string, secrets
from assets.checker.main_app import checker_tsn, checker_zt
from assets.config.cfg import add_id_to_settings, channel_id
from assets.data.db import add_code, check_ban, create_tables_if_not_exist, get_post_pid, get_user
from assets.keyboard.keyboard_inline_all import delete
from assets.keyboard.keyboard_main import edit_post
from assets.states.edit_post import post
from assets.states.settings_state import add
from .handler_imports import *

@dp.message_handler(commands=['start'], state='*')
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username
    if await check_ban(user_id) == 1: return
    await state.finish()

    text = """В процессі..."""

    if not user_name:
        await bot.send_message(user_id, "<b>На жаль, у вас немає username'а Телеграм.\nВстановіть його в налаштуваннях.</b>")
        return

    if await get_user(user_id):
        #await bot.send_message(user_id, text, reply_markup=main(user_id))
        await bot.send_message(user_id, text)
    else:
        await bot.send_message(message.from_user.id, "<b>Вас не знайдено в базі даних, введіть код пропуску:</b>", reply_markup=delete())
        await add.code.set()

@dp.message_handler(commands=['add'])
async def add_command_handler(message: Message):
    if await check_ban(message.from_user.id) == 1 or message.from_user.id not in get_admins(): return
    args = message.get_args()
    if not args:
        await message.reply("Будь ласка, вкажіть ID для додавання.")
        return

    new_id = args.strip()

    add_id_to_settings(new_id)

    await message.reply(f"ID {new_id} додано в settings.ini.")

@dp.message_handler(commands=['code'])
async def add_codex(message: Message):
    if await check_ban(message.from_user.id) == 1 or message.from_user.id not in get_admins(): return
    
    code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
    await add_code(code)
    await message.reply(f"<b>Код <code>{code}</code> додано!</b>")

@dp.message_handler(commands=['create'])
async def createpostx(message: Message):
    if await check_ban(message.from_user.id) == 1 or message.from_user.id not in get_admins(): return
    await bot.send_message(message.from_user.id, "<b>Відправте дані для посту:\n\nПісля відправки даних, пост одразу буде опубліковано!</b>")
    await post.post.set()

@dp.message_handler(commands=['go'], state='*')
async def gogo(message: Message):
    if await check_ban(message.from_user.id) == 1 or message.from_user.id not in get_admins(): return
    await create_tables_if_not_exist()
    await bot.send_message(message.from_user.id, "yesss")

@dp.message_handler(commands=['check'])
async def check_info(message: Message):
    if await check_ban(message.from_user.id) == 1 or message.from_user.id not in get_admins(): return
    g = await bot.send_message(message.chat.id, "<b>⏳ Дані оновлюються...</b>")
    await checker_zt()
    await checker_tsn()
    await g.edit_text("<b>✅ Дані оновлено.</b>")

@dp.message_handler(content_types=types.ContentType.ANY)
async def handle_message(message: Message):
    if await check_ban(message.from_user.id) == 1 or message.from_user.id not in get_admins(): return
    if message.forward_from_chat and str(message.forward_from_chat.id) == channel_id:
        #forwarded_message_id = message.forward_from_message_id
        post = await get_post_pid(message.forward_from_message_id)
        if post:
            await bot.send_message(message.from_user.id, "<b>Пост знайдено в базі даних. Виберіть що треба зробити з постом:</b>", reply_markup=edit_post(message.forward_from_message_id))
        else:
            await bot.send_message(message.from_user.id, "<b>Пост не знайдено в базі даних.</b>", reply_markup=delete())
            return
    else:
        pass