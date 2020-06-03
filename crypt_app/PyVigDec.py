#Vigenere Decrypt

def decrypt(key,text):
    result=[]
    key_index = 0
    #letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz"


    for letter in text:
        num = letters.find(letter)
        num -= letters.find(key[key_index])
        num %= len(letters)

        result.append(letters[num])

        key_index += 1
        if key_index == len(key):
            key_index = 0
        

    return''.join(result)
