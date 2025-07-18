

import random
import string


KEY="akpt"

class PolyAlphabeticCipher:
    """Program to implement a vigenere cipher which is also known as poly 
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
        
        # Get sum of ASCII values
        ascii_sum = sum(ord(c) % 97 for c in text)
        
        # Generate a 4-letter hash based on the sum
        hash_letters = []
        for i in range(4):
            # Use different aspects of the ascii_sum to 
            # generate each letter
            val = (ascii_sum + i * len(text)) % 26
            hash_letters.append(chr(val + 97))
            
        return ''.join(hash_letters)
    
    
    
    
        
    def verify(self,plaintext):
        PLAINTEXT_LENGTH = len(plaintext)
        s = plaintext[:PLAINTEXT_LENGTH-4]
        hash_s = plaintext[PLAINTEXT_LENGTH-4:]
        # print("s:",s," hash_s:",hash_s)
        if self.hash_fn(s) == hash_s:
            return True
        return False
    
    def is_possible_key(self,encrypted_texts,key):
        ans=True
        for i in encrypted_texts:
            temp=self.decrypt(i,key)
            ans=ans and self.verify(temp)
        return ans
    
    
    def brute_force(self,ciphertext,cipher_texts):
        key_list=['a','a','a','a']
        for i in range(26):
            key_list[0]=chr(ord('a')+i)
            for j in range(26):
                key_list[1]=chr(ord('a')+j)
                for k in range(26):
                    key_list[2]=chr(ord('a')+k)
                    for l in range(26):
                        key_list[3]=chr(ord('a')+l)
                        key=''.join(key_list)
                        # print(key)
                        decryptedtext=self.decrypt(ciphertext,key)
                        # print('------------------')
                        
                        if(self.is_possible_key(cipher_texts,key)):
                            return key
        return "none"

    
    
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
        print(f"Random String {i+1} : {random_strings[i]} Encrypted : {temp}")
        
    # Brute Force Attack
    
    print("Brute force attack..... ")
    possible_key=obj.brute_force(encrypted[0],encrypted)
    print("Recovered key:",possible_key)
    
    
    
    # for index, random_string in enumerate(random_strings):
    #     temp=obj.encrypt(random_string,KEY)
    #     print(f"Random String {index + 1}: {random_string} Encrypted: {temp} Decrypted: {obj.decrypt(temp,KEY)}")
    
    #     print("Attacking :"+obj.brute_force(temp))
        
    
        
    