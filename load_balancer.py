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
import thread

#divert url according to url
def divert(sendparam, delay):
    try : 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((sendparam['address']['host'],
                            sendparam['address']['port']))
        client_socket.send(json.dumps(sendparam['address']))
        server_response = client_socket.recv(10000)
        sendparam['connection'].send(server_response)
    
    except ValueError:
        print "400 Bad Request port Number must be a integer format"

    except socket.error, v:
        errorcode=v[0]
        if errorcode==111:
            errormessage = "404 Connection Refused for HOST : " + sendparam['address']['host'] + " PORT : " + str(sendparam['address']['port'])
            print errormessage
            sendparam['connection'].send(errormessage)

    except socket.error as msg:
        print "400 Bad request Socket Error: %s" % msg

#import extra modules
try:
    
    with open('configutration.json') as configurtaions:
        configdata = json.load(configurtaions)

    datakeys = configdata['configuration'].keys()

    server = socket.socket()
    server.bind(('127.0.0.1', 8090))
    server.listen(5)
    print 'start listening {"host" : "127.0.0.1" , "port" : 8090 }'

    while True:
        connection, address = server.accept()
        data = json.loads(connection.recv(4096))
        url = data['url']
        if url in datakeys:
            sendparam = {
                "connection": connection,
                "address": configdata['configuration'][url],
                "data": data
            }
            thread.start_new_thread(divert, (sendparam, 5))
        else:
            connection.send("400 Bad Request")

except ValueError:
    print "400 Bad request port Number must be a integer format"

except socket.error, v:
    errorcode=v[0]
    if errorcode==errno.ECONNREFUSED:
        errormessage = "404 Connection Refused for HOST : localhost  PORT : 8090 "
        print errormessage
        connection.send(errormessage)

except socket.error as msg:
    print "400 Bad request Socket Error: %s" % msg
