from certification_authority import CertificationAuthority
from client import Client

def main():
    # Create Certification Authority
    ca = CertificationAuthority()
    
    # Create two clients
    client_a = Client("CLIENT_A", ca)
    client_b = Client("CLIENT_B", ca)
    
    # Demonstrate secure messaging
    try:
        # Client A sends a message to Client B
        secret_message = "Hello, this is a confidential message!"
        encrypted_msg = client_a.send_encrypted_message("CLIENT_B", secret_message)
        
        # Client B receives and decrypts the message
        received_msg = client_b.receive_encrypted_message(encrypted_msg)
        
        print("Original Message:", secret_message)
        print("Received Message:", received_msg)
        print("Message transmission successful!")
        
        # Verify certificate
        is_valid, cert_data = ca.verify_certificate(client_a.certificate)
        print("\nClient A Certificate Details:")
        print("Valid:", is_valid)
        print("Certificate Data:", cert_data)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()