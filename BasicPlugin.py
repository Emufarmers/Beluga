class BasicPlugin:
  def __init__(self, IRC):
    # own the IRC client!
    self.IRC = IRC
  
  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.
    return
    
  def action(self, user, channel, msg):
    #This will get called when the bot sees someone do an action.
    return
    
  def irc_NICK(self, prefix, params):
    #Called when an IRC user changes their nickname.
    return