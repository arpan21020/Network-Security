# DES Cipher Implementation with Per-Round Output Storage and Verification for Three Pairs
# (No changes to the underlying logic)

#------------------------------
# TABLES & CONSTANTS
#------------------------------

# Initial permutation table
ip_table = {
    1: 58, 2: 50, 3: 42, 4: 34, 5: 26, 6: 18, 7: 10, 8: 2,
    9: 60, 10: 52, 11: 44, 12: 36, 13: 28, 14: 20, 15: 12, 16: 4,
    17: 62, 18: 54, 19: 46, 20: 38, 21: 30, 22: 22, 23: 14, 24: 6,
    25: 64, 26: 56, 27: 48, 28: 40, 29: 32, 30: 24, 31: 16, 32: 8,
    33: 57, 34: 49, 35: 41, 36: 33, 37: 25, 38: 17, 39: 9, 40: 1,
    41: 59, 42: 51, 43: 43, 44: 35, 45: 27, 46: 19, 47: 11, 48: 3,
    49: 61, 50: 53, 51: 45, 52: 37, 53: 29, 54: 21, 55: 13, 56: 5,
    57: 63, 58: 55, 59: 47, 60: 39, 61: 31, 62: 23, 63: 15, 64: 7
}

# Key permutation table
key_perm_table = {
    1: 50, 2: 43, 3: 36, 4: 29, 5: 22, 6: 15, 7: 8, 8: 1,
    9: 51, 10: 44, 11: 37, 12: 30, 13: 23, 14: 16, 15: 9, 16: 2,
    17: 52, 18: 45, 19: 38, 20: 31, 21: 24, 22: 17, 23: 10, 24: 3,
    25: 53, 26: 46, 27: 39, 28: 32, 29: 56, 30: 49, 31: 42, 32: 35,
    33: 28, 34: 21, 35: 14, 36: 7, 37: 55, 38: 48, 39: 41, 40: 34,
    41: 27, 42: 20, 43: 13, 44: 6, 45: 54, 46: 47, 47: 40, 48: 33,
    49: 26, 50: 19, 51: 12, 52: 5, 53: 25, 54: 18, 55: 11, 56: 4
}

# Substitution boxes
S1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]

S2 = [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
]

S3 = [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
]

S4 = [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
]

S5 = [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
]

S6 = [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
]

S7 = [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
]

S8 = [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]

# Permutation used in function applied on R
R_perm = [
    15, 6, 19, 20, 28, 11, 27, 16,
    0, 14, 22, 25, 4, 17, 30, 9,
    1, 7, 23, 13, 31, 26, 2, 8,
    18, 12, 29, 5, 21, 10, 3, 24
]

# Bits for compressing the keys
key_compression_table = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

# Final permutation table
final_permutation = {
    1: 40, 2: 8, 3: 48, 4: 16, 5: 56, 6: 24, 7: 64, 8: 32,
    9: 39, 10: 7, 11: 47, 12: 15, 13: 55, 14: 23, 15: 63, 16: 31,
    17: 38, 18: 6, 19: 46, 20: 14, 21: 54, 22: 22, 23: 62, 24: 30,
    25: 37, 26: 5, 27: 45, 28: 13, 29: 53, 30: 21, 31: 61, 32: 29,
    33: 36, 34: 4, 35: 44, 36: 12, 37: 52, 38: 20, 39: 60, 40: 28,
    41: 35, 42: 3, 43: 43, 44: 11, 45: 51, 46: 19, 47: 59, 48: 27,
    49: 34, 50: 2, 51: 42, 52: 10, 53: 50, 54: 18, 55: 58, 56: 26,
    57: 33, 58: 1, 59: 41, 60: 9, 61: 49, 62: 17, 63: 57, 64: 25
}

#------------------------------
# HELPER FUNCTIONS
#------------------------------

def circular_shift(array):
    array2 = []
    array2.extend(array[1:len(array)])
    array2.append(array[0])
    return array2

def binary_to_hex(binary_string):
    decimal_value = int(binary_string, 2)
    hex_length = (len(binary_string) + 3) // 4
    hex_string = hex(decimal_value)[2:].zfill(hex_length)
    return hex_string

def hex_to_binary(hex_num):
    # hex_num = hex_num.lstrip('0x')
    int_num = int(hex_num, 16)
    binary_num = format(int_num, '064b')
    return binary_num

def int_to_binary(n):
    return format(n, '04b')

def binary_to_int(s):
    return int(s, 2)

def R_function(R, key):
    expanded_bits = [31,0,1,2,3,4,3,4,5,6,7,8,7,8,9,10,11,12,11,12,13,14,15,16,15,16,17,18,19,20,19,20,21,22,23,24,23,24,25,26,27,28,27,28,29,30,31,0]
    expanded_R = [R[i] for i in expanded_bits]
    for i in range(len(expanded_R)):
        expanded_R[i] = expanded_R[i] ^ key[i]
    shortened_R = ""
    for i in range(0, 48, 6):
        temp = expanded_R[i:i+6]
        temp_x = str(temp[i % 6]) + str(temp[(i % 6) + 5])
        temp_y = str(temp[(i % 6) + 1]) + str(temp[(i % 6) + 2]) + str(temp[(i % 6) + 3]) + str(temp[(i % 6) + 4])
        S_box = eval("S" + str((i // 6) + 1))
        val = S_box[binary_to_int(temp_x)][binary_to_int(temp_y)]
        shortened_R += int_to_binary(val)
    shortened_R_array = [int(i) for i in shortened_R]
    return_R_array = [shortened_R_array[R_perm[i]] for i in range(32)]
    return return_R_array

def round_key_calculator(key, round):
    l_key = key[:28]
    r_key = key[28:]
    if (round != 0 and round != 1 and round != 8 and round != 15):
        l_key = circular_shift(l_key)
        r_key = circular_shift(r_key)
    l_key = circular_shift(l_key)
    r_key = circular_shift(r_key)
    rejoin_key = l_key + r_key
    return rejoin_key

def round_key_compressor(key):
    return_key = [int(key[key_compression_table[i] - 1]) for i in range(len(key_compression_table))]
    return return_key

#------------------------------
# MAIN: Process Three Pairs
#------------------------------

encryption_results = []   # To store encryption round outputs for each pair
decryption_results = []   # To store decryption round outputs for each pair

# Test cases
test_cases = [
    {'plaintext': '0123456789ABCDEF', 'key': '133457799BBCDFF1'},
    {'plaintext': 'FEDCBA9876543210', 'key': 'AABBCCDDEEFF0011'},
    {'plaintext': '0000000000000000', 'key': 'FFFFFFFFFFFFFFFF'}
]
f=open("encryption.txt","w")
f2=open("decryption.txt","w")
for pair in range(3):
    print(f"\n=== Pair {pair+1} Encryption ===")
    
    # plaintext_input = input("Enter plaintext in hex: ")
    plaintext_input = test_cases[pair]['plaintext']
    # key_input = input("Enter key in hex: ")
    key_input = test_cases[pair]['key']

    key = hex_to_binary(key_input)
    # Removing parity bits
    key2 = ""
    for i in range(len(key)):
        if (i+1) % 8 == 0:
            continue
        key2 += key[i]
    key = key2
    key_after_perm = [key[key_perm_table[i+1]-1] for i in range(len(key))]
    key = key_after_perm
    plaintext = hex_to_binary(plaintext_input)

    # Applying initial permutation to plaintext
    plaintext_after_ip = [0]*64
    for i in range(1, 65):
        plaintext_after_ip[i-1] = int(plaintext[ip_table[i]-1])
    f.write(f"After initial permutation: {binary_to_hex(''.join(str(i) for i in plaintext_after_ip))}\n")
    print(f"After initial permutation: {binary_to_hex(''.join(str(i) for i in plaintext_after_ip))}\n")
    
    # Splitting plaintext into halves
    L = plaintext_after_ip[:32]
    R = plaintext_after_ip[32:]
    R_orig = R.copy()
    
    enc_round_outputs = []  # To store per-round outputs for encryption
    # 16 rounds of DES
    for round in range(16):
        key = round_key_calculator(key, round)
        round_key = round_key_compressor(key)
        rk = ""
        for i in round_key:
            rk += str(i)
        print(f"Round key: {binary_to_hex(rk)}")
        f.write(f"Round key: {binary_to_hex(rk)}\n")
        out = R_function(R, round_key)
        R = []
        for j in range(0, 32):
            R.append(out[j] ^ L[j])
        L = R_orig
        R_orig = R
        round_output = ""
        temp = L + R 
        for i in range(len(R+L)):
            round_output += str(temp[i])
        round_hex = binary_to_hex(round_output).upper()
        print(f"Output in Round {round+1} is {round_hex}\n")
        f.write(f"Output in Round {round+1} is {round_hex}\n")
        enc_round_outputs.append(round_hex)
    output = R + L
    final = [output[final_permutation[i+1]-1] for i in range(len(output))]
    final_str = ""
    for i in final:
        final_str += str(i)
    final_ciphertext = binary_to_hex(final_str).upper()
    print(f"Final encrypted output is {final_ciphertext}")
    f.write(f"Final encrypted output is {final_ciphertext}\n-----------------------------------------\n")
    
    encryption_results.append({
        "round_outputs": enc_round_outputs,
        "ciphertext": final_ciphertext
    })
    
    print(f"\n=== Pair {pair+1} Decryption ===")
    ciphertext_input = final_ciphertext
    key_input = test_cases[pair]['key']
    ciphertext = hex_to_binary(ciphertext_input)
    key = hex_to_binary(key_input)
    # Removing parity bits
    key2 = ""
    for i in range(len(key)):
        if (i+1) % 8 == 0:
            continue
        key2 += key[i]
    key = key2
    key_after_perm = [key[key_perm_table[i+1]-1] for i in range(len(key))]
    key = key_after_perm
    
    ciphertext_after_ip = [0]*64
    for i in range(64):
        ciphertext_after_ip[i] = int(ciphertext[ip_table[i+1]-1])
    
    subkeys = []
    for i in range(16):
        key = round_key_calculator(key, i)
        subkeys.append(round_key_compressor(key))
    
    L = ciphertext_after_ip[:32]
    R = ciphertext_after_ip[32:]
    R_orig = R.copy()
    
    dec_round_outputs = []  # To store per-round outputs for decryption
    for round in range(16):
        round_key = subkeys[15-round]
        rk = ""
        for i in round_key:
            rk += str(i)
        print(f"Round key: {binary_to_hex(rk)}")
        f2.write(f"Round key: {binary_to_hex(rk)}\n")
        out = R_function(R, round_key)
        R = []
        for j in range(0, 32):
            R.append(out[j] ^ L[j])
        L = R_orig
        R_orig = R
        round_output = ""
        temp = L + R 
        for i in range(len(R+L)):
            round_output += str(temp[i])
        round_hex = binary_to_hex(round_output).upper()
        print(f"Output in Round {round+1} is {round_hex}")
        f2.write(f"Output in Round {round+1} is {round_hex}\n")
        dec_round_outputs.append(round_hex)
    output = R + L
    final = [output[final_permutation[i+1]-1] for i in range(len(output))]
    final_str = ""
    for i in final:
        final_str += str(i)
    final_plaintext = binary_to_hex(final_str).upper()
    print(f"Final output is {final_plaintext}")
    f2.write(f"Final output is {final_plaintext}\n---------------------\n")
    decryption_results.append({
        "round_outputs": dec_round_outputs,
        "plaintext": final_plaintext
    })

f.close()
f2.close()
#------------------------------
# SUMMARY OUTPUT
#------------------------------

print("\n=== SUMMARY OF ALL PAIRS ===")
for i in range(3):
    print(f"\n--- Pair {i+1} ---")
    print("Encryption Round Outputs:")
    for r, out in enumerate(encryption_results[i]["round_outputs"]):
        print(f"  Round {r+1}: {out}")
    print("Final Ciphertext:", encryption_results[i]["ciphertext"])
    print("\nDecryption Round Outputs:")
    for r, out in enumerate(decryption_results[i]["round_outputs"]):
        print(f"  Round {r+1}: {out}")
    print("Final Decrypted Plaintext:", decryption_results[i]["plaintext"])

#------------------------------
# VERIFICATION OF ROUND OUTPUTS
#------------------------------

print("\n=== VERIFICATION OF ROUND OUTPUTS ===")
for i in range(3):
    enc_round1 = encryption_results[i]["round_outputs"][0]
    dec_round15 = decryption_results[i]["round_outputs"][15]
    if enc_round1 == dec_round15:
        print(f"Pair {i+1}: Encryption Round 1 equals Decryption Round 15: {enc_round1}")
    else:
        print(f"Pair {i+1}: MISMATCH! Encryption Round 1: {enc_round1}, Decryption Round 15: {dec_round15}")
    
    enc_round14 = encryption_results[i]["round_outputs"][14]
    dec_round2 = decryption_results[i]["round_outputs"][1]
    if enc_round14 == dec_round2:
        print(f"Pair {i+1}: Encryption Round 14 equals Decryption Round 2: {enc_round14}")
    else:
        print(f"Pair {i+1}: MISMATCH! Encryption Round 14: {enc_round14}, Decryption Round 2: {dec_round2}")
