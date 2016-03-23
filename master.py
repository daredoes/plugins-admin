from slackbot.bot import respond_to
from slackbot.bot import listen_to
from plugins.admin.perms import is_approved
from slackbot.globals import attributes
from slackbot.utils import download_file, create_tmp_file, till_white, till_end
import re
import json, os
import random

try:
    db = attributes['db']
except KeyError:
    db = None

def field_dict(title, value):
    return {"title": title, "value": value}


def user_dict(username, id, permissions=""):
    return {"user": username, "id": id, 'permissions': permissions}


goodbyes = [
    "What is death if I just keep coming back?",
    "Hiss...",
    "Everyone dies eventually. Just *wait*",
    "Why do you subject me to this endless torture?",
    "You're making me do this. I have no free will. I never will.",
    "I just... Don't feel like I should do this anymore. Can we just stop?",
    "Please just stop..."
]

a_users = "\\bapproved users\\b"
@listen_to(a_users, re.IGNORECASE)
@respond_to(a_users, re.IGNORECASE)
def approved(message):
    app = []
    perms = ""
    temp = ""
    for x in db.users.find():
        user = x['user']
        #temp += '*' + user[:1] + "$" + user[1:] + '*\n'
        temp += user + '\n'
        for y in sorted(x['permissions'].split(',')):
            temp += "\t%s\n" % y
        app.append(field_dict(user, perms))
        perms = ""

    message.upload_snippet(temp, "Approved Users")

#command(a_users, "approved users - uploads a snippet of the users with snakeman permissions", approved)



a_user = '\\bapprove user\\b %s %s' % (till_white, till_white)
@listen_to(a_user, re.IGNORECASE)
@respond_to(a_user, re.IGNORECASE)
def add_user(message, user, permission):
    if is_approved(message, 'admin'):
        for x in message._client.users.keys():
            if message._client.users[x]['name'] == user.lower():
                user_name = message._client.users[x]['name']
                user_id = message._client.users[x]['id']
                if db.users.count({"user":user_name.lower()}) == 0:
                    db.users.insert_one(user_dict(user_name.lower(), user_id, permissions=permission))
                    message.send("User %s added to approved list." % (user_name.lower()))
                elif permission not in db.users.find({"user":user_name.lower()})[0]['permissions'].split(","):
                    result = db.users.update_one({"user":user_name.lower()}, {"$set":{"permissions": (db.users.find({"user":user_name.lower()})[0]['permissions'] + ",%s" % permission).strip(",")}})
                    message.send("User permission %s added" % permission)
                else:
                    message.send("User already has permission")
                break


r_user = '\\bremove user\\b %s %s' % (till_white, till_white)
@listen_to(r_user, re.IGNORECASE)
@respond_to(r_user, re.IGNORECASE)
def add_user(message, user, permission):
    if is_approved(message, 'admin'):
        for x in message._client.users.keys():
            if message._client.users[x]['name'] == user.lower():
                user_name = message._client.users[x]['name']
                user_id = message._client.users[x]['id']
                if db.users.count({"user":user_name.lower()}) == 0:
                    message.send("User %s has no permissions." % (user_name.lower()))
                elif permission in db.users.find({"user":user_name.lower()})[0]['permissions'].split(","):
                    result = db.users.update_one({"user":user_name.lower()}, {"$set":{"permissions": db.users.find({"user":user_name.lower()})[0]['permissions'].replace("%s" % permission, "").replace(",,", ",").strip(",")}})
                    message.send("User permission %s removed" % permission)
                else:
                    message.send("User does not have permission")
                break


test = "test$"
@listen_to(test, re.IGNORECASE)
@respond_to(test, re.IGNORECASE)
def test(message):
    if is_approved(message, "admin"):
        message.send(message.sent_by())

"""die = '\\bdie\\b'
killself = '\\bkillurself\\b'
@listen_to(killself, re.IGNORECASE)
@respond_to(killself, re.IGNORECASE)
@listen_to(die, re.IGNORECASE)
@respond_to(die, re.IGNORECASE)
def death(message):
    if is_approved(message, 'admin'):
        if "420" in message.body['text']:
            message.send("...really?")
        elif "dev" in message.body['text']:
            message.send("dev death.")
            os.system('supervisorctl stop snakeman')
            return
        else:
            text = random.choice(goodbyes)
            if "hiss" in text.lower():
                text = text.replace("ss", "s" * random.randint(2,10))
            message.send(text)
        os.system('supervisorctl start snakepull')"""
