import rsa_utils
import zmq
import json
import sys

class Client:
    def __init__(self, client_id, ca_host="localhost", ca_port=5555):
        self.id = client_id
        self.context = zmq.Context()
        self.ca_socket = self.context.socket(zmq.REQ)
        self.ca_socket.connect(f"tcp://{ca_host}:{ca_port}")
        
        # Generate client's keypair
        p = rsa_utils.generate_prime(1000, 5000)
        q = rsa_utils.generate_prime(1000, 5000)
        self.private_key, self.public_key = rsa_utils.generate_keypair(p, q)
        self.public_key_authority=None
        
        # Create a REP socket to receive messages
        self.receiver_socket = self.context.socket(zmq.REP)
        self.receiver_port = 6000 + int(client_id)  # Assign unique port based on client ID
        self.receiver_socket.bind(f"tcp://*:{self.receiver_port}")
        
        # Register with CA (this now generates and stores certificate)
        response = self._send_to_ca('register', {'public_key': self.public_key, 'port': self.receiver_port})
        if response['status'] != 'success':
            raise Exception("Failed to register with CA")
        else:
            self.public_key_authority=response['authority_key']
                    
        # Store other clients' certificates and their ports
        self.other_certificates = {}
        self.client_ports = {}  # To store other clients' ports
    
    def _send_to_ca(self, action, data=None):
        """Send a request to the CA and return the response."""
        if data is None:
            data = {}
            
        request = {
            'action': action,
            'client_id': self.id,
            'data': data
        }
        print("Request : ", request)
        
        self.ca_socket.send_json(request)
        response = self.ca_socket.recv_json()
        print("Response : ",response)
        return response
    
    def close(self):
        """Clean up ZMQ resources."""
        self.ca_socket.close()
        self.receiver_socket.close()
        self.context.term()
    
    def verify_certificate(self, certificate):
        """Verify a certificate's authenticity and validity."""
        try:
            # Decrypt with CA's public key
            decrypted_data = rsa_utils.decrypt(self.public_key_authority, certificate['encrypted_data'])
            cert_data = eval(decrypted_data)
            
            
            if str(decrypted_data)==str(certificate['plain_data']):
                valid=True
            print("Verified......")
            return valid, cert_data
        except Exception as e:
            print("error raised:",e)
            return False, None
        
    def get_client_certificate(self, target_client_id):
        """Request and verify another client's certificate from CA."""
        # Get certificate from CA
        response = self._send_to_ca('get_certificate', {'target_client_id': target_client_id})
        
        if response['status'] == 'success':
            certificate = response['certificate']
            print("verifying..............")
            # Verify the certificate
            verify_response_valid, verify_response_data = self.verify_certificate(response['certificate'])
            
            if verify_response_valid:
                self.other_certificates[target_client_id] = certificate
                self.client_ports[target_client_id] = certificate['plain_data']['port']
                return True
        return False
    
    def send_encrypted_message(self, target_client_id, message):
        """Encrypt and send a message to another client."""
        if target_client_id not in self.other_certificates:
            # Try to get certificate first
            if not self.get_client_certificate(target_client_id):
                raise ValueError(f"Cannot send message. No valid certificate for {target_client_id}")
        
        # Get public key from verified certificate
        target_cert = self.other_certificates[target_client_id]
        target_public_key = target_cert['plain_data']['public_key']
        
        # Encrypt message with target's public key
        encrypted_message = rsa_utils.encrypt(target_public_key, message)
        
        # Create a REQ socket for sending the message
        sender_socket = self.context.socket(zmq.REQ)
        target_port = self.client_ports[target_client_id]
        sender_socket.connect(f"tcp://localhost:{target_port}")
        
        # Send the encrypted message
        sender_socket.send_json({
            'sender_id': self.id,
            'message': encrypted_message
        })
        
        # Wait for acknowledgment
        ack = sender_socket.recv_json()
        sender_socket.close()
        
        return ack
    
    def receive_encrypted_message(self):
        """Receive and decrypt a message."""
        # Wait for incoming message
        request = self.receiver_socket.recv_json()
        sender_id = request['sender_id']
        encrypted_message = request['message']
        
        # Decrypt the message
        decrypted_message = rsa_utils.decrypt(self.private_key, encrypted_message)
        
        # Send acknowledgment
        self.receiver_socket.send_json({'status': 'received'})
        
        return sender_id, decrypted_message

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: python client.py <client_id>")
        sys.exit(1)

    client_id = sys.argv[1]
    client = Client(client_id)
    
    try:
        while True:
            print("\n*********Menu*********")
            print("1) Request certificate")
            print("2) Send message to some client")
            print("3) Check for incoming messages")
            print("4) Exit")
            
            x = int(input("Enter option: "))
            
            if x == 1:
                target_client = input("Enter target client_id: ")
                client.get_client_certificate(target_client)
            
            elif x == 2:
                target_client = input("Enter target client_id: ")
                msg = input("Enter message to send: ")
                try:
                    ack = client.send_encrypted_message(target_client, msg)
                    print(f"Message sent. Acknowledgment: {ack}")
                except Exception as e:
                    print(f"Error sending message: {e}")
            
            elif x == 3:
                print("Checking for messages (waiting for 5 seconds)...")
                # Set a timeout for receiving messages
                client.receiver_socket.RCVTIMEO = 5000  # 5 seconds in milliseconds
                try:
                    sender_id, message = client.receive_encrypted_message()
                    print(f"\nReceived message from {sender_id}: {message}")
                except zmq.Again:
                    print("No messages received within the timeout period.")
            
            elif x == 4:
                break
            
            else:
                print("Invalid option. Please try again.")
    
    finally:
        client.close()