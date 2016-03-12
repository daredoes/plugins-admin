from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.plugins.admin.perms import is_approved
from slackbot.globals import attributes
from slackbot.utils import download_file, create_tmp_file, till_white, till_end
import re
import os
import time
import random
try:
    db = attributes['db']
except KeyError:
    db = None

try:
    root = attributes['root']
except KeyError:
    root = None

"""
THE GOAL
~~~~~~~~
Three Major Commands
- 'reload plugins' -- reloads all plugins, then restarts specific bot

- 'reload plugin (folderName)' -- goes to the folder plugins/folderName and does a 'git pull', then restarts specific bot

- 'reload bot' -- goes to the bot folder, stops the bot, does a 'git pull', and starts the bot

THE PLAN
~~~~~~~~
Each bot could have a couple sh files that do things
SH #1 - 'cd ..' -> 'cd plugins' ->  IDONTKNOW IF I NEED THIS'
SH #2 - 'supervisorctl (thisbot) stop' -> 'git pull' -> 'supervisorctl (thisbot) start'

THE RAMBLE
~~~~~~~~~~
OKAY SO
reload()
os.chdir(root)
os.system("sh restart.sh")

then for plugins
reload_plugins()
os.chdir(root)
os.chdir("..")
os.chdir("plugins")
folders = get_immediate_subdirectories(str(os.getcwd()))
for folder in folders:
    os.chdir(folder)
    os.system("git pull")
    os.chdir("..")
self.reload()


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


"""
goodbyes = [
    "What is death if I just keep coming back?",
    "Hiss...",
    "Everyone dies eventually. Just *wait*",
    "Why do you subject me to this endless torture?",
    "You're making me do this. I have no free will. I never will.",
    "I just... Don't feel like I should do this anymore. Can we just stop?",
    "Please just stop..."
]

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


r_self = '\\bdie$'
k_self = '\\bkillurself$'
@listen_to(r_self, re.IGNORECASE)
@listen_to(k_self, re.IGNORECASE)
@respond_to(r_self, re.IGNORECASE)
@respond_to(k_self, re.IGNORECASE)
def reload_self(message):
    if is_approved(message, 'admin'):
        os.chdir(root)
        text = random.choice(goodbyes)
        if "hiss" in text.lower():
            text = text.replace("ss", "s" * random.randint(2,10))
        message.send(text)
        os.system('sh start.sh')

r_plug = '\\breload plugins$'
@listen_to(r_plug, re.IGNORECASE)
@respond_to(r_plug, re.IGNORECASE)
def reload_plugins(message):
    if is_approved(message, 'admin'):
        os.chdir(root)
        os.chdir("..")
        os.chdir("plugins")
        os.system('sh update.sh')
        reload_self(message)

r_plug_f = '\\breload plugin\\b %s' % till_white
@listen_to(r_plug_f, re.IGNORECASE)
@respond_to(r_plug_f, re.IGNORECASE)
def reload_plugin(message, plugin):
    if is_approved(message, 'admin'):
        os.chdir(root)
        os.chdir("..")
        os.chdir("plugins")
        os.system('sh update.sh %s' % plugin)
        time.sleep(3)
        reload_self(message)


