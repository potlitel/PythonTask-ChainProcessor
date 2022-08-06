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
    FORMAT = "utf-8"
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
                #data = connection.recv(10000024).decode(FORMAT)
                data = connection.recv(10000024).decode(FORMAT)
                #print('received {!r}'.format(data))
                if data:
                    #print('sending data back to the client')
                    
                    #create a function
                    #split_word = " \ "
                    #res_str = data.partition(split_word)
                    #print('Response from server {!r}'.format(res_str))
                    #data = connection.recv(10000024).decode(FORMAT)
                    
                    #myfile = open(data,'w')
                    data1 = data.split('\n')
                    intValues = []
                    #print(data1[1])
                    list_length = len(data1)
                    for i in range(list_length-1):
                        #convert every item in list to an integer, para poder enviarlo como respuesta al cliente
                        data1[i] = '{0} {1}'.format(data1[i], ' Processed by server')
                        #data1[i] = int('{0} {1}'.format(data1[i], ' two'))
                    #print list of strings
                    print(data1)
                    #end create a function
                    #arr = bytes(data1, 'utf-8')
                    #bytes = bytearray(data1)
                    #create a bytearray from a list, list cannot send directly as response
                    #test_list = [int(i) for i in data1]
                    #test_list = list(map(bytearray, data1))
                    #values = bytearray(test_list)
                    
                    #convert a list of strings to a bytearray
                    a = '|'.join(data1)
                    test_array = bytearray(a.encode('utf-8'))
                    #send back response to client
                    connection.sendall(test_array)
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