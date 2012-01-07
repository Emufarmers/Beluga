# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys, json, subprocess, thread, re, BasicPlugin, os
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
        for plugin in CONF_PLUGINS:
            modules[plugin] = __import__(plugin)
            exec("plugins[plugin] = modules[plugin].%s(self)" % plugin)
            
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
              if plugin == "BasicPlugin": return
              if not os.path.isfile(plugin + ".py"): return
              if plugin in self.plugins:
                msg = "can't load %s twice" % plugin
                self.me(channel, msg)
              else:
                if not plugin in self.modules:
                  self.modules[plugin] = __import__(plugin)
                else:
                  reload(self.modules[plugin])
                exec("self.plugins[plugin] = self.modules[plugin].%s(self)" % plugin)
                msg = "has loaded %s" % plugin
                self.me(channel, msg)
              return
          elif msg.startswith(self.nickname + ": !unload"):
              user = user.split('!', 1)[0]
              plugin = msg.split(':', 2)[2]
              if plugin == "BasicPlugin": return
              if not os.path.isfile(plugin + ".py"): return
              if plugin in self.plugins:
                temp = self.modules[plugin]
                self.plugins[plugin].teardown()
                self.plugins.pop(plugin)
                msg = "has unloaded %s" % plugin
                self.me(channel, msg)
              else:
                msg = "isn't running %s" % plugin
                self.me(channel, msg)
              return
          elif msg.startswith(self.nickname + ": !reload"):
              user = user.split('!', 1)[0]
              plugin = msg.split(':', 2)[2]
              if plugin == "BasicPlugin" or plugin == "GitPost": return
              if not os.path.isfile(plugin + ".py"): return
              if plugin in self.plugins:
                temp = self.modules[plugin]
                self.plugins[plugin].teardown()
                self.plugins.pop(plugin)
                time.sleep(1)
                reload(self.modules[plugin])
                exec("self.plugins[plugin] = self.modules[plugin].%s(self)" % plugin)
                msg = "has reloaded %s" % plugin
                self.me(channel, msg)
              else:
                msg = "isn't running %s" % plugin
                self.me(channel, msg)
              return
              
          for k, v in self.plugins.iteritems():
              if v.privmsg(user, channel, msg): return

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        for k, v in self.plugins.iteritems():
            if v.action(user, channel, msg):
                return 
                
    def userJoined(self, user, channel):
        """This will get called when the bot sees someone join a channel."""
        for k, v in self.plugins.iteritems():
            if v.userJoined(user, channel):
                return
    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        for k, v in self.plugins.iteritems():
            if v.irc_NICK(prefix, params):
                return

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
    f = BelugaBotFactory(CHANNEL)

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
