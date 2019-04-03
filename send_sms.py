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

api_id = "162650"
api_hash = "1851642d6022571a418fbf25b4eda34e"

loop = asyncio.get_event_loop()

# sign in
print("Signing in users...")
get_session = "SELECT session FROM promoters"
get_users = "SELECT username FROM scraped_users WHERE msg_sent=0"

mycursor.execute(get_session)
sessions_files = mycursor.fetchall()
mycursor.execute(get_users)
users = mycursor.fetchall()
async def main():
    try:
        clients = []

        for session_file in sessions_files:

            client = TelegramClient(StringSession(string=session_file[0]), api_id, api_hash)
            await client.start()
            print("Logged In As :   ",(await client.get_me()).first_name)
            clients.append(client)
        print(clients)
        user_list = []
        print("Preparing To Send Message's ...")
        for client in clients:
            for user in users:
                print(user[0])
                user = await client.get_entity("whalehulk")
                id = 653673167
                await client.send_message(user ,"hi ,How Are You ? :) ")
                user_list.append(user)

            print(clients)
    except PeerFloodError as e:
        print("This account can't invite any more users :(")
        sys.exit(1)
    except FloodWaitError as e:
        print(e)
        time = int(str(e).split()[3])
        sleep(time)
    except Exception as e:
        print(e)
        print(e)
        print("other problems")
        pass

if __name__=='__main__' :
    loop.run_until_complete(main())