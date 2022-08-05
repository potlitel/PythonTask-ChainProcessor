from ctypes import util
import random
import string
import os

from modules import utils

def GenerateRandomAlphabeticalString():
    """
    This function generate a random alphabetical string of a variable length
    """
    ChainsToProcessOnServer = []
    str1 = ""
    lenght = random.randint(int(utils.initValues["minchainlenght"]),int(utils.initValues["maxchainlenght"])) #longitug de la cadena a generar varía aleatoriamente entre 50 y 100 caracteres
    for i in range(lenght):
        str1 += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        if i == random.randint(1,lenght-1): #obtenemos una posicion random entre 1 y la longitud de la cadena a generar(excepto el final de la misma)
            str1+=''.ljust(random.randint(3,5)) #insertamos 3 ó 5 espacios vacíos en dicha posición de longitud aleatoria
    #we cut the generated chain to a maximum of the length allowed in the key "maxChainLenght"
    cutted_str = str1[:int(utils.initValues["maxchainlenght"])]
    #emove trailing spaces from the end of the cutted_str
    #cutted_str.rstrip()
    
    # Check if last character is ' ', used also 'endswith' method
    #if cutted_str[-1] == ' ':
    #    print("Last character is ' ' ")
    cutted_str = utils.ReplaceLastCharacterIfIsEmptySpace(cutted_str)
    
    ChainsToProcessOnServer.append(cutted_str)
    #call this fucntion to append str text
    utils.writeChainToFile(cutted_str)
    print(ChainsToProcessOnServer)
    return ChainsToProcessOnServer

def SendChainsToSocketServer(chaintToProcess):
    #verify if socket is available
    socket_available = utils.check_tcp_socket('localhost', int(utils.initValues["port_server"]),2)
    if socket_available:
        utils.SendChainsViaSocket('Content sending from client')
        #utils.SendChainsViaSocket(chaintToProcess)
    else:
        #utils.logging.exception("Socket not available to sending and processing this info")
        utils.time.sleep(2) # Sleep for 2 seconds
        print("Launch ProcessingServer.py (Server side app) and try again.")
        utils.time.sleep(2) # Sleep for 2 seconds
       
def GenerateCharacterStringIntoFile(totalChains):
    """
    This function greets to the person passed in as a parameter
    """
    print("\nGenerating a total of {} character strings".format(int(utils.initValues["numberofchains"])))
    # verify if chains.txt exist, in positive case, we proced to deleted
    if utils.file_exists(utils.initValues["filename"]):
        os.remove(utils.initValues["filename"])
    for i in range(totalChains):
        chaintToProcess=GenerateRandomAlphabeticalString()
    SendChainsToSocketServer(chaintToProcess)

#def Main():      
#    if utils.file_exists("config.ini"):
#        GenerateCharacterStringIntoFile(int(utils.initValues["numberofchains"]))
#    else:
#        utils.time.sleep(2) # Sleep for 2 seconds
#        utils.createConfigFile()
#        utils.time.sleep(2) # Sleep for 2 seconds
#        GenerateCharacterStringIntoFile(int(utils.initValues["numberofchains"]))
        
def Main():
    """
    Main function. Verifies the existence of the configuration file, if not, it proceeds to create it, 
    then the character string generation process begins
    """
    if not utils.file_exists("config.ini"):
        utils.time.sleep(2)  # Sleep for 2 seconds
        utils.createConfigFile()
        utils.time.sleep(2)  # Sleep for 2 seconds
    numberofchains = int(utils.initValues["numberofchains"])
    GenerateCharacterStringIntoFile(numberofchains)

Main()

