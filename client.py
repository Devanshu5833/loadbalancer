#!/usr/bin/env python

'''
Filename : clinet.py
purpouse : create a client socket and send request
'''

#import core modules
import socket
import sys
import json

#create an object of socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    socketurl = sys.argv[3]

    url = "http://" + hostname + ":" + str(port) + "/" + socketurl
    message = "Hi from " + hostname + " \n data from url " + socketurl
    #data that should be transfered
    transferdata = {
        "hostname": hostname,
        "port": port,
        "url": socketurl,
        "data": message
    }

    client_socket.connect((hostname, port))
    client_socket.send(json.dumps(transferdata))
    server_response = client_socket.recv(10000)

    print server_response

    client_socket.close()

except IndexError:
    print "Hostname or portnumber is not defined"

except ValueError:
    print "port Number must be a integer format"

except socket.error as err:
    print err
