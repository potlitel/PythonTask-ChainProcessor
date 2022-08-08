"""
Text Processing Module
"""
#from asyncio.log import logger
import string, logging
from modules import utils

#Create and configure logger
utils.customlogger(__name__)

dict_init = utils.new_func(utils.config_object)

def StringCountElements(content,counter):
    """
    This function counts the number of elements(letters, digits, whitespaces and other) in the string
    return: number of elements in dictionary {'letters':0,'digits':0,'whitespaces':0,'other':0}
    @params:
        content   - Required  : strigns to process (String)
        counter   - Required  : dictionary to storage data (Dict[str, int])
    """
    normalized_content = content.lower()
    result = counter
    for i in normalized_content:
        if i in string.ascii_lowercase:
            result['letters'] += 1
        elif i in string.digits:
            result['digits'] += 1
        elif i == ' ':
            result['space'] += 1
        else:
            result['other'] += 1
        
    return result

def IsSequenceRepeated(content,letter,maximum):
    """
    This function counts the number of repited letters in the string
    return: indice de la primera vez q aparece la secuencia. -1 si no aparece
    @params:
        content   - Required  : strigns to process (String)
        letter    - Required  : letter to search (String)
        maximum   - Required  : maximum ocurrence value of the string (Int)
    """
    normalized_content = content.lower()
    #letter = string(letter)
    maximum = int(maximum)
    sequence = letter * maximum
    result = normalized_content.find(sequence)
   
    return result

def getChainWeighting(chain, dict_init):
    """
    This function calculates the Weighting of the chain received via parameter
    @params:
        chain   - Required  : strigns to process (String)
    """
    Weighting = ""
    mcounter = {
        'letters': 0,
        'digits': 0,
        'space': 0,
        'other': 0
    }   
    existSequence = IsSequenceRepeated(chain,dict_init['letter_to_detect'],dict_init['maximum_ocurrence_value'])
    if existSequence == -1:
        result = StringCountElements(chain, mcounter)
        processedLetters = result['letters'] * 1.5
        processedNumbers = result['digits'] * 2
        sumValue = processedLetters + processedNumbers
        Weighting = sumValue / result['space']
    else:
        #print('Double {0} rule detected in chain: {1}'.format(utils.letter_to_detect,chain))
        print('Rule detected: {0} .Character "{1}" appears {2} times'.format(chain, dict_init['letter_to_detect'], dict_init['maximum_ocurrence_value']))
        #utils.time.sleep(2)
        Weighting = 100
    return Weighting