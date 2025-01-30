# class PolyAlphabeticCipher:
#     def __init__(self):
#         pass
    
#     def encrypt(self,plaintext,key):
#         pass
#     def decrypt(self,ciphertext,key):
#         pass

"""Program to implement a vigenere cipher
Vigenere cipher is a polyalphabetic cipher for which the plaintext is made up of letters of the English alphabet,
and the key is a word. The letters are encoded in such a way that they are assigned a value from 0 to 25, and the 
ciphertext is computed by adding the values of the plaintext and the key, and taking a modulus with 26.
"""
#function to accept plaintext from the user
def input_plaintext():
    plaintext=input("enter a message ")

    #empty string for making the plaintext upper case
    str1=""   

    #ignoring spaces in the plaintext
    for letter in plaintext:
        if letter!=" ":
            str1+=letter

    plaintext=str1

    #converting plaintext to uppercase
    plaintext=plaintext.upper()
    return plaintext

#function to encrypt the plaintext with the help of the key
def encrypt(plaintext,key):
    index1=0                  #pointer iterating over the plaintext letters
    index2=0                  #pointer iterating over the key letters 
    ciphertext=""             #ciphertext string which is returned at the end
    
    #iterating over the plaintext
    while index1<len(plaintext):

        #assigning every letter a code by using their ASCII values
        letter=ord(plaintext[index1])%65       
        key_letter=ord(key[index2])%65     

        #shifting every letter in the plaintext by the value of the corresponding value of the key,
        #taking a modulo with 26, and converting it back into letter by generating ASCII value
        cipher_letter=chr(((letter+key_letter)%26)+65)   

        #appending every letter to the ciphertext
        ciphertext+=cipher_letter

        #increasing both pointers by 1
        index1+=1
        index2+=1

        #resetting the index of the key until the plaintext pointer reaches the end
        if index2==len(key):
            index2=0
    return ciphertext


plaintext=input_plaintext()
key=input("enter key ")            #taking key input from the user
key=key.upper()                    #converting key to uppercase
ciphertext=encrypt(plaintext,key)  #calling the encrypt function
print(ciphertext)           

""" 
for test vector
plaintext="she is listening"
key=PASCAL
ciphertext=HHWKSWXSLGNTCG
output matches the given ciphertext
"""