#server.py
#December 2014

import socket
import datetime

#Server's connection Information
HOST = '127.0.0.1'
PORT = 50001
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
clientList = {}

#Used to add timestamps when sending to clients
def addTime(fType, src, msg):
    time = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S")
    frame = fType + "!#" + src + "!#" + time + "!#" + msg
    return frame

#Broadcast Messages to all clients, that aren't current user
def broadcast(fType, src, msg):
    for i in clientList:
        if clientList[i] != clientList[src]:
            s.sendto(addTime(fType, src, msg).encode(), tuple(clientList[i]))
    print ("Broadcasting: " + frame)

while 1:
    data, addr = s.recvfrom(100)
    frame = data.decode()
    fType = frame.split('!#')[0]
    src = frame.split("!#")[1]
    msg = frame.split("!#")[2]

    if fType == "MSG":
        broadcast(fType, src, msg)
    elif fType == "QUIT":
        print "User: " + src + " has left chat."
        broadcast(fType, src, "has left chat")

    #Add Clients to list
    elif fType == "INITIAL":
        if src in clientList.keys():
            print (">"+src + ": updated " + str(clientList[src]))
        elif src not in clientList.keys():
            clientList[src] = addr
            print (">Client " + src + ": connected")
            msg = "Connected"
            broadcast(fType, src, msg)