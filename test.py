from itertools import chain
import random
import string

def addChar(text,char,place):
  return text[:place] + char + text[place:]

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
    sequence = letter * maximum
    result = normalized_content.find(sequence)
   
    return result

str1 = ""
for i in range(10):
    str1 += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
    #print('{0} {1}'.format('random choice ',str1))
    if i == random.randint(1,8) or i % 2 == 0: #obtenemos una posicion random entre 1 y la longitud de la cadena a generar(excepto el final de la misma)
        #str1+=''.ljust(random.randint(3,5)) #insertamos 3 ó 5 espacios vacíos en dicha posición de longitud aleatoria
        str1+=''.ljust(random.randint(3,5), " ") #insertamos 3 ó 5 espacios vacíos en dicha posición de longitud aleatoria
        #str1 += 
        #print("0")
        #str1 += addChar(str1, " ", i)
print(IsSequenceRepeated("str111eEr",'e',2))