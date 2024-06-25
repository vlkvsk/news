from .keyboard_imports import *

def send(m_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(ikb(text='✅ Відправити', callback_data=f'send_post:{m_id}'), ikb(text='🗑 Видалити', callback_data=f'delete_zav:{m_id}'))
    return keyboard

def edit_post(post_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(ikb(text='🗑 Видалити', callback_data=f'delete_post:{post_id}'))
    return keyboard