def hex_to_bin(hex_str):
    """Convert hexadecimal string to binary string."""
    bin_str = ''
    for i in range(len(hex_str)):
        bin_str += bin(int(hex_str[i], 16))[2:].zfill(4)
    return bin_str

def bin_to_hex(bin_str):
    """Convert binary string to hexadecimal string."""
    hex_str = ''
    for i in range(0, len(bin_str), 4):
        hex_str += hex(int(bin_str[i:i+4], 2))[2:].zfill(1)
    return hex_str.upper()

def permute(k, arr, n):
    """Permute the bits of k according to the array arr."""
    permutation = ''
    for i in range(n):
        permutation += k[arr[i] - 1]
    return permutation

def shift_left(k, shifts):
    """Circular left shift k by shifts positions."""
    return k[shifts:] + k[:shifts]

def xor(a, b):
    """XOR two strings of binary numbers."""
    ans = ''
    for i in range(len(a)):
        if a[i] == b[i]:
            ans += '0'
        else:
            ans += '1'
    return ans

# Initial Permutation (IP)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation (IP^-1)
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

# Expansion D-box Table
expansion_table = [32, 1, 2, 3, 4, 5, 4, 5,
                  6, 7, 8, 9, 8, 9, 10, 11,
                  12, 13, 12, 13, 14, 15, 16, 17,
                  16, 17, 18, 19, 20, 21, 20, 21,
                  22, 23, 24, 25, 24, 25, 26, 27,
                  28, 29, 28, 29, 30, 31, 32, 1]

# S-box Tables
sbox = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# Straight Permutation Table (P-box)
per = [16, 7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2, 8, 24, 14,
       32, 27, 3, 9,
       19, 13, 30, 6,
       22, 11, 4, 25]

# Parity bit drop table (PC-1)
keyp = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Number of bit shifts for each round
shift_table = [1, 1, 2, 2,
              2, 2, 2, 2,
              1, 2, 2, 2,
              2, 2, 2, 1]

# Key compression table (PC-2)
key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]

def generate_keys(key):
    """Generate 16 subkeys for DES rounds."""
    # Convert key to binary
    key = hex_to_bin(key)
    
    # Parity bit drop (PC-1): Convert 64-bit key to 56-bit key
    key = permute(key, keyp, 56)
    
    # Splitting: Split the 56-bit key into two 28-bit halves
    left = key[0:28]
    right = key[28:56]
    
    rkb = []  # Round keys binary
    rk = []   # Round keys hex
    
    for i in range(16):
        # Shifting according to shift table
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])
        
        # Combining: Combine the two 28-bit halves
        combined = left + right
        
        # Key Compression (PC-2): Reduce from 56 bits to 48 bits
        round_key = permute(combined, key_comp, 48)
        
        rkb.append(round_key)
        rk.append(bin_to_hex(round_key))
    
    return rkb, rk

def f_function(right, rkb_i):
    """Feistel (F) function used in each round."""
    # 1. Expansion: Expand 32-bit right half to 48 bits
    right_expanded = permute(right, expansion_table, 48)
    
    # 2. XOR with round key
    xor_result = xor(right_expanded, rkb_i)
    
    # 3. S-box substitution: Transform 48 bits to 32 bits
    sbox_result = ''
    for j in range(8):
        # Get the 6-bit chunk for current S-box
        chunk = xor_result[j*6:j*6+6]
        
        # Calculate row (first and last bit) and column (middle 4 bits)
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        
        # Get value from S-box and convert to 4-bit binary
        val = sbox[j][row][col]
        sbox_result += bin(val)[2:].zfill(4)
    
    # 4. Permutation: Rearrange the 32 bits
    return permute(sbox_result, per, 32)

def encrypt(plain_text, key, debug=False):
    """Encrypt plaintext using DES algorithm."""
    # Convert plaintext to binary
    plain_text = hex_to_bin(plain_text)
    
    # Initial Permutation (IP)
    plain_text = permute(plain_text, IP, 64)
    
    if debug:
        print("After initial permutation:", bin_to_hex(plain_text))
    
    # Generate subkeys for all rounds
    rkb, rk = generate_keys(key)
    
    # Split the permuted block into left and right halves
    left = plain_text[0:32]
    right = plain_text[32:64]
    
    # Store round outputs for verification
    round_outputs = []
    
    # 16 rounds of encryption
    for i in range(16):
        if debug:
            print(f"Round {i+1}:")
            print(f"  Left: {bin_to_hex(left)}, Right: {bin_to_hex(right)}")
            print(f"  Round Key: {rk[i]}")
        
        # Save original right half before modification (needed for swap)
        original_right = right
        
        # Apply F-function to right half and XOR with left half
        right_processed = f_function(right, rkb[i])
        new_right = xor(left, right_processed)
        
        # New left half is original right half (swap happens here)
        left = original_right
        
        # New right half is result of XOR
        right = new_right
        
        # Store combined output after this round
        round_output = left + right
        round_outputs.append(round_output)
        
        if debug:
            print(f"  After round {i+1}: {bin_to_hex(round_output)}")
    
    # After final round, swap one last time (undo last swap)
    # Note: in DES, we need to swap after the 16th round to make encryption/decryption symmetric
    left, right = right, left
    
    # Combine final left and right halves
    combined = left + right
    
    # Final Permutation (IP^-1)
    cipher_text = permute(combined, FP, 64)
    
    if debug:
        print("Final cipher text:", bin_to_hex(cipher_text))
    
    return bin_to_hex(cipher_text), round_outputs

def decrypt(cipher_text, key, debug=False):
    """Decrypt ciphertext using DES algorithm."""
    # Convert ciphertext to binary
    cipher_text = hex_to_bin(cipher_text)
    
    # Initial Permutation (IP)
    cipher_text = permute(cipher_text, IP, 64)
    
    if debug:
        print("After initial permutation (decrypt):", bin_to_hex(cipher_text))
    
    # Generate subkeys (same as encryption, but use in reverse order)
    rkb, rk = generate_keys(key)
    rkb = rkb[::-1]  # Reverse the list of keys for decryption
    rk = rk[::-1]    # For debugging only
    
    # Split into left and right halves
    left = cipher_text[0:32]
    right = cipher_text[32:64]
    
    # Store round outputs for verification
    round_outputs = []
    
    # 16 rounds of decryption (identical to encryption, but with keys in reverse order)
    for i in range(16):
        if debug:
            print(f"Decryption Round {i+1}:")
            print(f"  Left: {bin_to_hex(left)}, Right: {bin_to_hex(right)}")
            print(f"  Round Key: {rk[i]}")
        
        # Save original right half before modification (needed for swap)
        original_right = right
        
        # Apply F-function to right half and XOR with left half
        right_processed = f_function(right, rkb[i])  
        new_right = xor(left, right_processed)
        
        # New left half is original right half
        left = original_right
        
        # New right half is result of XOR
        right = new_right
        
        # Store combined output after this round
        round_output = left + right
        round_outputs.append(round_output)
        
        if debug:
            print(f"  After decryption round {i+1}: {bin_to_hex(round_output)}")
    
    # After final round, swap one last time (undo last swap)
    left, right = right, left
    
    # Combine final left and right halves
    combined = left + right
    
    # Final Permutation (IP^-1)
    plain_text = permute(combined, FP, 64)
    
    if debug:
        print("Final decrypted text:", bin_to_hex(plain_text))
    
    return bin_to_hex(plain_text), round_outputs

def verify_des(debug=False):
    """Verify DES encryption/decryption with test cases and check round equivalences."""
    # Test cases with plaintext and key
    test_cases = [
        {
            'plaintext': '0123456789ABCDEF',
            'key': '133457799BBCDFF1'
        },
        {
            'plaintext': 'FEDCBA9876543210',
            'key': 'AABBCCDDEEFF0011'
        },
        {
            'plaintext': '0000000000000000',
            'key': 'FFFFFFFFFFFFFFFF'
        }
    ]
    
    for i, test in enumerate(test_cases):
        plaintext = test['plaintext']
        key = test['key']
        
        print(f"\nTest Case {i+1}:")
        print(f"Plaintext: {plaintext}")
        print(f"Key: {key}")
        
        # Encrypt
        ciphertext, enc_rounds = encrypt(plaintext, key, debug)
        print(f"Ciphertext: {ciphertext}")
        
        # Decrypt
        decrypted, dec_rounds = decrypt(ciphertext, key, debug)
        print(f"Decrypted: {decrypted}")
        
        # Verify (a): Check if decryption yields original plaintext
        print(f"a. Original plaintext recovered: {plaintext == decrypted}")
        
        # Verify (b): Check if output of 1st encryption round equals output of 15th decryption round
        first_enc_round = bin_to_hex(enc_rounds[0])
        fifteenth_dec_round = bin_to_hex(dec_rounds[14])
        print(f"b. 1st encryption round equals 15th decryption round: {first_enc_round == fifteenth_dec_round}")
        if debug and first_enc_round != fifteenth_dec_round:
            print(f"   First encryption round: {first_enc_round}")
            print(f"   Fifteenth decryption round: {fifteenth_dec_round}")
        
        # Verify (c): Check if output of 14th encryption round equals output of 2nd decryption round
        fourteenth_enc_round = bin_to_hex(enc_rounds[13])
        second_dec_round = bin_to_hex(dec_rounds[1])
        print(f"c. 14th encryption round equals 2nd decryption round: {fourteenth_enc_round == second_dec_round}")
        if debug and fourteenth_enc_round != second_dec_round:
            print(f"   Fourteenth encryption round: {fourteenth_enc_round}")
            print(f"   Second decryption round: {second_dec_round}")

# Run verification
if __name__ == "__main__":
    verify_des(debug=False)  # Set to True for detailed debugging output