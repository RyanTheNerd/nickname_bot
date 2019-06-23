from database import db
from discord import Client
import config

async def genStatsHTML(client, db, path, close=False):
    users = {}
    for nickname in db.names.find():
        userid = nickname['id']
        users.setdefault(userid, [])

        userbank = users[userid]
        userbank.append(nickname['nickname'])


    html = "<!DOCTYPE html>\n<html>\n<head>\n<title>Bot Stats</title>\n"
    html += "<meta charset='UTF-8'>"
    html += "<style>body {display: flex; flex-wrap: wrap; background-color:darkblue; color: #cacaca; white-space:nowrap;} .userbox {display: block; flex: 1; margin: 10px; padding: 10px; background-color: purple;}</style>"
    html += "</head>\n<body>"

    for userid, nicknames in users.items():
        user = client.get_user(int(userid))
        if user == None:
            continue
        username = user.display_name
        userimg = user.avatar_url_as(size=128)
        html += f"<div class='userbox' style='float: left'>\n<img src='{userimg}'></img>\n<h3>Nicknames for {username}:</h3>\n"

        html += "<ul>"

        for nickname in nicknames:
            html += f"<li>{nickname}</li>"

        html += "</ul></div>"
        

    html += "</body>\n</html>"

    with open(path, 'w') as html_file:
        html_file.write(html)

    if close:
        await client.close()

client = Client()

@client.event
async def on_ready():
    await genStatsHTML(client, db, config.STATSPATH, close=True)

if __name__ == "__main__":
    client.run(config.TOKEN)
