#!/usr/bin/python

import errno, socket, time

mylist = []

for i in range(50000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.connect(('127.0.0.1', 5000))
    except socket.error as e:
        if e.errno == errno.EINPROGRESS:
            pass
        else:
            raise
    mylist.append(s)

print "sockets opened"

while True:
   time.sleep(1)
