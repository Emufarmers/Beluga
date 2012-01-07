Beluga
======
A (modular) Python IRC Bot Framework

Setup
-----
* Make secure_config.py

>cp secure_config.py.example secure_config.py

* Fill out the settings in secure_config.py
* Note that conf_plugins are loaded just before joining the channel
* Start bot with:

>python main.py
  
Notes
-----
Any plugins that start other reactor services (for instance, GitPost) should not be reloaded with !reload, but instead !unload and then !load.

Plugins
-------
A plugin should subclass BasicPlugin and override the methods that it needs.
  
For example the simple "PingBack" plugin:

```python
import string
from BasicPlugin import BasicPlugin

class PingBack(BasicPlugin):

  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.
    if string.lower(self.IRC.nickname) in string.lower(msg):
      self.IRC.me(channel, "snuggles %s" % user.split("!",1)[0])
    return
```