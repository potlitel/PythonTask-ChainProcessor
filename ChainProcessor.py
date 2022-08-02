import random
import string
import os

from modules import utils
    
print("\nGenerate a random alphabetical string of a fixed length:")


def GenerateRandomAlphabeticalString():
    """
    This function generate a random alphabetical string of a variable length
    """
    str1 = ""
    lenght = random.randint(int(utils.initValues["minChainLenght"]),int(utils.initValues["maxChainLenght"])) #longitug de la cadena a generar varía aleatoriamente entre 50 y 100 caracteres
    #os.remove("chains.txt")
    for i in range(lenght):
        str1 += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        if i == random.randint(1,lenght-1): #obtenemos una posicion random entre 1 y la longitud de la cadena a generar(excepto el final de la misma)
            str1+=''.ljust(random.randint(3,5)) #insertamos 3 ó 5 espacios vacíos en dicha posición de longitud aleatoria
    #we cut the generated chain to a maximum of the length allowed in the key "maxChainLenght"
    cutted_str = str1[:int(utils.initValues["maxChainLenght"])]
    print(cutted_str)
    #call this fucntion to append str text
    saveChainToFile(cutted_str)
    
def writeChain(chain):
    """
    This function open file in append mode and write new content
    """
    try:
        with open(utils.initValues["fileName"], 'a') as f:
            f.write(chain + '\n')
    except IOError:
        f.close()
    
def saveChainToFile(chain):
    """
    This function greets to the person passed in as a parameter
    """
    # verify if chains.txt exist, in positive case, we proced to deleted
    if utils.file_exists(utils.initValues["fileName"]):
        print(f'The file exists')
        #os.remove("chains.txt")
        writeChain(chain)
    else:
        #open file in append mode and write new content
        writeChain(chain)
       
def GenerateCharacterStringIntoFile(totalChains):
    """
    This function greets to the person passed in as a parameter
    """
    # verify if chains.txt exist, in positive case, we proced to deleted
    if utils.file_exists(utils.initValues["fileName"]):
        os.remove(utils.initValues["fileName"])
    for i in range(totalChains):
        GenerateRandomAlphabeticalString()
        
#if file_exists("config.ini"):
GenerateCharacterStringIntoFile(int(utils.initValues["numberOfChains"]))        
