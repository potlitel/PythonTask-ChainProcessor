"""
ChainProcessor.py: is in charge of all the processing of character strings from the server side
"""
import os, socket, logging
from modules import utils, textProcessingUtils

#Create and configure logger
logger = utils.customlogger("ProcessingServer")

dict_init = utils.new_func(utils.config_object)

def ProcessStringsCharacters(content, dict_init):
    """
    This function process content sending by socket client
    @return:  The content processed.
    """
    #split content into array values
    data = content.split('\n')
    list_length = len(data)
    for i in range(list_length-1):
        weighting_value = textProcessingUtils.getChainWeighting(data[i], dict_init)
        data[i] = '{0} {1} {2}'.format(data[i], 'Weighting:',weighting_value)
    #print(data)             
    #convert a list of strings to a bytearray
    a = '|'.join(data)
    response = bytearray(a.encode('utf-8'))
    return response

def getServerSocketConnection():
    """
    This function create the socket connection
    @return:  the socket object.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    #server_address = ((string(utils.initValues["ip_server"]),utils.initValues["port_server"]))
    server_address = (('localhost',int(dict_init['port_server'])))
    sock.bind(server_address)
    # Listen for incoming connections and configure how many client the server can listen simultaneously
    sock.listen(int(dict_init['incoming_connections']))
    logger.info('Socker server listenning on {0}:{1}'.format(dict_init['ip_server'],int(dict_init['port_server'])))
    return sock

def ReceivedChainsAndSendResponse():
    """
    This function receives the character strings from the client, processes them 
    and returns them as a response to the client.
    @return:  None.
    """
    FORMAT = "utf-8"
    # Create a TCP/IP socket
    sock = getServerSocketConnection()
    while True:
        # update init values in case they are modifies
        dict_init = utils.new_func(utils.config_object)
        # Wait for a connection
        logger.info('Waiting for character strings to be processed, sentding by the client')
        utils.time.sleep(1)
        connection, client_address = sock.accept()
        try:
            logger.info('connection from {0}'.format(client_address))
            utils.time.sleep(1)
            # Receive the data in chunks and retransmit it
            while True:
                data = connection.recv(10000024).decode(FORMAT)
                if data:
                    response = ProcessStringsCharacters(data, dict_init)
                    #print(response)
                    connection.sendall(response)
                else:
                    logger.info('no data from '.format(client_address))
                    utils.time.sleep(1)
                    break
        finally:
            # Clean up the connection
            connection.close()

def Main():
    """
    Principal function. Verifies the existence of the configuration file and logs folder, otherwise it proceeds to create them,
    then the socket server starts the listening process
    @return:  None.
    """
    utils.time.sleep(1)
    if not utils.file_exists("logs"):       
        os.mkdir("logs")
    if not utils.file_exists("config.ini"):
        utils.time.sleep(1)
        utils.createConfigFile()
        utils.time.sleep(1)
    ReceivedChainsAndSendResponse()

Main()