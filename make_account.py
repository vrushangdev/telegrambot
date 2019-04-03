from telethon import TelegramClient, sync
import requests
import json
import time
from telethon.sessions import StringSession, string
from telethon.tl.functions.account import UpdateUsernameRequest

import random
import mysql.connector

mydb = mysql.connector.connect(
    host="telegramdata.cxh7xkivqcfs.us-east-1.rds.amazonaws.com",
    user="vrushang",
    passwd="root091098",
    database="telegramdata"
)
mycursor = mydb.cursor()
sql = "INSERT INTO promoters (id, username, phone,session) VALUES (%s,%s,%s,%s)"

get_bal_url = "http://smspva.com/priemnik.php?metod=get_balance&service=opt29&apikey=PmwsDB2zVcVJNMWC4QeuaWYB84ZhKT"
req_num_url = "http://smspva.com/priemnik.php?metod=get_number&service=opt29&apikey=PmwsDB2zVcVJNMWC4QeuaWYB84ZhKT&country=RU"
get_sms_url = "http://smspva.com/priemnik.php?metod=get_sms&service=opt29&apikey=PmwsDB2zVcVJNMWC4QeuaWYB84ZhKT&country=RU&id={}"

resp_bal = requests.get(get_bal_url)
curr_bal = json.loads(resp_bal.text)
print("Your Current Balance Is : " + curr_bal['balance'])

resp_num = requests.get(req_num_url)
curr_num = json.loads(resp_num.text)
print("Your Current Number Is : " + str(curr_num['CountryCode']) + str(
    curr_num['number']) + "id found :    " + str(curr_num['id']))
time.sleep(20)
idnum = curr_num['id']
print(idnum)


def get_code(idnum):
    curr_sms = requests.get(get_sms_url.format(idnum))
    curr_sms = json.loads(curr_sms.text)
    curr_sms_text = curr_sms['sms']
    if curr_sms_text == "null":
        get_code(idnum)
    else:
        return curr_sms_text


api_id = "162650"
api_hash = "1851642d6022571a418fbf25b4eda34e"
name = str(curr_num['number'])
phone_number = str(curr_num['CountryCode'] + curr_num['number'])
print(phone_number)

client = TelegramClient("./sessions/bulk/session_{}".format(phone_number), api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone_number, force_sms=True)
    time.sleep(30)
    code = get_code(idnum)
    name = "TradingWiz" + str(random.randint(1, 500))
    client.sign_up(
        code=code,
        first_name=name,
        last_name=name,
    )
    me = client.sign_in(phone_number, code)
    string = StringSession.save(client.session)
    client(UpdateUsernameRequest(name))

    myself = client.get_me()
    id = myself.id
    username = myself.username
    phone = myself.phone
    session = str(string)
    val = (id, username, phone, session)
    mycursor.execute(sql, val)
    mydb.commit()

print(curr_num['number'])
