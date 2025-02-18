# DES Implementation from Scratch

# Initial and Final Permutation Tables
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

# Expansion Table
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# S-boxes
S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Permutation P
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# PC-1 table (Permuted Choice 1 - for key schedule)
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# PC-2 table (Permuted Choice 2 - for key schedule)
PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

# Number of left shifts for each round
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def permute(block, table):
    """Permute the block according to the given table"""
    return [block[i-1] for i in table]

def left_shift(half, shift_count):
    """Perform a circular left shift on the half"""
    return half[shift_count:] + half[:shift_count]

def string_to_bits(text):
    """Convert a string to a list of bits"""
    result = []
    for char in text:
        bits = bin(ord(char))[2:].zfill(8)
        result.extend([int(b) for b in bits])
    return result

def bits_to_string(bits):
    """Convert a list of bits to a string"""
    result = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        result += chr(int(''.join(map(str, byte)), 2))
    return result

def hex_to_bits(hex_string):
    """Convert a hex string to a list of bits"""
    result = []
    for char in hex_string:
        bits = bin(int(char, 16))[2:].zfill(4)
        result.extend([int(b) for b in bits])
    return result

def bits_to_hex(bits):
    """Convert a list of bits to a hex string"""
    result = ""
    for i in range(0, len(bits), 4):
        nibble = bits[i:i+4]
        result += hex(int(''.join(map(str, nibble)), 2))[2:]
    return result

def apply_expansion(block):
    """Apply the expansion permutation to a 32-bit block"""
    return permute(block, E)

def apply_substitution(expanded_block):
    """Apply S-boxes substitution to a 48-bit block"""
    result = []
    for i in range(8):
        # Extract a 6-bit chunk
        chunk = expanded_block[i*6:(i+1)*6]
        
        # Calculate row and column
        row = (chunk[0] << 1) + chunk[5]
        col = (chunk[1] << 3) + (chunk[2] << 2) + (chunk[3] << 1) + chunk[4]
        
        # Get the value from the S-box
        val = S_BOXES[i][row][col]
        
        # Convert the value to 4 bits
        bits = [int(b) for b in bin(val)[2:].zfill(4)]
        result.extend(bits)
    
    return result

def xor(a, b):
    """XOR two lists of bits"""
    return [a[i] ^ b[i] for i in range(len(a))]

def generate_subkeys(key):
    """Generate 16 subkeys from the main key"""
    # Convert the key to binary if it's a string
    if isinstance(key, str):
        if len(key) == 16:  # Hex key
            key_bits = hex_to_bits(key)
        else:  # ASCII key
            key_bits = string_to_bits(key)
            if len(key_bits) < 64:
                key_bits.extend([0] * (64 - len(key_bits)))
            elif len(key_bits) > 64:
                key_bits = key_bits[:64]
    else:
        key_bits = key
    
    # Apply PC1 permutation
    key_pc1 = permute(key_bits, PC1)
    
    # Split the key into left and right halves
    left_half = key_pc1[:28]
    right_half = key_pc1[28:]
    
    subkeys = []
    for i in range(16):
        # Apply the shift schedule
        left_half = left_shift(left_half, SHIFT_SCHEDULE[i])
        right_half = left_shift(right_half, SHIFT_SCHEDULE[i])
        
        # Combine the halves
        combined = left_half + right_half
        
        # Apply PC2 permutation
        subkey = permute(combined, PC2)
        subkeys.append(subkey)
    
    return subkeys

def f_function(right_half, subkey):
    """The Feistel (F) function"""
    # Expand the right half from 32 to 48 bits
    expanded = apply_expansion(right_half)
    
    # XOR with the subkey
    xored = xor(expanded, subkey)
    
    # Apply S-box substitution
    substituted = apply_substitution(xored)
    
    # Apply permutation P
    permuted = permute(substituted, P)
    
    return permuted

def des_encrypt_block(plaintext, key):
    """Encrypt a 64-bit block using DES"""
    # Convert the plaintext to binary if it's a string
    if isinstance(plaintext, str):
        if len(plaintext) == 16:  # Hex plaintext
            plaintext_bits = hex_to_bits(plaintext)
        else:  # ASCII plaintext
            plaintext_bits = string_to_bits(plaintext)
            if len(plaintext_bits) < 64:
                plaintext_bits.extend([0] * (64 - len(plaintext_bits)))
            elif len(plaintext_bits) > 64:
                plaintext_bits = plaintext_bits[:64]
    else:
        plaintext_bits = plaintext
    
    # Generate subkeys
    subkeys = generate_subkeys(key)
    
    # Apply initial permutation
    permuted = permute(plaintext_bits, IP)
    
    # Split into left and right halves
    left_half = permuted[:32]
    right_half = permuted[32:]
    
    # Store the intermediate states for verification
    round_outputs = []
    
    # 16 rounds of encryption
    for i in range(16):
        round_outputs.append((left_half.copy(), right_half.copy()))
        
        # Apply F function and XOR with left half
        f_output = f_function(right_half, subkeys[i])
        new_right = xor(left_half, f_output)
        
        # Update left and right halves for next round
        left_half = right_half
        right_half = new_right
    
    # Store the final state before swap
    round_outputs.append((left_half.copy(), right_half.copy()))
    
    # Final swap of left and right halves
    final_block = right_half + left_half
    
    # Apply final permutation
    ciphertext_bits = permute(final_block, IP_INV)
    
    return ciphertext_bits, round_outputs

def des_decrypt_block(ciphertext, key):
    """Decrypt a 64-bit block using DES"""
    # Convert the ciphertext to binary if it's a string
    if isinstance(ciphertext, str):
        if len(ciphertext) == 16:  # Hex ciphertext
            ciphertext_bits = hex_to_bits(ciphertext)
        else:  # ASCII ciphertext
            ciphertext_bits = string_to_bits(ciphertext)
    else:
        ciphertext_bits = ciphertext
    
    # Generate subkeys (same as encryption but in reverse order)
    subkeys = generate_subkeys(key)
    subkeys.reverse()
    
    # Apply initial permutation
    permuted = permute(ciphertext_bits, IP)
    
    # Split into left and right halves
    left_half = permuted[:32]
    right_half = permuted[32:]
    
    # Store the intermediate states for verification
    round_outputs = []
    
    # 16 rounds of decryption
    for i in range(16):
        round_outputs.append((left_half.copy(), right_half.copy()))
        
        # Apply F function and XOR with left half
        f_output = f_function(right_half, subkeys[i])
        new_right = xor(left_half, f_output)
        
        # Update left and right halves for next round
        left_half = right_half
        right_half = new_right
    
    # Store the final state before swap
    round_outputs.append((left_half.copy(), right_half.copy()))
    
    # Final swap of left and right halves
    final_block = right_half + left_half
    
    # Apply final permutation
    plaintext_bits = permute(final_block, IP_INV)
    
    return plaintext_bits, round_outputs

def pad_text(text):
    """Pad the text to a multiple of 8 bytes (64 bits) using PKCS#7"""
    padding_length = 8 - (len(text) % 8)
    padded_text = text + chr(padding_length) * padding_length
    return padded_text

def unpad_text(text):
    """Remove PKCS#7 padding"""
    padding_length = ord(text[-1])
    return text[:-padding_length]

def des_encrypt(plaintext, key, output_format='hex'):
    """Encrypt plaintext using DES with the given key"""
    # Pad the plaintext to a multiple of 64 bits
    padded_text = pad_text(plaintext)
    
    ciphertext_bits = []
    all_round_outputs = []
    
    # Process each 64-bit block
    for i in range(0, len(padded_text), 8):
        block = padded_text[i:i+8]
        block_bits = string_to_bits(block)
        encrypted_block, round_outputs = des_encrypt_block(block_bits, key)
        ciphertext_bits.extend(encrypted_block)
        all_round_outputs.append(round_outputs)
    
    if output_format == 'hex':
        return bits_to_hex(ciphertext_bits), all_round_outputs
    else:  # 'text'
        return bits_to_string(ciphertext_bits), all_round_outputs

def des_decrypt(ciphertext, key, input_format='hex'):
    """Decrypt ciphertext using DES with the given key"""
    if input_format == 'hex':
        ciphertext_bits = hex_to_bits(ciphertext)
    else:  # 'text'
        ciphertext_bits = string_to_bits(ciphertext)
    
    plaintext_bits = []
    all_round_outputs = []
    
    # Process each 64-bit block
    for i in range(0, len(ciphertext_bits), 64):
        block_bits = ciphertext_bits[i:i+64]
        decrypted_block, round_outputs = des_decrypt_block(block_bits, key)
        plaintext_bits.extend(decrypted_block)
        all_round_outputs.append(round_outputs)
    
    plaintext = bits_to_string(plaintext_bits)
    
    # Remove padding
    try:
        plaintext = unpad_text(plaintext)
    except:
        pass  # In case there's no valid padding
    
    return plaintext, all_round_outputs

def verify_encryption_decryption(plaintext, key):
    """Verify that encryption followed by decryption yields the original plaintext"""
    # Encrypt
    ciphertext, encrypt_rounds = des_encrypt(plaintext, key)
    
    # Decrypt
    decrypted, decrypt_rounds = des_decrypt(ciphertext, key)
    
    print(f"Original: {plaintext}")
    print(f"Encrypted (hex): {ciphertext}")
    print(f"Decrypted: {decrypted}")
    print(f"Encryption successful: {plaintext == decrypted}")
    
    return encrypt_rounds, decrypt_rounds

def verify_round_outputs(plaintext, key):
    """Verify that specific rounds in encryption match corresponding rounds in decryption"""
    encrypt_rounds, decrypt_rounds = verify_encryption_decryption(plaintext, key)
    
    # Verify that output of 1st encryption round matches output of 15th decryption round
    first_enc_output = encrypt_rounds[0][0][0] + encrypt_rounds[0][0][1]  # First block, first round
    fifteenth_dec_output = decrypt_rounds[0][14][0] + decrypt_rounds[0][14][1]  # First block, fifteenth round
    
    print("\nVerifying 1st encryption round == 15th decryption round:", end=" ")
    print(first_enc_output == fifteenth_dec_output)
    
    # Verify that output of 14th encryption round matches output of 2nd decryption round
    fourteenth_enc_output = encrypt_rounds[0][13][0] + encrypt_rounds[0][13][1]  # First block, fourteenth round
    second_dec_output = decrypt_rounds[0][1][0] + decrypt_rounds[0][1][1]  # First block, second round
    
    print("Verifying 14th encryption round == 2nd decryption round:", end=" ")
    print(fourteenth_enc_output == second_dec_output)

# Test with multiple plaintext-key pairs
def run_tests():
    test_cases = [
        ("Hello123", "SecretK1"),
        ("TestTest", "KeyKey12"),
        ("12345678", "87654321")
    ]
    
    for i, (plaintext, key) in enumerate(test_cases, 1):
        print(f"\n----- Test Case {i} -----")
        print(f"Plaintext: {plaintext}")
        print(f"Key: {key}")
        verify_round_outputs(plaintext, key)
        print("-----------------------")

# Run the tests
if __name__ == "__main__":
    run_tests()