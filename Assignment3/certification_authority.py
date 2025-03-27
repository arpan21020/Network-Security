import rsa_utils
import base64

class CertificationAuthority:
    def __init__(self):
        # CA's own keypair
        p = rsa_utils.generate_prime(1000, 5000)
        q = rsa_utils.generate_prime(1000, 5000)
        self.private_key, self.public_key = rsa_utils.generate_keypair(p, q)
        
        # Store client certificates
        self.client_certificates = {}
        self.client_public_keys = {}
        
        # CA identifier
        self.id = "MAIN_CA_2025"
    
    def register_client(self, client_id, client_public_key):
        """Register a client's public key."""
        self.client_public_keys[client_id] = client_public_key
    
    def generate_certificate(self, client_id, client_public_key, duration_seconds=3600):
        """Generate a certificate for a client."""
        # Current timestamp
        timestamp = int(rsa_utils.time.time())
        
        # Certificate contents
        cert_data = {
            'client_id': client_id,
            'public_key': client_public_key,
            'timestamp': rsa_utils.encode_timestamp(timestamp),
            'duration': duration_seconds,
            'ca_id': self.id
        }
        
        # Encrypt certificate contents with CA's private key
        encoded_cert_data = str(cert_data).encode()
        encrypted_cert = rsa_utils.encrypt(self.private_key, encoded_cert_data.decode())
        
        # Construct full certificate
        certificate = {
            'plain_data': cert_data,
            'encrypted_data': encrypted_cert
        }
        
        # Store certificate
        self.client_certificates[client_id] = certificate
        
        return certificate
    
    def verify_certificate(self, certificate):
        """Verify a certificate's authenticity and validity."""
        try:
            # Decrypt with CA's public key
            decrypted_data = rsa_utils.decrypt(self.public_key, certificate['encrypted_data'])
            cert_data = eval(decrypted_data)
            
            # Check timestamp validity
            timestamp = rsa_utils.decode_timestamp(cert_data['timestamp'])
            valid = rsa_utils.is_timestamp_valid(timestamp, cert_data['duration'])
            
            return valid, cert_data
        except Exception as e:
            return False, None
    
    def get_client_certificate(self, client_id):
        """Retrieve a client's certificate."""
        return self.client_certificates.get(client_id)
    
    def get_client_public_key(self, client_id):
        """Retrieve a client's public key."""
        return self.client_public_keys.get(client_id)