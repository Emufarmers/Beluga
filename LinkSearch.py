import string, re, urllib2
from urllib2 import Request, urlopen, URLError
from BasicPlugin import BasicPlugin

class LinkSearch(BasicPlugin):
  
  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.   
    m = re.match("(https?\:\/\/.*?)(\s|$)", msg)
    if m:
      text = ""
      try: page = urllib2.urlopen(m.group(1))
      except URLError, e:
        self.IRC.me(channel,'couldn\'t find ' + m.group(1))
        return
      if page: text = page.read(4096)
      text = string.replace(text,"\n", "")
      m = re.search("<title>(.*?)</title>", text)
      if m:
        self.IRC.msg(channel,'title: %s' % ' '.join(m.group(1).split()))
    return
