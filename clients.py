#server.py
#December 2014

import socket
import threading
import time
import sys

#Server Connection Information
HOST = '127.0.0.1'
PORT = 50001
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(False)

#Used to send Messages to Server
def sendMsg(fType, src, msg):
    msg = fType + "!#" + src + "!#" + msg
    return msg


#Runn on separate thread to receive messages
#If no data, sleep
#If there is Data print out
def recMsgs():
    while 1:
        data = None
        try:
            data,addr = s.recvfrom(100)
        except:
            time.sleep(0.1)
        if data:
            try:
                src = data.split("!#")[1]
                curtime = data.split("!#")[2]
                msg = data.split("!#")[3]
                print "[" +curtime + "]" + src + ": " + msg
            except:
                print "no data"

#Prompt User and send name to Server
client = raw_input("Username: ")
print("Welcome: '" + client + "' type '!q' to quit")
iMsg = sendMsg("INITIAL",client,"")
s.sendto(iMsg.encode(),(HOST, PORT))

#Start thread for listening
t1 = threading.Thread(name='recMsgs', target=recMsgs)
t1.setDaemon(True)
t1.start()

#Grab messages and quit appropriately
while 1:
    msg = raw_input("").strip()
    if msg == "!q":
        print "You have Left Chat"
        msg = sendMsg("QUIT",client,msg)
        s.sendto(msg.encode(),(HOST, PORT))
        s.close()
        sys.exit()
    else:
        msg = sendMsg("MSG",client,msg)
        s.sendto(msg.encode(),(HOST, PORT))

