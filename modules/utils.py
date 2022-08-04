import itertools
from os.path import exists as file_exists
from configparser import ConfigParser
import socket, logging, time

#Get the configparser object
config_object = ConfigParser()
initValues = ""
#def getInitValues():
if file_exists("config.ini"):
   #Read config.ini file
   config_object.read("config.ini")
   #Get the password
   initValues = config_object["AppConfig"]
   #print("File name es {}".format(initValues["fileName"]))
else:
    config_object["AppConfig"] = {
    "# Value to indicate the name of the exported container file of the generated strings"
    "fileName": "chains.txt",
    "# value to indicate total character string to generate"
    "numberOfChains": "500",
    "# value to indicate minimum length value in each generated string"
    "minChainLenght" : "10",
    "# value to indicate maximum length value in each generated string"
    "maxChainLenght" : "45",
    "# Value to indicate the server name to communicate with server via socket"
    "ip_server" : "127.0.0.1",
    "# Value to indicate the port to communicate with server via socket, specify a value above 1024"
    "port_server" : "8085"
    }
    #Write the above sections to config.ini file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
        
        
def writeChain(chain):
    """
    This function open file in append mode and write new content
    """
    try:
        with open(initValues["fileName"], 'a') as f:
            f.write(chain + '\n')
    except IOError:
        f.close()
        
def saveChainToFile(chain):
    """
    This function greets to the person passed in as a parameter
    """
    # verify if chains.txt exist, in positive case, we proced to deleted
    if file_exists(initValues["fileName"]):
        #print(f'The file exists')
        #os.remove("chains.txt")
        writeChain(chain)
    else:
        #open file in append mode and write new content
        writeChain(chain)        

def SendChainsViaSocket(content):
    #line to create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connect to the server socket by invoking the above client socket object’s
    #client_socket.connect((initValues["ip_server"], initValues["port_server"]))
    client_socket.connect(('localhost', int(initValues["port_server"])))
    #send text data to the server socket
    try:
        client_socket.sendall(content.encode('utf-8'))
        print(print("Sending content to server"))
        time.sleep(2) # Sleep for 2 seconds
        #read the text that the server socket sends back.
        #data_tmp = client_socket.recv(1024)
        #The received data is also a bytes object, you need to convert it to a text string by invoking
        # the bytes object’s function decode(‘utf-8’).
        #str_tmp = data_tmp.decode('utf-8')
        # Look for the response
        amount_received = 0
        amount_expected = len(content)

        while amount_received < amount_expected:
            data = client_socket.recv(1024)
            amount_received += len(data)
            print('Received from server {!r}'.format(data))
            time.sleep(2) # Sleep for 2 seconds
    finally:
        print('closing socket')
        time.sleep(2) # Sleep for 2 seconds
        #close the socket connection
        client_socket.close()
    
    
def check_tcp_socket(host, port, s_timeout=2):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(s_timeout)
        tcp_socket.connect((host, port))
        tcp_socket.close()
        print("Socket available at {}:{} to sending and processing this info".format(initValues["ip_server"], initValues["port_server"]))
        time.sleep(2) # Sleep for 2 seconds
        return True
    except (socket.timeout, socket.error):
        print("Socket not available to sending and processing this info")
        time.sleep(2) # Sleep for 2 seconds
        #logging.exception("socket NOT available!")
        return False 