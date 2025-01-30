
KEY="fuck"

import random
import string



class PolyAlphabeticCipher:
    """Program to implement a vigenere cipher
    Vigenere cipher is a polyalphabetic cipher for which the plaintext is made up of letters of the English alphabet,
    and the key is a word. The letters are encoded in such a way that they are assigned a value from 0 to 25, and the 
    ciphertext is computed by adding the values of the plaintext and the key, and taking a modulus with 26.
"""
    def __init__(self):
        pass
    
    def encrypt(self,plaintext,key):
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

    def decrypt(self,plaintext,key):
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
            cipher_letter=chr(((letter-key_letter)%26)+65)   

            #appending every letter to the ciphertext
            ciphertext+=cipher_letter

            #increasing both pointers by 1
            index1+=1
            index2+=1

            #resetting the index of the key until the plaintext pointer reaches the end
            if index2==len(key):
                index2=0
        return ciphertext
    def hash_fn(self,text):
        """
        Simple hash function that:
        1. Sums the position values of each character in the alphabet (a=0, b=1, etc.)
        2. Multiplies by the length of the text
        3. Takes modulo 100 to keep it two digits
        """
        # Convert text to uppercase and filter only letters
        text = ''.join(c for c in text.upper() if c in string.ascii_uppercase)
        
        # Get sum of ASCII values
        ascii_sum = sum(ord(c) % 65 for c in text)
        
        # Generate a 4-letter hash based on the sum
        hash_letters = []
        for i in range(4):
            # Use different aspects of the ascii_sum to generate each letter
            val = (ascii_sum + i * len(text)) % 26
            hash_letters.append(chr(val + 65))
            
        return ''.join(hash_letters)
def generate_random_strings(num_strings=5, string_length=10):
    random_strings = []
    for _ in range(num_strings):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=string_length))
        random_strings.append(random_string)
    return random_strings
    
if __name__=="__main__":
    obj=PolyAlphabeticCipher()
    random_strings = generate_random_strings()
    for i in range(0,len(random_strings)):
        random_strings[i]=random_strings[i]+obj.hash_fn(random_strings[i])
    encrypted=[]
    for i in range(0,len(random_strings)):
        temp=obj.encrypt(random_strings[i])
        encrypted.append(temp)
    
    for index, random_string in enumerate(random_strings):
        print(f"Random String {index + 1}: {random_string} ")
        
    