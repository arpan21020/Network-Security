import rsa_utils
import zmq
import threading
import json
from datetime import datetime, timedelta

class CertificationAuthority:
    def __init__(self, host="*", port=5555):
        # CA's own keypair
        p = rsa_utils.generate_prime(1000, 5000)
        q = rsa_utils.generate_prime(1000, 5000)
        self.private_key, self.public_key = rsa_utils.generate_keypair(p, q)
        
        # Store client certificates (not just public keys)
        self.client_certificates = {}
        
        # CA identifier
        self.id = "MAIN_CA_2025"
        
        # ZMQ setup
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://{host}:{port}")
        print(f"Server listening on tcp://{host}:{port}")
        # Start server thread
        self.running = True
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.start()
        
    def _run_server(self):
        """Main server loop to handle client requests."""
        while self.running:
            try:
                message = self.socket.recv_json()
                print("Message recieved:",message)
                response = self._handle_request(message)
                self.socket.send_json(response)
            except zmq.ZMQError:
                if self.running:
                    raise
                break
    
    def _handle_request(self, message):
        """Handle incoming client requests."""
        action = message.get('action')
        client_id = message.get('client_id')
        data = message.get('data', {})
        
        try:
            if action == 'register':
                public_key = data['public_key']
                port=data['port']
                # Generate and store certificate immediately during registration
                certificate = self.generate_certificate(client_id, public_key,port)
                self.client_certificates[client_id] = certificate
                # print(self.client_certificates)
                with open("certificate_logs.txt","w") as f:
                    json.dump(self.client_certificates,f,indent=4)
                return {'status': 'success','authority_key':self.public_key,'message': 'Client registered and certificate generated'}
                
            elif action == 'get_certificate':
                # Return the full certificate instead of just public key
                target_client_id=data["target_client_id"]
                certificate = self.client_certificates.get(target_client_id)
                if certificate:
                    return {'status': 'success', 'certificate': certificate}
                return {'status': 'error', 'message': 'Certificate not found'}
                
            elif action == 'verify_certificate':
                cert = data['certificate']
                valid, cert_data = self.verify_certificate(cert)
                return {
                    'status': 'success',
                    'valid': valid,
                    'cert_data': cert_data if valid else None
                }
                
            else:
                return {'status': 'error', 'message': 'Invalid action'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def stop(self):
        """Stop the server."""
        self.running = False
        self.socket.close()
        self.context.term()
        self.server_thread.join()
    
    def generate_certificate(self, client_id, client_public_key, port ,duration_seconds=3600):
        """Generate a certificate for a client."""
        timestamp = int(rsa_utils.time.time())
        
        cert_data = {
            'client_id': client_id,
            'public_key': client_public_key,
            'port':port,
            'timestamp': timestamp,
            'duration': duration_seconds,
            'ca_id': self.id
        }
        
        # Encrypt certificate contents with CA's private key
        # encoded_cert_data = str(cert_data).encode()
        encrypted_cert = rsa_utils.encrypt(self.private_key, str(cert_data))
        
        certificate = {
            'plain_data': cert_data,
            'encrypted_data': encrypted_cert
        }
        
        return certificate
    
    
if __name__=="__main__":
    ca=CertificationAuthority()