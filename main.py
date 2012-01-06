# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys, json, subprocess, thread, re

class BelugaBot(irc.IRCClient):
    
    nickname = "BelugaBot"
    ns_user = "TuskBot"
    password = "rawr"
    admin_list = ["wikipedia/The-Earwig", "wikipedia/RandomStringOfCharacters"]
    modules = dict()
    
    def parse_response(self, output):
        if output == "\n":
            return
        print output
        output = json.loads(output)
      
        if output['do'] == "me":
            self.me(output['channel'].encode('ascii','ignore'), output['msg'].encode('ascii','ignore'))
        elif output['do'] == "msg":
            self.msg(output['channel'].encode('ascii','ignore'), output['msg'].encode('ascii','ignore'))
        
    def send_data(self, data):
        data = json.dumps(data)
        
        for k, v in self.modules.iteritems():
            v.stdin.write('%s\n' % data)
            output = v.stdout.readline()
            self.parse_response(output)
            
    def tick(self):
        self.send_data({'method' : 'tick', 'channel' : self.factory.channel})
            
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.msg("nickserv", "identify %s %s" % (self.ns_user, self.password))
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        print msg
        
        host = user.split('@',1)[1] if ('@' in user) else ""
        
        if host in self.admin_list:
          if msg.startswith(self.nickname + ": !load"):
              user = user.split('!', 1)[0]
              module = msg.split(':', 2)[2]
              if module in self.modules:
                msg = "can't load %s twice" % module
                self.me(channel, msg)
              else:
                self.modules[module] = subprocess.Popen('python %s.py' % module, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                msg = "has loaded %s" % module
                self.me(channel, msg)
              return
          elif msg.startswith(self.nickname + ": !unload"):
              user = user.split('!', 1)[0]
              module = msg.split(':', 2)[2]
              if module in self.modules:
                temp = self.modules[module]
                del self.modules[module]
                temp.kill()
                msg = "has unloaded %s" % module
                self.me(channel, msg)
              else:
                msg = "isn't running %s" % module
                self.me(channel, msg)
              return
            
        data = {'method' : 'privmsg', 'nick' : self.nickname, 'user' : user, 'channel' : channel, 'msg' : msg}
        self.send_data(data)

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        data = {'method' : 'action', 'nick' : self.nickname, 'user' : user, 'channel' : channel, 'msg' : msg}
        self.send_data(data)

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        data = {'method' : 'irc_nick', 'nick' : self.nickname, 'prefix' : prefix, 'params' : params}
        self.send_data(data)


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'

p = BelugaBot()

def tick():
  while True:
    time.sleep(3)
    p.tick()

class BelugaBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        #p = BelugaBot()
        p.factory = self
        thread.start_new_thread(tick,())
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # create factory protocol and application
    f = BelugaBotFactory("##earwig")

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
