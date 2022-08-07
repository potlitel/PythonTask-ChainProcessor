"""
ChainProcessor.py: is in charge of all the processing of character strings from the server side
"""
import os, socket, logging
from modules import utils, textProcessingUtils

#Create and configure logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
# root logger
logger = logging.getLogger("ProcessingServer")

def ProcessStringsCharacters(content):
    """
    This function process content sending by socket client
    @return:  The content processed.
    """
    #split content into array values
    data = content.split('\n')
    list_length = len(data)
    for i in range(list_length-1):
        weighting_value = textProcessingUtils.getChainWeighting(data[i])
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
    server_address = (('localhost',int(utils.port_server)))
    sock.bind(server_address)
    # Listen for incoming connections and configure how many client the server can listen simultaneously
    sock.listen(int(utils.incoming_connections))
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
        # Wait for a connection
        print('Waiting for character strings to be processed sent by the client')
        utils.time.sleep(1)
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            utils.time.sleep(1)
            # Receive the data in chunks and retransmit it
            while True:
                data = connection.recv(10000024).decode(FORMAT)
                if data:
                    response = ProcessStringsCharacters(data)
                    print(response)
                    connection.sendall(response)
                else:
                    print('no data from', client_address)
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
    utils.createConfigFile()
    utils.time.sleep(1)
    if not utils.file_exists("logs"):       
        #print(False)
        #create folder logs
        os.mkdir("logs")
        #create ini file
    if not utils.file_exists("config.ini"):
        utils.time.sleep(1)
        utils.createConfigFile()
        utils.time.sleep(1)
    ReceivedChainsAndSendResponse()

Main()