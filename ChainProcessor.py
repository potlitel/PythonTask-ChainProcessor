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
        if i == random.randint(1,lenght-5) or i % 2 == 0: #obtenemos una posicion random entre 1 y la longitud de la cadena a generar(excepto el final de la misma)
            #str1+=''.ljust(random.randint(3,5)) #insertamos 3 ó 5 espacios vacíos en dicha posición de longitud aleatoria
            str1+=''.ljust(random.randint(3,5), " ") #insertamos 3 ó 5 espacios vacíos en dicha posición de longitud aleatoria
    #we cut the generated chain to a maximum of the length allowed in the key "maxChainLenght"
    cutted_str = str1[:int(utils.initValues["maxchainlenght"])]    
    cutted_str = utils.ReplaceLastCharacterIfIsEmptySpace(cutted_str)
    # add cutted_str to arrary that contains the chains to be processed
    ChainsToProcessOnServer.append(cutted_str)
    #call this fucntion to append str text
    utils.writeChainToFile(cutted_str)
    #print(ChainsToProcessOnServer)
    return ChainsToProcessOnServer

def SendChainsToSocketServer(chaintToProcess):
    """
    This function is responsible for sending content to be processed on server
    @params:
        chaintToProcess   - Required  : strigns to process (String)
    """
    #verify if socket is available
    socket_available = utils.check_tcp_socket('localhost', int(utils.initValues["port_server"]),2)
    if socket_available:
        #utils.SendChainsViaSocket('Content sending from client')
        """ Opening and reading the file data. """
        file = open("chains.txt", "r")
        data = file.read()
        utils.SendChainsViaSocket(data)
    else:
        #utils.logging.exception("Socket not available to sending and processing this info")
        utils.time.sleep(2) # Sleep for 2 seconds
        print("Launch ProcessingServer.py (Server side app) and try again.")
        utils.time.sleep(2) # Sleep for 2 seconds
       
def GenerateCharacterStringIntoFile(totalChains):
    """
    This function greets to the person passed in as a parameter
    @params:
        totalChains   - Required  : total character strings to generate (String)
    """
    print("\nGenerating a total of {} character strings".format(int(utils.initValues["numberofchains"])))
    # verify if chains.txt exist, in positive case, we proced to deleted
    if utils.file_exists(utils.initValues["filename"]):
        os.remove(utils.initValues["filename"])
    for i in range(totalChains):
        chaintToProcess=GenerateRandomAlphabeticalString()
    SendChainsToSocketServer(chaintToProcess)
        
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

