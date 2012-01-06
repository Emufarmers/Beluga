import sys, json, string, time, thread

while True:
    time.sleep(1)
    next_line = sys.stdin.readline()
    if next_line:
        data = json.loads(next_line)

        if data['method'] == 'user_joined':    
            out = {'do' : 'me', 'msg' : 'swims by %s' % data['user'].split("!",1)[0], 'channel' : data['channel']}
            out = json.dumps(out)
            sys.stdout.write("%s" % out)
            sys.stdout.flush()
            
        sys.stdout.write("\n")
        sys.stdout.flush()

