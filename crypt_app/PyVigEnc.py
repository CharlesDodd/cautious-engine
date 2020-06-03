#Vigenere Encrypt

def encrypt(key, text):
    result=[]
    key_index = 0
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz"


    for letter in text:
        num = letters.find(letter)
        if num != -1:
            num += letters.find(key[key_index])
            num %= len(letters)

            result.append(letters[num])

            key_index += 1
            if key_index == len(key):
                key_index = 0
        
            
    return''.join(result)
