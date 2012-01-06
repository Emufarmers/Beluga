import sys, json, string, time, thread, re, urllib2

while True:
    time.sleep(1)
    next_line = sys.stdin.readline()
    if next_line:
        data = json.loads(next_line)
        
        m = 0
        page = 0
        text = 0

        if data['method'] == 'privmsg':    
            m = re.match("(https?\:\/\/.*?)(\s|$)",data['msg'])
            if m:
                page = urllib2.urlopen(m.group(1))
                text = string.replace(page.read(4096),"\n", "")
                m = re.search("<title>(.*?)</title>", text)
                if m:
                    out = {'do' : 'msg', 'msg' : 'title: %s' % ' '.join(m.group(1).split()), 'channel' : data['channel']}
                    out = json.dumps(out)
                    sys.stdout.write("%s" % out)
                    sys.stdout.flush()
            
        sys.stdout.write("\n")
        sys.stdout.flush()