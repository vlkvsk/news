from assets.data.db import change_p_id, delete_post, delete_zav, get_post
from assets.handlers.handler_inline_all import send_message_in_tech
from .handler_imports import *
from assets.config.cfg import channel_id

@dp.callback_query_handler(text_startswith='send_post:', state='*')
async def sendpost(call: CallbackQuery, state: FSMContext):
    m_id = call.data.split(":")[1]
    post = get_post(m_id)
    if post:
        g = await bot.copy_message(
            chat_id=channel_id,
            from_chat_id=call.message.chat.id,
            message_id=m_id
        )
        change_p_id(m_id, g.message_id)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        channel_link = f'https://t.me/c/{channel_id[4:]}/{g.message_id}'
        await bot.send_message(
            call.from_user.id,
            f'<b>✅ Відправлено</b>\n\n<a href="{channel_link}">Дивитись пост</a>'
        )
    else:
        await bot.send_message(call.from_user.id, "Пост не знайдено")
    await state.finish()

@dp.callback_query_handler(text_startswith='delete_zav:', state='*')
async def sendpost(call: CallbackQuery, state: FSMContext):
    m_id = call.data.split(":")[1]
    try:
        delete_zav(m_id)
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
        delete_post(post_id)
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