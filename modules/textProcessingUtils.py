import string


def StringCountElements(content,counter):
    """
    This function counts the number of elements(letters, digits, whitespaces and other) in the string
    return: number of elements in dictionary {'letters':0,'digits':0,'whitespaces':0,'other':0}
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

    """
    normalized_content = content.lower()
    sequence = letter * maximum
    result = normalized_content.find(sequence)
   
    return result