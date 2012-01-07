import string, re, urllib
from BasicPlugin import BasicPlugin

class WikiLink(BasicPlugin):
  
  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.
    m = re.match("\[\[(.*?)\]\]", msg)
    if m:
      self.IRC.msg(channel, "http://en.wikipedia.org/wiki/" + urllib.quote(string.replace(m.group(1)," ", "_")))
      return
    
    m = re.match("\{\{(.*?)\}\}", msg)
    if m:
      self.IRC.msg(channel, "http://en.wikipedia.org/wiki/Template:" + urllib.quote(string.replace(m.group(1)," ", "_")))
      return
      
    return
