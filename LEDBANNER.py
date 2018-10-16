#!/usr/bin/python
import socket
import time
import sys
s=socket.socket()
s.settimeout(1)
s.connect(("127.0.0.1",23735))
m = " ".join(sys.argv[1:])
s.send(m+"\n")
if "?" in m:
  buff = ""
  while '\n' not in buff:
    r = s.recv(1024)
    if not r:
       break
    buff += r
  print buff.strip()
s.close()