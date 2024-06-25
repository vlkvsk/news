import configparser
import sys
sys.dont_write_bytecode=True
read_config = configparser.ConfigParser()
read_config.read("settings.ini")

BOT_TOKEN = read_config['settings']['token'].strip().replace(" ", "")
PATH_DATABASE = 'assets/data/db.db'
a_chat_id = read_config["chats"]['a_chat_id']
tech_chat_id = read_config["chats"]['tech_chat_id']
channel_id = read_config["channels"]['channel_id']
main_link = read_config["links"]['main_link']

#other
admin_id = read_config["ids"]['admin_id']

def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['ids']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: admins.remove("")
    while " " in admins: admins.remove(" ")
    while "\r" in admins: admins.remove("\r")
    while "\n" in admins: admins.remove("\n")

    admins = list(map(int, admins))

    return admins

def add_id_to_settings(new_id):
    if 'ids' not in read_config:
        read_config['ids'] = {}

    admin_ids = read_config['ids'].get('admin_id', '')

    if admin_ids:
        id_list = admin_ids.split(',')
        if new_id not in id_list:
            id_list.append(new_id)
            read_config['ids']['admin_id'] = ','.join(id_list)
    else:
        read_config['ids']['admin_id'] = new_id

    with open('settings.ini', 'w') as configfile:
        read_config.write(configfile)