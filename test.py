from itertools import chain
import os
import random
import string
from turtle import clear
from os.path import exists as file_exists

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
for i in range(70):
    str1 += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
    #if i == random.randint(2,68) or i % 50 == 0: #obtenemos una posicion random entre 1 y la longitud de la cadena a generar(excepto el final de la misma)
    #    str1+=''.ljust(random.randint(3,5), " ") #insertamos 3 ó 5 espacios vacíos en dicha posición de longitud aleatoria
    if i == random.randint(2,70/2) or i == 70/2:
        str1+=''.ljust(random.randint(3,5), " ")
def generate_code():

    return ''.join(random.choice(string.ascii_uppercase) +random.choice(string.digits)+ random.choice(('   ', '     ')) for _ in range(random.randrange(50,100)))
str2 = generate_code()



val = file_exists("config.ini")
#list1 = [string.ascii_uppercase, string.ascii_lowercase, string.digits]
#string_val = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + (' ' * 3)) for i in range(70))
print(val)