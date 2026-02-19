import json
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class KeyManager:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.keys = {}
        
    def save_keys(self, user_id, key_pair):
        """Сохранение ключей пользователя"""
        key_data = {
            'key_id': key_pair['key_id'],
            'private_key': key_pair['private_key'].private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode(),
            'public_key': key_pair['public_key'].public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
        }
        
        os.makedirs(self.storage_path, exist_ok=True)
        with open(f"{self.storage_path}/{user_id}_keys.json", 'w') as f:
            json.dump(key_data, f)
            
    def load_keys(self, user_id):
        """Загрузка ключей пользователя"""
        try:
            with open(f"{self.storage_path}/{user_id}_keys.json", 'r') as f:
                key_data = json.load(f)
                
            private_key = serialization.load_pem_private_key(
                key_data['private_key'].encode(),
                password=None,
                backend=default_backend()
            )
            public_key = serialization.load_pem_public_key(
                key_data['public_key'].encode(),
                backend=default_backend()
            )
            
            return {
                'key_id': key_data['key_id'],
                'private_key': private_key,
                'public_key': public_key
            }
        except FileNotFoundError:
            return None