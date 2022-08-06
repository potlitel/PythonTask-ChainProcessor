from os.path import exists as file_exists
from configparser import ConfigParser
import random, socket, logging, time, re, sys, string, os

def printWithDelay(firstString, seconds):
    """
    This function print firstString, wait n seconds and print lastString  
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
    """
    ROOT_DIR = os.path.abspath(os.curdir)
    print('{0} {1} '.format('See processing results on file:', os.path.join(ROOT_DIR, fileNameResults)))

def createConfigFile():
    """
    This function is responsible for creating the configuration file, if it does not exist
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
    "port_server" : "8085",
    "# incoming connections that server can listen simultaneously\n"
    "incoming_connections" : "1"
    }
    #Write the above sections to config.ini file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)

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
    createConfigFile()
                  
def ReplaceLastCharacterIfIsEmptySpace(str):
    """
    This function checks if the last character of a string (str parameter) is a blank character, 
    if so it replaces it with another character. Used also 'endswith' method.
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
    """
    try:
        with open(initValues["filename"], 'a') as f:
            f.write(chain + '\n')
    except IOError:
        f.close()
        
def writeResponseFromServerToFile(response):
    """
    This function craete response file, opened it in append mode and write every response from server
    """
    try:
        with open(initValues["filename_responseserver"], 'a') as f:
            f.write(response + "\n")
    except IOError:
        f.close()
        
def saveChainToFile(chain):
    """
    This function greets to the person passed in as a parameter
    """
    writeChainToFile(chain)

def SendChainsViaSocket(content):
    """
    This function is responsible for establish connection to server
    """
    FORMAT = "utf-8"
    #line to create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connect to the server socket by invoking the above client socket object’s
    #client_socket.connect((initValues["ip_server"], initValues["port_server"]))
    client_socket.connect(('localhost', int(initValues["port_server"])))
    #send text data to the server socket
    try:
        #client_socket.sendall(content.encode('utf-8'))
        client_socket.send(content.encode(FORMAT))
        printWithDelay("Sending content to server", 2)
        #print("Sending content to server \u2714")
        time.sleep(1) # Sleep for 2 seconds
        # Look for the response
        amount_received = 0
        amount_expected = len(content)

        while amount_received < amount_expected:
            data = client_socket.recv(10000024)
            amount_received += len(data)
            #print('Received from server {!r}'.format(data))
            time.sleep(1)
            #print("Receiving processing result from server \u2714")
            printWithDelay("Receiving processing result from server", 2)
            time.sleep(1)
            #create function
            data1 = data.decode(FORMAT)
            data2 = data1.split('|')
            list_length = len(data2)
            if file_exists(initValues["filename_responseserver"]):
                os.remove(initValues["filename_responseserver"])
            # Initial call to print 0% progress
            time.sleep(1)
            print('{0} {1} \u2714'.format('Storing processing result in file:', initValues["filename_responseserver"]))
            time.sleep(1)
            printProgressBar(0, list_length, prefix = 'Storage progress:', suffix = 'Complete', length = 50)
            for i in range(list_length):
                writeResponseFromServerToFile(data2[i])
                time.sleep(0.04)
                # Update Progress Bar
                printProgressBar(i + 1, list_length, prefix = 'Storage progress:', suffix = 'Complete', length = 50)
    finally:
        printWithDelay('Closing connection with server', 2)
        time.sleep(1) # Sleep for 2 seconds
        #calling function to display processing results file
        DisplayPathToProcessingResultFile(initValues["filename_responseserver"])
        #close the socket connection
        client_socket.close()
    
    
def check_tcp_socket(host, port, s_timeout=2):
    """
    This function is verify if socket on server is enable
    """
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(s_timeout)
        tcp_socket.connect((host, port))
        tcp_socket.close()
        print("Socket available at {}:{} to sending and processing this info \u2714".format(initValues["ip_server"], initValues["port_server"]))
        time.sleep(2) # Sleep for 2 seconds
        return True
    except (socket.timeout, socket.error):
        print("Socket not available to sending and processing this info")
        time.sleep(2) # Sleep for 2 seconds
        #logging.exception("socket NOT available!")
        return False 