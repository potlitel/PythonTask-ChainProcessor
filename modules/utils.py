from os.path import exists as file_exists
from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()
initValues = ""
#def getInitValues():
if file_exists("config.ini"):
   #Read config.ini file
   config_object.read("config.ini")
   #Get the password
   initValues = config_object["AppConfig"]
   print("File name es {}".format(initValues["fileName"]))
else:
    config_object["AppConfig"] = {
    "fileName": "chains.txt",
    "numberOfChains": "500",
    "ip_server" : "127.0.0.1",
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
        print(f'The file exists')
        #os.remove("chains.txt")
        writeChain(chain)
    else:
        #open file in append mode and write new content
        writeChain(chain)

def SendChainsViaSocket(content,ip_server,port_server):
    print(print("Sending content to server {}".format(ip_server)))