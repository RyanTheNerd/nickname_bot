from pymongo import MongoClient
from random import randrange

client = MongoClient()
db = client.nicknames

serverStatusResult = db.command("serverStatus")

def remove_all_names(id_num):
    db.nicknames.remove({'id': id_num})
    return

def get_nickname(id_num, original):
    nicknames_db = db.nicknames.find({'id': id_num})
    nicknames = []
    for nickname in nicknames_db:
        nicknames.append(nickname["nickname"])
    nickname = False
    if len(nicknames) < 2:
        return original
    while nickname == False or nickname == original:
        nickname = nicknames[randrange(len(nicknames))]
    return nickname 

def remove_nickname(id_num, nickname):
    nicknames = db.nicknames.remove({"nickname": nickname})

def add_nickname(id_num, nickname):
    matches = db.nicknames.find({'id': id_num, 'nickname': nickname})
    if matches.count() == 1:
        return False
    post_data = {
        "nickname": nickname,
        "id": id_num,
    }
    db.nicknames.insert_one(post_data)
    return True


def list_names(id_num):
    nicknames = db.nicknames.find({'id': id_num})
    name_list = ""

    for index, nickname in enumerate(nicknames):
        name_list += f"{index + 1}. {nickname['nickname']}\n"

    return name_list


# Test code:
#add_nickname(509528, "billy")
#print(get_nickname(509528))
#add_nickname(509528, "suzy")
#add_nickname(509528, "sally")
#
#print(list_names(509528))
#
#remove_nickname(509528, "billy")
#remove_nickname(509528, "suzy")
#remove_nickname(509528, "sally")
#

