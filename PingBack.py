import string
from BasicPlugin import BasicPlugin

class PingBack(BasicPlugin):
  
  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.
    if string.lower(self.IRC.nickname) in string.lower(msg):
      self.IRC.me(channel, "snuggles %s" % user.split("!",1)[0])
    return
