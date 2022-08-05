import random
import string
import os

from modules import utils

def GenerateRandomAlphabeticalString():
    """
    This function generate a random alphabetical string of a variable length
    """
    my_input = []
    str1 = ""
    lenght = random.randint(int(utils.initValues["minchainlenght"]),int(utils.initValues["maxchainlenght"])) #longitug de la cadena a generar varía aleatoriamente entre 50 y 100 caracteres
    for i in range(lenght):
        str1 += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        if i == random.randint(1,lenght-1): #obtenemos una posicion random entre 1 y la longitud de la cadena a generar(excepto el final de la misma)
            str1+=''.ljust(random.randint(3,5)) #insertamos 3 ó 5 espacios vacíos en dicha posición de longitud aleatoria
    #we cut the generated chain to a maximum of the length allowed in the key "maxChainLenght"
    cutted_str = str1[:int(utils.initValues["maxchainlenght"])]
    #print(cutted_str) print current chain
    my_input.append(cutted_str)
    #print(my_input)
    #call this fucntion to append str text
    utils.saveChainToFile(cutted_str)
       
def GenerateCharacterStringIntoFile(totalChains):
    """
    This function greets to the person passed in as a parameter
    """
    print("\nGenerating a total of {} character strings".format(int(utils.initValues["numberofchains"])))
    # verify if chains.txt exist, in positive case, we proced to deleted
    if utils.file_exists(utils.initValues["filename"]):
        os.remove(utils.initValues["filename"])
    for i in range(totalChains):
        GenerateRandomAlphabeticalString()
    #verify if socket is available
    socket_available = utils.check_tcp_socket('localhost', int(utils.initValues["port_server"]),2)
    if socket_available:
        utils.SendChainsViaSocket('Content sending from client')
    else:
        #utils.logging.exception("Socket not available to sending and processing this info")
        utils.time.sleep(2) # Sleep for 2 seconds
        print("Launch ProcessingServer.py (Server side app) and try again.")
        utils.time.sleep(2) # Sleep for 2 seconds

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

