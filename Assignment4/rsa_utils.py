import math
import random
import time
import base64
import hashlib

def sha256_hash(data):
    """Generate SHA-256 hash of the data."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def sign(private_key, data):
    """Create a digital signature by hashing then encrypting the data."""
    data_hash = sha256_hash(str(data))
    encrypted_hash = encrypt(private_key, data_hash)
    return encrypted_hash

def verify_signature(public_key, data, signature):
    """Verify a signature by decrypting it and comparing with data hash."""
    try:
        decrypted_hash = decrypt(public_key, signature)
        data_hash = sha256_hash(str(data))
        return decrypted_hash == data_hash
    except:
        return False

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(min_val, max_val):
    """Generate a random prime number between min_val and max_val."""
    while True:
        prime = random.randint(min_val, max_val)
        if is_prime(prime):
            return prime

def gcd(a, b):
    """Calculate the Greatest Common Divisor using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Find modular multiplicative inverse of e mod phi."""
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = egcd(b % a, a)
            return gcd, y - (b // a) * x, x

    gcd, x, _ = egcd(e, phi)
    if gcd != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % phi

def generate_keypair(p, q):
    """Generate public and private keys."""
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e (public key exponent)
    e = random.randint(1, phi)
    while gcd(e, phi) != 1:
        e = random.randint(1, phi)
    
    # Compute d (private key)
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    """Encrypt the plaintext using public key."""
    key, n = pk
    # Convert text to number representation
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    """Decrypt the ciphertext using private key."""
    key, n = pk
    # Convert back to text
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)