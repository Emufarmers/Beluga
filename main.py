# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys, json, subprocess, thread, re, BasicPlugin
from secure_config import *

class BelugaBot(irc.IRCClient):
    
    nickname = NS_NICK
    ns_user = NS_USER
    password = NS_PASSWORD
    admin_list = NS_ADMINS
    modules = dict()
    plugins = dict()
           
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
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
              plugin = msg.split(':', 2)[2]
              if plugin in self.modules:
                msg = "can't load %s twice" % plugin
                self.me(channel, msg)
              else:
                self.modules[plugin] = __import__(plugin)
                exec("self.plugins[plugin] = self.modules[plugin].%s(self)" % plugin)
                msg = "has loaded %s" % plugin
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
              
          for k, v in self.plugins:
            v.privmsg(user, channel, msg)

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'

p = BelugaBot()

class BelugaBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        #p = BelugaBot()
        p.factory = self
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
