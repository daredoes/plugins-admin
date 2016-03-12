from slackbot.globals import attributes

try:
    db = attributes['db']
except KeyError:
    db = None

def is_approved(message, permission="any"):
      try:
          sent_user_id = message._body['user']
          if permission == "any":
              try:
                  if 'none' in db.users.find({'id':sent_user_id})[0]['permissions'].split(","):
                      message.send("User is not allowed to use commands.")
                      return False
                  else:
                      return True
              except IndexError:
                  return True
          if db.users.count({'id':sent_user_id} != 0):
              if 'admin' in db.users.find({'id':sent_user_id})[0]['permissions'].split(","):
                  return True
              elif permission in db.users.find({'id':sent_user_id})[0]['permissions'].split(","):
                  return True
              else:
                  message.send("User does not have sufficient permissions.")
                  return False
          else:
              message.send("User does not have sufficient permissions.")
              return False
      except IndexError:
          message.send("User does not have sufficient permissions.")
          return False
      except KeyError:
          message.send("You're a bot! NICE TRY")
          return False
