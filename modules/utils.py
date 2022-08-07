"""
Utils Module
"""
from os.path import exists as file_exists
from configparser import ConfigParser
import random, socket, logging, time, re, sys, string, os

#Get the configparser object
config_object = ConfigParser()
initValues = ""

def printWithDelay(firstString, seconds):
    """
    This function print firstString, wait n seconds and print lastString  
    @params:
        firstString   - Required  : value to display (String)
        seconds       - Required  : delayed time in seconds to display other msg (Int)
    @return:  None.
    """
    print(firstString,end="",flush=True)
    sys.stdout.flush()
    time.sleep(seconds)
    print(' \u2714',flush=True)

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    @return:  None.
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
        
def DisplayPathToProcessingResultFile(fileNameResults):
    """
    This function is responsible display path to access to file that contains processing results
    @params:
        fileNameResults   - Required  : file name where the processing results will be stored (String)
    @return:  None.
    """
    ROOT_DIR = os.path.abspath(os.curdir)
    print('{0} {1} '.format('See processing results on file:', os.path.join(ROOT_DIR, fileNameResults)))
    
def PostProcessingTask(content):
    """
    This function is responsible for executing post processing tasks on client side
    @params:
        content   - Required  : content to process (String)
    @return:  None.
    """
    FORMAT = "utf-8"
    data1 = content.decode(FORMAT)
    data2 = data1.split('|')
    list_length = len(data2)
    if file_exists(filename_responseserver):
        os.remove(filename_responseserver)
        # Initial call to print 0% progress
        time.sleep(1)
        print('{0} {1} \u2714'.format('Storing processing result in file:', filename_responseserver))
        time.sleep(1)
        printProgressBar(0, list_length, prefix = 'Storage progress:', suffix = 'Complete', length = 50)
        for i in range(list_length):
            writeResponseFromServerToFile(data2[i])
            time.sleep(0.04)
            # Update Progress Bar
            printProgressBar(i + 1, list_length, prefix = 'Storage progress:', suffix = 'Complete', length = 50)

def createConfigFile():
    """
    This function is responsible for creating the configuration file, if it does not exist
    @return:  initValues list.
    """
    config_object["AppConfig"] = {
    "# Value to indicate the name of the exported container file of the generated strings\n"
    "filename": "chains.txt",
    "# Value to indicate the name of the exported file of server processing\n"
    "filename_responseserver" : "ServerProcessingResult.txt",
    "# value to indicate total character string to generate\n"
    "numberofchains": "500",
    "# value to indicate minimum length value in each generated string\n"
    "minchainlenght" : "10",
    "# value to indicate maximum length value in each generated string\n"
    "maxchainlenght" : "45",
    "# Value to indicate the server name to communicate with server via socket\n"
    "ip_server" : "127.0.0.1",
    "# Value to indicate the port to communicate with server via socket, specify a value above 1024\n"
    "port_server" : "9085",
    "# incoming connections that server can listen simultaneously\n"
    "incoming_connections" : "1"
    }
    #Write the above sections to config.ini file
    try:
        with open('config.ini', 'w') as conf:
            config_object.write(conf)
    except IOError:
        print('Unable to create file on disk.')
    #call function to read this values
    config_object.read("config.ini")
    initValues = config_object["AppConfig"]
    return initValues
    
if file_exists("config.ini"):
   config_object.read("config.ini")
   initValues = config_object["AppConfig"]
   filename = initValues["filename"]
   filename_responseserver = initValues["filename_responseserver"]
   numberofchains = initValues["numberofchains"]
   minchainlenght = initValues["minchainlenght"]
   maxchainlenght = initValues["maxchainlenght"]
   ip_server = initValues["ip_server"]
   port_server = initValues["port_server"]
   incoming_connections = initValues["incoming_connections"]
else:
    createConfigFile()
#python configparser to dict (google search)
config_parser_dict = {s:dict(config_object.items(s)) for s in config_object.sections()}
print(config_parser_dict["AppConfig"]["ip_server"])
                  
def ReplaceLastCharacterIfIsEmptySpace(str):
    """
    This function checks if the last character of a string (str parameter) is a blank character, 
    if so it replaces it with another character. Used also 'endswith' method.
    @params:
        str   - Required  : strigns to process (String)
    @return:  the str processed
    """
    if str[-1] == ' ':
       #print("Last character is ' ' ")
       character = random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
       # Replace last character of string with 'character'
       str = re.sub(r".$", character, str)
    return str

def writeChainToFile(chain):
    """
    This function open file (chains.txt) in append mode and write new string character
    @params:
        str   - Required  : strigns to process (String)
    @return:  None.
    """
    try:
        with open(filename, 'a') as f:
            f.write(chain + '\n')
    except IOError:
        f.close()
        
def writeResponseFromServerToFile(response):
    """
    This function craete response file, opened it in append mode and write every response from server
    @params:
        response   - Required  : strigns to process (String)
    @return:  None.
    """
    try:
        with open(filename_responseserver, 'a') as f:
            f.write(response + "\n")
    except IOError:
        f.close()
        
def saveChainToFile(chain):
    """
    This function greets to the person passed in as a parameter
    @return:  None.
    """
    writeChainToFile(chain)

def SendChainsViaSocket(content):
    """
    This function is responsible for establish connection to server
    @params:
        content   - Required  : content to process on the server side (String)
    @return:  None.
    """
    FORMAT = "utf-8"
    #line to create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connect to the server socket by invoking the above client socket object’s
    client_socket.connect(('localhost', int(port_server)))
    #send text data to the server socket
    try:
        #client_socket.sendall(content.encode('utf-8'))
        client_socket.send(content.encode(FORMAT))
        printWithDelay("Sending content to server", 2)
        time.sleep(1) # Sleep for 2 seconds
        # receiving the response
        data = client_socket.recv(10000024)
        time.sleep(1)
        printWithDelay("Receiving processing result from server", 2)
        time.sleep(1)
        PostProcessingTask(data)
    finally:
        printWithDelay('Closing connection with server', 2)
        time.sleep(1) # Sleep for 2 seconds
        #calling function to display processing results file
        DisplayPathToProcessingResultFile(filename_responseserver)
        #close the socket connection
        client_socket.close()
    
    
def check_tcp_socket(host, port, s_timeout=2):
    """
    This function is verify if socket on server is enable
    @params:
        host        - Required  : server host to connect (String)
        port        - Required  : listening port on server (String)
        s_timeout   - Required  : delayed time in seconds (Int)
    @return:  Boolean. True if socket is available, False otherwise
    """
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(s_timeout)
        tcp_socket.connect((host, port))
        tcp_socket.close()
        print("Socket available at {}:{} to sending and processing this info \u2714".format(ip_server, port_server))
        time.sleep(2) # Sleep for 2 seconds
        return True
    except (socket.timeout, socket.error):
        print("Socket not available to sending and processing this info")
        time.sleep(2) # Sleep for 2 seconds
        #logging.exception("socket NOT available!")
        return False 

#createConfigFile()