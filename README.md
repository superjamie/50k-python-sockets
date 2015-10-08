# 50k-python-sockets
A tool to open 50000 sockets in a hurry

### ABOUT

Discussing with a co-worker about the speed of `ss` when there are tens of thousands of sockets on a system, I decided to try it myself.

Starting 50000 netcats turned out to be a really bad idea, not just because of the difficulty of actually having 50000 processes running, but because `nc-1.84-24.el6` (based on [BSD Netcat](http://www.openbsd.org/cgi-bin/cvsweb/src/usr.bin/nc/)) calls `listen()` with a backlog of `1` and does not `accept()` particularly fast, so the majority of client SYNs end up ignored.

The only purpose of these sockets is to transition them to `ESTABLISHED` state, not for data transfer. The client opens sockets and appends the socket objects to a `list[]`, the server does the same then uses `epoll()` to check socket state and `close()` the socket when the client ends.

### SETUP

* Have Linux
* Increase the system-wide socket max backlog
~~~
sysctl -w net.core.somaxconn=50000
~~~
* Increase the system-wide available ephemeral ports
~~~
sysctl -w net.ipv4.ip_local_port_range="10000 61000"
~~~
* Increase the max open files in each terminal where you run the client and server
~~~
ulimit -n 262144
~~~

### RESULTS

On a not-particularly-fast RHEL6 VM:

~~~
# time ss -nlta | wc -l
100012
real    0m0.272s
user    0m0.217s
sys     0m0.055s
~~~

Adding `-p` for process name totally kills runtime, don't do that.

### AUTHORS

Jamie Bainbridge - jamie.bainbridge @ gmail.com
