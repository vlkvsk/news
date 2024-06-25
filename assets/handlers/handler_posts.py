from assets.data.db import change_p_id, check_ban, delete_post, delete_zav, get_post
from assets.handlers.handler_inline_all import send_message_in_tech
from assets.states.edit_post import post
from .handler_imports import *
from assets.config.cfg import channel_id, main_link

@dp.callback_query_handler(text_startswith='send_post:', state='*')
async def sendpost(call: CallbackQuery, state: FSMContext):
    m_id = call.data.split(":")[1]
    post = await get_post(m_id)
    if post:
        g = await bot.copy_message(
            chat_id=channel_id,
            from_chat_id=call.message.chat.id,
            message_id=m_id
        )
        await change_p_id(m_id, g.message_id)
        channel_link = f'https://t.me/c/{channel_id[4:]}/{g.message_id}'
        await call.message.edit_text(f'<b>✅ Відправлено</b>\n\n<a href="{channel_link}">Дивитись пост</a>')
    else:
        await call.message.edit_text("<b>Пост не знайдено.</b>")
    await state.finish()

@dp.callback_query_handler(text_startswith='delete_zav:', state='*')
async def sendpost(call: CallbackQuery, state: FSMContext):
    m_id = call.data.split(":")[1]
    try:
        await delete_zav(m_id)
        await call.answer("Видалено!", show_alert=False)
    except Exception as e:
        send_message_in_tech(
            error_text=f"Помилка під час видалення запису посту: {e}",
            user_id=call.from_user.id,
            username=call.from_user.username
        )
        await call.answer("Виникла помилка!", show_alert=True)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=m_id)
    await state.finish()

@dp.callback_query_handler(text_startswith='delete_post:', state='*')
async def sendpost(call: CallbackQuery, state: FSMContext):
    try:
        post_id = call.data.split(":")[1]
        await delete_post(post_id)
        await call.answer("Пост видалено з каналу!", show_alert=True)
        await bot.delete_message(chat_id=channel_id, message_id=post_id)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    except Exception as e:
        send_message_in_tech(
            error_text=f"Помилка під час видалення посту: {e}",
            user_id=call.from_user.id,
            username=call.from_user.username
        )
    await state.finish()

@dp.message_handler(state=post.post, content_types=['photo', 'text'])
async def postcreate(message: types.Message, state: FSMContext):
    if await check_ban(message.from_user.id) == 1 or message.from_user.id not in get_admins():
        return

    text = message.caption or message.text or ''

    caption = f"{text}\n\n<a href='{main_link}'>🇺🇦 Україна понад усе</a>"

    if message.photo:
        photo_file_id = message.photo[-1].file_id
        await bot.send_photo(channel_id, photo=photo_file_id, caption=caption)
    else:
        await bot.send_message(channel_id, caption)

    await state.finish()