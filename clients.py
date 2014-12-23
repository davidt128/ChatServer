import socket
import threading
import time
import sys

#Server Connection Information
HOST = '127.0.0.1'
PORT = 40007
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(False)


def sendMsg(type, src, msg):
    msg = type + "#" + src  + "#" + msg
    return msg

def recMsgs():
    while 1:
        data = None
        try:
            data,addr = s.recvfrom(100)
        except:
            time.sleep(0.1)
        if data:
            try:
                type = data.split("#")[0]
                src = data.split("#")[1]
                ctime = data.split("#")[2]
                msg = data.split("#")[3]
                print "[" +ctime + "]" + src + ": " + msg
            except:
                print "no data"

#Prompt User
client = raw_input("Username: ")
print("Welcome: '" + client + "' type '!q' to quit")
iMsg = sendMsg("INITIAL",client,"")
s.sendto(iMsg.encode(),(HOST, PORT))

t1 = threading.Thread(name='recMsgs', target=recMsgs)
t1.setDaemon(True)
t1.start()

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

