#!./env/bin/python
# -*- coding: utf-8 -*-
import asyncio
from telethon.tl.types import User
import mysql.connector
from telethon import TelegramClient,events
from telethon.sessions import StringSession
import time
mydb = mysql.connector.connect(
    host="telegramdata.cxh7xkivqcfs.us-east-1.rds.amazonaws.com",
    user="vrushang",
    passwd="root091098",
    database="telegramdata"
)
mycursor = mydb.cursor()

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

api_id = "162650"
api_hash = "1851642d6022571a418fbf25b4eda34e"

loop = asyncio.get_event_loop()

# sign in
print("Signing in users...")

# path = "./sessions/bulk/"
# # sessions_files = [f for f in listdir(path) if isfile(join(path, f))]
# sessions_files = ["default"]
get_session = "SELECT session FROM promoters"
insert_query = "INSERT INTO scraped_users (id, username) VALUE (%s,%s) "

mycursor.execute(get_session)
sessions_files = mycursor.fetchall()

async def main():
    clients = []
    for session_file in sessions_files:
        client = TelegramClient(StringSession(string=session_file[0]), api_id, api_hash)
        await client.start()
        print(client.session.dc_id)
        print(client.session.auth_key.key.hex())
        clients.append(client)

    for client in clients:

        try:
            me = await client.get_me()
            me = me.first_name
            print("Signed in as : ", me)
            print("Trying To Unban")


            bot = await client.get_entity("t.me/SpamBot")
            me = await client.get_entity("t.me/whalehulk")
            await client.send_message(me, "/start")
            await client.send_message(bot, "/start")
            # await client.get
            @ client.on(events.NewMessage(chats=('SpamBot', 'whalehulk')))

            async def new_msg(event):
                client = event.client
                print(event.raw_text)
                if "Good news, no limits are currently applied to your account. You’re free as a bird!" in event.raw_text:
                    print("Already Unbanned !")
                    await client.send_message(me, "Cool,thanks")


        except Exception as e:
            print(e)
            pass







if __name__=='__main__' :
    loop.run_until_complete(main())