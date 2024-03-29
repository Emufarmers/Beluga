import string
from secure_config import *
from BasicPlugin import BasicPlugin

class Say(BasicPlugin):
  
  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.
    if string.lower(self.IRC.nickname) in string.lower(channel):
      host = user.split('@',1)[1] if ('@' in user) else ""
      if host in NS_ADMINS:
        self.IRC.msg(self.IRC.factory.channel, msg)
    return
