import subprocess
import os
from pymongo import MongoClient, ReturnDocument
from random import choice


class DB_Client:
    def __init__(self, test=False):

        self.client = MongoClient(port=27018)
        if test is True:
            self.db = self.client.nicknames_test

        else:
            self.db = self.client.nicknames

        self.names = self.db.nicknames
        self.iqs = self.db.iqs

        self.status = self.db.command("serverStatus")

    def get_iq(self, id_num):
        id_num = str(id_num)
        iq = self.iqs.find_one({'id': id_num})
        if iq is not None:
            return iq['iq']
        else:
            self.iqs.insert_one({'id': id_num, 'iq': 100})
            return 100

    def list_iqs(self, server):
        # Get a list of member id's
        members = []
        for member in server.members:
            members.append(member.id)

        # Retrieve member iq's based on id's
        iqs = []
        for iq in self.iqs.find():
            if iq['id'] in members:
                iqs.append(iq)

        iq_list = "IQ Scoreboard:\n"
        for iq in iqs:
            iq_list += f"\t<@{iq['id']}>: {iq['iq']}\n"

        return iq_list
            

    def delta_iq(self, id_num, iq_points):
        id_num = str(id_num)
        user_iq = self.get_iq(id_num)
        return self.iqs.find_one_and_update(
            {'id': id_num}, 
            {'$set': {'iq': user_iq + iq_points}}, 
            return_document=ReturnDocument.AFTER,
        )['iq']


    def remove_all_names(self, id_num):
        id_num = str(id_num)
        self.names.update_one({'id': id_num}, )
        return

    def get_nickname(self, id_num, original):
        id_num = str(id_num)
        nicknames = self.list_names(id_num)
        nickname = False
        if len(nicknames) < 2:
            if len(nicknames) == 0:
                return original
            return nicknames[0]
        while nickname == False or nickname == original:
            nickname = choice(nicknames)
        return nickname 

    def remove_nickname(self, id_num, nickname):
        id_num = str(id_num)
        if nickname.isdigit():
            nickname = int(nickname)
            nickname = self.list_names(id_num)[nickname-1]
        self.archive_names(id_num, [nickname])

    def add_nickname(self, id_num, nickname):
        id_num = str(id_num)
        nickname = nickname.strip()
        if len(nickname) > 32:
            return f"Error: nickname '{nickname}' is longer than 32 characters!"

        elif len(nickname) < 1:
            return f"Error: no nickname given. Try `/addname name`"

        matches = self.names.find({'id': id_num, 'nickname': nickname})
        if matches.count() > 0:
            for match in matches:
                if not match['archived']:
                    return f"Error: nickname '{nickname}' already exists!"
                else:
                    self.archive_names(id_num, [nickname], archive=False)
                    return f"Successfully restored nickname: '{nickname}'!"
        post_data = {
            "nickname": nickname,
            "id": id_num,
            "archived": False,
        }
        self.names.insert_one(post_data)
        return f"Successfully added nickname '{nickname}' to <@{id_num}>'s user bank."

    def archive_names(self, id_num, nicknames, archive = True):
        id_num = str(id_num)
        if nicknames == None:
            self.names.update_many({'id': id_num},{'$set': {"archived": archive}})
        for nickname in nicknames:
            self.names.update_one({'id': id_num, 'nickname': nickname}, 
                {'$set': {"archived": archive}})


    def list_names(self, id_num, query = "default"):
        id_num = str(id_num)
        nicknames = self.names.find({'id': id_num})
        name_list = []
        for index, nickname in enumerate(nicknames):
            if( 
                query == "default" and not(nickname["archived"]) or
                query == "archived" and nickname["archived"] or
                query == "all"
            ):
                name_list.append(nickname['nickname'])
        return name_list


    def pprint_names(self, id_num, query = "default"):
        id_num = str(id_num)
        names = self.list_names(id_num, query)
        name_list = f"Name list for <@{id_num}>:\n"
        for index in range(len((names))):
            name_list += f"{index + 1}. {names[index]}\n"

        return name_list

    def count_nicknames(self):
        return self.names.count()
    
    def clear_iq(self):
        self.iqs.drop()

    def backup(self, db_path=os.path.join(os.path.dirname(__file__), 'database')):
        self.client.fsync(lock=True);
        subprocess.call(['git', '-C', db_path, 'add', '*'])
        subprocess.call(['git', '-C', db_path, 'commit', '-m', 
            f'{self.count_nicknames()} saved nicknames'])
        self.client.unlock()
        

db = DB_Client()
test_db = DB_Client(test=True)

if __name__ == "__main__":
    print(db.list_iqs())
