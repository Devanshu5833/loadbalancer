#!/usr/bin/env python

'''
Filename : loadbalancer.py
purpouse : create a server socket and receives incomming messges
'''

#import core modules
import socket
import sys
import json
import select

#import extra modules
try :
    data = {
        "configuration": {
            "/socket3": {
                "host": "127.0.0.1",
                "port": 3003
            },
            "/socket4": {
                "host": "127.0.0.1",
                "port": 3004
            }
        }
    }

    config = data['configuration']
    servers = []

    for key,value in config.items(): 
        server = socket.socket()
        host = value['host']
        port = value['port']
        server.bind((host,port))
        server.listen(5)
        print 'start listening {"host" : ' + host + ', "port" :' +  str(port) + '}' 
        servers.append(server)

    while True:
        readable,_,_ = select.select(servers, [], [])
        ready_server = readable[0]
        connection, address = ready_server.accept()
        enddata = connection.recv(4096)
        print enddata
        connection.send("Done url > " + enddata )

except :
    print "Something went to wrong Try again ...."