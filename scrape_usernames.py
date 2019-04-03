#!./env/bin/python
# -*- coding: utf-8 -*-
import asyncio

import telethon
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
import logging
from telethon import TelegramClient
from telethon.tl.types import UserStatusOffline, UserStatusOnline
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep
import csv
from telethon.errors.rpcerrorlist import PeerFloodError, UserNotMutualContactError, UserPrivacyRestrictedError, FloodWaitError
from telethon.tl.types import UserStatusOffline, UserStatusOnline
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.channels import EditAdminRequest
from time import sleep
from os import listdir
from os.path import isfile, join
import time
import datetime
import json
import random
import sys
from telethon.sessions import StringSession
import pytz
import mysql.connector
utc=pytz.UTC

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
        clients.append(client)
        me = await client.get_me()
        me = me.first_name
        print("Signed in as : ",me)
    # # input
    #
    groupname ="t.me/jlsaj"
    # input("Enter Group Name To Scrape ? :   ")

    channels = []
    for client in clients:
        print((await client.get_me()).first_name)
        channels.append(await client.get_entity(groupname))
        print((await client.get_entity(groupname)))

    # join

    print("joining channel...")
    for client, channel in zip(clients, channels):
        client_name =(await client.get_me()).first_name
        print(client_name," Is Joining :    ",channel.title)
        await client(JoinChannelRequest(channel))
        print(client_name," Joined ",channel.title)
    # # get info
    #
    # ans = clients[0](GetFullChannelRequest(channels[0]))
    # filename = "{}.csv".format(
    #     ''.join(e for e in ans.chats[0].title if e.isalnum()) or "data")


    # get participants






    print("fetching members...")

    participantss = []

    i = 0
    for client,channel in zip(clients,channels):
        print("fetching with account {}/{}".format(i + 1, len(clients)))
        participantss.append(await client.get_participants(channel, aggressive=True))
        i += 1

    print(len(participantss))
    print("saving...")


    for user in participantss[0]:
        try:
            i=1
            user_status_time = user.status.was_online + datetime.timedelta(hours=20)
            now = datetime.datetime.utcnow().astimezone(utc)
            active = user.status is not None and (type(user.status) is UserStatusOffline and  user_status_time > now or type(user.status) is UserStatusOnline)
            if active :
                try:
                    print("Actice User Found ...")
                    val = (user.id, user.username,1)
                    print("Sending Msg Too ... :  ",val[1])

                    sel = random.randint(0,(len(clients)+1))
                    client = clients[sel]
                    await client.send_message(user ,"hi mate :)")

                    mycursor.execute(insert_query, val)

                    mydb.commit()
                    # temp_dict = dict()
                    # temp_dict['_id'] = user.id
                    # temp_dict['username'] = user.username
                    # # temp_dict['access_hash'] = user.acess_hash


                except PeerFloodError as e:
                    print("This account can't invite any more users :(")
                    sys.exit(1)
                except FloodWaitError as e:
                    print(e)
                    time = int(str(e).split()[3])
                    time.sleep(time)
                except Exception as e:
                    print(e)
                    print(e)
                    print("other problems")
                    pass
        except Exception as e:
            print(e)
            pass

if __name__=='__main__' :
    loop.run_until_complete(main())