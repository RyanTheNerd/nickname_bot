from database import db

for nickname in db.names.find():
    print("Nickname: {:<32} User: {:>18}".format(nickname['nickname'], nickname['id']))



