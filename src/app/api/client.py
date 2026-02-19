import json
import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin

class APIClient:
    def __init__(self, base_url="https://vzmakh.su/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = None
        
    def set_auth_token(self, token):
        self.auth_token = token
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        
    def _request(self, method, endpoint, data=None, params=None):
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'status': 'error'}
            
    def register(self, user_data):
        """Регистрация пользователя"""
        return self._request('POST', '/auth/register', data=user_data)
        
    def verify_pin(self, user_id, pin_code):
        """Проверка пин-кода"""
        return self._request('POST', '/auth/verify-pin', 
                            data={'user_id': user_id, 'pin_code': pin_code})
    
    def register_public_key(self, key_data):
        """Регистрация публичного ключа"""
        return self._request('POST', '/keys/register', data=key_data)
    
    def get_public_key(self, user_id):
        """Получение публичного ключа пользователя"""
        return self._request('GET', f'/keys/{user_id}')
    
    def get_chats(self):
        """Получение списка чатов пользователя"""
        return self._request('GET', '/chats')
    
    def get_chat_messages(self, chat_id, limit=50, offset=0):
        """Получение сообщений чата"""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', f'/chats/{chat_id}/messages', params=params)
    
    def send_message(self, message_data):
        """Отправка зашифрованного сообщения"""
        return self._request('POST', '/messages/send', data=message_data)
    
    def check_registration(self, check_data):
        """Проверка регистрации по спискам"""
        return self._request('POST', '/registration/check', data=check_data)
    
    def manual_registration_request(self, request_data):
        """Запрос на ручную регистрацию"""
        return self._request('POST', '/registration/manual-request', data=request_data)
    
    def get_digest(self):
        """Получение последних сообщений из дайджеста"""
        return self._request('GET', '/digest/latest')
    
    def get_branches(self):
        """Получение списка филиалов"""
        return self._request('GET', '/branches')
    
    def get_classes(self, branch_id):
        """Получение списка классов для филиала"""
        return self._request('GET', f'/branches/{branch_id}/classes')
    
    def subscribe_to_chat(self, chat_id):
        """Подписка на чат"""
        return self._request('POST', f'/chats/{chat_id}/subscribe')
    
    def get_menu_items(self):
        """Получение пунктов меню"""
        return self._request('GET', '/menu/items')