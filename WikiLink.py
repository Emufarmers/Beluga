import string, re
from BasicPlugin import BasicPlugin

class WikiLink(BasicPlugin):
  
  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.
    m = re.match("\[\[(.*?)\]\]", msg)
    if m:
      self.IRC.msg(channel, "http://en.wikipedia.org/wiki/" + m.group(1))
    return
