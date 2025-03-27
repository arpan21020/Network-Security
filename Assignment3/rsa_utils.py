import math
import random
import time
import base64

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

def encode_timestamp(timestamp=None):
    """Encode timestamp to a fixed-length string."""
    if timestamp is None:
        timestamp = int(time.time())
    return base64.b64encode(str(timestamp).encode()).decode()

def decode_timestamp(encoded_timestamp):
    """Decode timestamp from encoded string."""
    return int(base64.b64decode(encoded_timestamp.encode()).decode())

def is_timestamp_valid(issued_timestamp, duration_seconds):
    """Check if timestamp is still valid."""
    current_time = int(time.time())
    return current_time <= (issued_timestamp + duration_seconds)