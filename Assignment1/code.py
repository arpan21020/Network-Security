
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
        ciphertext=""
        minus=ord('a')
        for i in range (0,len(plaintext)):
            val1=ord(plaintext[i])-minus
            val2=ord(key[i%4])-minus
            val3=(val1+val2)%26
            ciphertext+=chr(val3+minus)
        return ciphertext
            
            

    def decrypt(self,ciphertext,key):
        plaintext=""
        minus=ord('a')
        for i in range(0, len(ciphertext)):
            val1=ord(ciphertext[i])-minus
            val2=ord(key[i%4])-minus
            val3=(val1-val2)%26
            plaintext+=chr(val3+minus)
        return plaintext
        
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
        random_string = ''.join(random.choices(string.ascii_lowercase, k=string_length))
        random_strings.append(random_string)
    return random_strings
    
if __name__=="__main__":
    obj=PolyAlphabeticCipher()
    # print(obj.encrypt("jgrhxfjmnq",KEY))
    random_strings = generate_random_strings()
    for i in range(0,len(random_strings)):
        random_strings[i]=random_strings[i]+obj.hash_fn(random_strings[i])
    encrypted=[]
    for i in range(0,len(random_strings)):
        temp=obj.encrypt(random_strings[i],KEY)
        encrypted.append(temp)
    
    for index, random_string in enumerate(random_strings):
        temp=obj.encrypt(random_string[:10],KEY)
        print(f"Random String {index + 1}: {random_string[:10]} Encrypted: {temp}  Decrypted: {obj.decrypt(temp,KEY)}")
        
    