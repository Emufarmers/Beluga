class BasicPlugin:
  def __init__(self, IRC):
    # own the IRC client!
    self.IRC = IRC
  
  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.
    return False
    
  def action(self, user, channel, msg):
    #This will get called when the bot sees someone do an action.
    return False

  def userJoined(self, user, channel):
    #This will get called when the bot sees someone join a channel.
    return false
    
  def irc_NICK(self, prefix, params):
    #Called when an IRC user changes their nickname.
    return False