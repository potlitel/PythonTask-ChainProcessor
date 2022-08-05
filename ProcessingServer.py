import os
import socket
import string
import sys
from modules import utils

def ReceivedChainsAndSendResponse():
    """
    This function receives the character strings from the client, processes them 
    and returns them as a response to the client.
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    #server_address = ((string(utils.initValues["ip_server"]),utils.initValues["port_server"]))
    server_address = (('localhost',int(utils.initValues["port_server"])))
    sock.bind(server_address)
    # Listen for incoming connections and configure how many client the server can listen simultaneously
    sock.listen(int(utils.initValues["incoming_connections"]))
    while True:
        # Wait for a connection
        print('Waiting for character strings to be processed sent by the client')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1024)
                print('received {!r}'.format(data))
                if data:
                    print('sending data back to the client')
                    connection.sendall(data)
                else:
                    print('no data from', client_address)
                    break
        finally:
            # Clean up the connection
            connection.close()


#def Main():
#    if utils.file_exists("logs"):
#        ReceivedChainsAndSendResponse()
#    else:
#        print(False)
#        #create folder logs
#        os.mkdir("logs")
#        #create ini file
#        ReceivedChainsAndSendResponse()

def Main():
    """
    Principal function. Verifies the existence of the configuration file and logs folder, otherwise it proceeds to create them,
    then the socket server starts the listening process
    """
    if not utils.file_exists("logs"):       
        print(False)
        #create folder logs
        os.mkdir("logs")
        #create ini file
    if not utils.file_exists("config.ini"):
        utils.time.sleep(2)  # Sleep for 2 seconds
        utils.createConfigFile()
        utils.time.sleep(2)  # Sleep for 2 seconds
    ReceivedChainsAndSendResponse()

Main()