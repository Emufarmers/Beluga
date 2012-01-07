import string, thread, time
from twisted.internet import reactor
from BasicPlugin import BasicPlugin

class TickTest(BasicPlugin):
  def tick(self):
    while self.still_running:
      reactor.callInThread(self.IRC.me, self.IRC.factory.channel, "makes a ticking noise")
      time.sleep(5)
    return
  
  def __init__(self, IRC):
    BasicPlugin.__init__(self, IRC)
    self.still_running = True
    reactor.callInThread(self.tick)
    
  
  def teardown(self):
    self.still_running = False
    print "rawrrrrr"
  
  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.
    if string.lower(self.IRC.nickname) in string.lower(msg):
      self.IRC.me(channel, "snuggles %s" % user.split("!",1)[0])
    return
