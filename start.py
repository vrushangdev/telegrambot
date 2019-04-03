#!./env/bin/python
# -*- coding: utf-8 -*-
import logging
from telethon import TelegramClient,sync
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep

import os
from telethon.sessions import StringSession
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
import mysql.connector

mydb = mysql.connector.connect(
    host="telegramdata.cxh7xkivqcfs.us-east-1.rds.amazonaws.com",
    user="vrushang",
    passwd="root091098",
    database="telegramdata"
)
mycursor = mydb.cursor()
sql ="INSERT INTO promoters (id, username, phone,session) VALUES (%s,%s,%s,%s)"

api_id = "162650"
api_hash = "1851642d6022571a418fbf25b4eda34e"
while True:
    print("What do you want to do?")
    cmd = input("[l=login new account, i=import user to a channel, e=exit] :")

    if cmd == 'l':
        phone_number = input("Enter a phone number: ")

        client = TelegramClient("./sessions/bulk/session_{}".format(phone_number), api_id, api_hash).start()
        string = StringSession.save(client.session)
        print(string)
        me=client.get_me()
        # print(me.stringify())

        id = me.id
        username = me.username
        phone = me.phone
        val = (id,username,phone,str(string))
        try:

            mycursor.execute(sql,val)
            mydb.commit()
        except Exception as e:
            print(e)
            pass
        print("Entered Into Database !")

    elif cmd == 'i':
        if os.name == 'nt':
            # windows
            os.system('get_and_add_users.bat')
        else:
            os.system('./get_and_add_users.py')

    elif cmd == 'e':
        exit()

    else:
        print("Unkown command")
