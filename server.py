#server.py
#December
import socket
import time
import datetime


#Server's connection Information
HOST = ''
PORT = 40007
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
clientList = {}     # Empty Client

def addTime(type,src,msg):
    time = datetime.datetime.strftime(datetime.datetime.now(),"%H:%M:%S")
    frame = type+"#"+src+"#"+time+"#"+msg
    return frame

def broadcast(type,src,msg):
    for i in clientList:
        if clientList[i] != clientList[src]:
            s.sendto(addTime(type,src,msg).encode(), tuple(clientList[i]))
        print ("Broadcasting: " + frame)

while (1):
    data, addr = s.recvfrom(100)
    frame = data.decode()
    type = frame.split('#')[0]
    src = frame.split("#")[1]
    msg = frame.split("#")[2]

    if type == "MSG":
        broadcast(type,src,msg)
    elif type == "QUIT":
        print "User: " + src+ " has left chat."
        broadcast(type,src,"has left chat")
    elif type == "INITIAL":
        if src in clientList.keys():
            print (">"+src + ": updated " + str(clientList[src]))
        elif src not in clientList.keys() :
            clientList[src] = (addr)
            print (">Client " + src + ": connected")
            msg = "Connected"
            broadcast(type,src,msg)
