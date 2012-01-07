import string, thread, time, cgi, json, urllib2, re
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from BasicPlugin import BasicPlugin

def gitio_url(url_to_shorten):
  req = urllib2.Request(url='http://git.io', data = "url=" + url_to_shorten)
  f = urllib2.urlopen(req)
  urlinfo = str(f.info())
  m = re.search("Location: (.+)\r\n?", urlinfo)
  
  if m:
    return m.group(1)
  return ""

class FormPage(Resource):
  isLeaf = True
  def __init__(self, IRC):
    Resource.__init__(self)
    self.IRC = IRC
    
  def render_GET(self, request):
    return 'Hey, you\'ve reached ' + self.IRC.nickname
  def render_POST(self, request):
    commit_info = json.loads(str(request.args["payload"][0]))
    
    number_of_commits = len(commit_info["commits"])
    commit_string = "commit" if number_of_commits == 1 else "commits"
    repo_output = "[%s] %i %s pushed to branch '%s'" % (commit_info["repository"]["name"],number_of_commits,commit_string,str(commit_info["ref"]).split("/")[2])
    
    if commit_info["before"] == "0000000000000000000000000000000000000000":
      repo_output = "[%s] %s created branch '%s' (%i %s)" % (commit_info["repository"]["name"],commit_info["pusher"]["name"] ,str(commit_info["ref"]).split("/")[2],number_of_commits,commit_string)
      
    if commit_info["after"] == "0000000000000000000000000000000000000000":
      repo_output = "[%s] %s deleted branch '%s'" % (commit_info["repository"]["name"],commit_info["pusher"]["name"] ,str(commit_info["ref"]).split("/")[2])
    
    self.IRC.msg(self.IRC.factory.channel, repo_output.encode('ascii','ignore'))
    
    for commit in commit_info["commits"]:
      output = "%s: %s (%s)" % (commit["author"]["name"], commit["message"], gitio_url(commit["url"]))
      self.IRC.msg(self.IRC.factory.channel, output.encode('ascii','ignore'))
    
    return 'beep'

class GitPost(BasicPlugin):
  
  def __init__(self, IRC):
    BasicPlugin.__init__(self, IRC)
    self.root = FormPage(IRC)
    self.factory = Site(self.root)
    self.listener = reactor.listenTCP(8880, self.factory)
    
  def teardown(self):
    print dir(self.factory)
    self.listener.stopListening()
  
  def privmsg(self, user, channel, msg):
    #This will get called when the bot receives a message.
    if string.lower(self.IRC.nickname) in string.lower(msg):
      self.IRC.me(channel, "snuggles %s" % user.split("!",1)[0])
    return
