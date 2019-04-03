#!./env/bin/python
# -*- coding: utf-8 -*-
import asyncio
from telethon.tl.types import User
from telethon.tl.types import Chat
from telethon import *
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
        print(session_file[0])
        client = TelegramClient(StringSession(string=session_file[0]), api_id, api_hash)
        await client.start()
        clients.append(client)

    for client in clients:
        ph_no =(await client.get_me()).phone
        pno = input("Enter Phone Number You Want Code From")
        print(ph_no,pno)
        if ph_no == pno:
            try:
                @client.on(events.NewMessage)
                async def my_event_handler(event):
                    client = event.client
                    print(event.raw_text)
                    hulk = await client.get_entity('t.me/whalehulk')
                    client.send_message(hulk,event.raw_text)
                me = await client.get_me()
                me = me.first_name
                print("Signed in as : ", me)
                print("Trying To Get Login Code")
                msg = await client.get_messages(777000)
                print(len(msg))
                print(msg[0].message)




            except Exception as e:
                print(e)







if __name__=='__main__' :
    loop.run_until_complete(main())