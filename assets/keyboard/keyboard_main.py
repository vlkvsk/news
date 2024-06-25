from .keyboard_imports import *
from assets.config.cfg import get_admins

# def main(user_id):
#     keyboard = InlineKeyboardMarkup()
#     keyboard.add(ikb(text='👨‍💼 Профіль', callback_data='profile_menu'), ikb(text='👛 Гаманець', callback_data='wallet_menu'))
#     keyboard.add(ikb(text='➕ Новий пост', callback_data='new_post'), ikb(text='🤝 Нова угода', callback_data='new_deal'))
#     keyboard.add(ikb(text='📃 Мої пости', callback_data='posts_menu'), ikb(text='👥 Мої чати', callback_data='chats_menu'))
#     keyboard.add(ikb(text='👹 Список кидал', callback_data='scam_menu'), ikb(text='🆘 Допомога', callback_data='help_menu'))
#     if user_id in get_admins():
#         keyboard.add(ikb(text='⚡️ Адмін меню', callback_data='admin_menu'))
#     return keyboard

def send(m_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(ikb(text='✅ Відправити', callback_data=f'send_post:{m_id}'), ikb(text='🗑 Видалити', callback_data=f'delete_zav:{m_id}'))
    return keyboard

def edit_post(post_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(ikb(text='🗑 Видалити', callback_data=f'delete_post:{post_id}'))
    return keyboard