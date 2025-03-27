import rsa_utils

class Client:
    def __init__(self, client_id, certification_authority):
        # Client's own identity
        self.id = client_id
        
        # CA reference
        self.ca = certification_authority
        
        # Generate client's keypair
        p = rsa_utils.generate_prime(1000, 5000)
        q = rsa_utils.generate_prime(1000, 5000)
        self.private_key, self.public_key = rsa_utils.generate_keypair(p, q)
        
        # Register with CA
        self.ca.register_client(self.id, self.public_key)
        
        # Get own certificate
        self.certificate = self.ca.generate_certificate(
            self.id, 
            self.public_key, 
            duration_seconds=3600  # 1-hour validity
        )
        
        # Store other clients' certificates and public keys
        self.other_certificates = {}
        self.other_public_keys = {}
    
    def request_client_certificate(self, target_client_id):
        """Request another client's certificate from CA."""
        # Get certificate from CA
        target_certificate = self.ca.get_client_certificate(target_client_id)
        
        if target_certificate:
            # Verify certificate
            is_valid, cert_data = self.ca.verify_certificate(target_certificate)
            
            if is_valid:
                self.other_certificates[target_client_id] = target_certificate
                self.other_public_keys[target_client_id] = cert_data['public_key']
                return True
        
        return False
    
    def send_encrypted_message(self, target_client_id, message):
        """Encrypt and send a message to another client."""
        if target_client_id not in self.other_public_keys:
            # Try to get certificate first
            if not self.request_client_certificate(target_client_id):
                raise ValueError(f"Cannot send message. No certificate for {target_client_id}")
        
        # Encrypt message with target's public key
        encrypted_message = rsa_utils.encrypt(
            self.other_public_keys[target_client_id], 
            message
        )
        
        return encrypted_message
    
    def receive_encrypted_message(self, encrypted_message):
        """Decrypt a received message."""
        decrypted_message = rsa_utils.decrypt(
            self.private_key, 
            encrypted_message
        )
        
        return decrypted_message