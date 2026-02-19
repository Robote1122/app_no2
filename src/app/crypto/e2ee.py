import os
import hashlib
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class E2EECrypto:
    @staticmethod
    def generate_key_pair():
        """Генерация пары ключей RSA"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        # Генерация ID из публичного ключа
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        key_id = hashlib.sha256(public_bytes).hexdigest()[:16]
        
        return {
            'private_key': private_key,
            'public_key': public_key,
            'key_id': key_id
        }
    
    @staticmethod
    def encrypt_message(message, recipient_public_key):
        """Шифрование сообщения для получателя"""
        # Генерируем симметричный ключ для сообщения
        session_key = os.urandom(32)
        iv = os.urandom(16)
        
        # Шифруем сообщение симметричным ключом
        cipher = Cipher(algorithms.AES(session_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
        
        # Шифруем симметричный ключ публичным ключом получателя
        encrypted_key = recipient_public_key.encrypt(
            session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return {
            'encrypted_key': base64.b64encode(encrypted_key).decode(),
            'iv': base64.b64encode(iv).decode(),
            'encrypted_message': base64.b64encode(encrypted_message).decode()
        }
    
    @staticmethod
    def decrypt_message(encrypted_data, private_key):
        """Дешифровка сообщения"""
        encrypted_key = base64.b64decode(encrypted_data['encrypted_key'])
        iv = base64.b64decode(encrypted_data['iv'])
        encrypted_message = base64.b64decode(encrypted_data['encrypted_message'])
        
        # Расшифровываем симметричный ключ
        session_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Расшифровываем сообщение
        cipher = Cipher(algorithms.AES(session_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
        
        return decrypted_message.decode()