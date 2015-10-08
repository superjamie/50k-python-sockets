#!/usr/bin/python

import errno, os, socket, select, sys, time

if not "EPOLLRDHUP" in dir(select):
    select.EPOLLRDHUP = 0x2000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

mylist = []

try:
    s.bind(('', 5000))
except socket.error as e:
    print "bind failed: " + e
    sys.exit()

s.listen(50000)

epoll = select.epoll()
# events = epoll.poll(1)

while True:
    try:
        conn, addr = s.accept()
        epoll.register(conn.fileno(), select.EPOLLIN | select.EPOLLRDHUP)
        mylist.append(conn)
    except socket.error as e:
        if e.errno == errno.EAGAIN:
            pass
        else:
            raise
    
    events = epoll.poll(1)
    for fileno, event in events:
        if event & select.EPOLLRDHUP:
            epoll.unregister(fileno)
            os.close(fileno)
