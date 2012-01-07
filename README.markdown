Beluga
------
A (modular) Python IRC Bot Framework

Setup
-----
1. Make secure_config.py
    cp secure_config.py.example secure_config.py
1. Fill out the settings in secure_config.py
1. Note that conf_plugins are loaded just before joining the channel
1. Start bot with:
    python main.py
  
Notes
-----
Due to how Twisted works, any plugins that start other reactor services should not be reloaded with !reload, but instead !unload and then !load.

Plugins
-------
A plugin should subclass BasicPlugin and override the methods that it needs.
  
For example the simple "PingBack" plugin:

  import string
  from BasicPlugin import BasicPlugin

  class PingBack(BasicPlugin):
  
    def privmsg(self, user, channel, msg):
      #This will get called when the bot receives a message.
      if string.lower(self.IRC.nickname) in string.lower(msg):
        self.IRC.me(channel, "snuggles %s" % user.split("!",1)[0])
      return