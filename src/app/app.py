import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os
import asyncio
from cryptography.hazmat.primitives import serialization

from .screens.loading_screen import LoadingScreen
from .screens.pin_screen import PinScreen
from .screens.main_screen import MainScreen
from .screens.registration_screen import RegistrationScreen
from .screens.completion_screen import CompletionScreen
from .screens.chat_list_screen import ChatListScreen
from .screens.chat_screen import ChatScreen
from .api.client import APIClient
from .crypto.key_manager import KeyManager
from .crypto.e2ee import E2EECrypto

class VzmakhApp(toga.App):
    def __init__(self):
        super().__init__(
            formal_name='Взмах',
            app_id='su.vzmakh.app',
            app_name='vzmakh_app'
        )
        self.api_client = APIClient()
        self.key_manager = None
        self.current_user = None
        self.is_registered = False
        
    def startup(self):
        # Инициализация главного окна
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Создаем директорию для хранения ключей
        keys_path = os.path.join(self.paths.data, 'keys')
        self.key_manager = KeyManager(keys_path)
        
        # Показываем экран загрузки
        self.show_loading_screen()

        self.add_background_task(self.check_registration_status)
        
    def show_loading_screen(self):
        """Показ экрана загрузки"""
        loading_screen = LoadingScreen(self)
        self.main_window.content = loading_screen.build()
        self.main_window.show()
        
        self.add_background_task(self.check_registration_status)
        
    async def check_registration_status(self, widget, **kwargs):
        """Проверка статуса регистрации"""
        await asyncio.sleep(2)
        
        # Проверяем, есть ли сохраненные ключи
        # В реальном приложении здесь была бы проверка токена и т.д.
        saved_user_id = None  # Заглушка
        
        if saved_user_id and self.key_manager.load_keys(saved_user_id):
            self.current_user = {'id': saved_user_id}
            self.is_registered = True
            self.show_pin_screen()
        else:
            self.show_main_screen()
            
    def show_pin_screen(self):
        """Показ экрана ввода пин-кода"""
        pin_screen = PinScreen(self)
        self.main_window.content = pin_screen.build()
        
    def show_main_screen(self):
        """Показ главного экрана"""
        main_screen = MainScreen(self, is_registered=self.is_registered)
        self.main_window.content = main_screen.build()
        
    def show_registration_screen(self):
        """Показ экрана регистрации"""
        reg_screen = RegistrationScreen(self)
        self.main_window.content = reg_screen.build()
        
    def show_completion_screen(self, registration_data, found_in_list=True):
        """Показ экрана завершения регистрации"""
        completion_screen = CompletionScreen(self, registration_data, found_in_list)
        self.main_window.content = completion_screen.build()
        
    def show_chat_list(self):
        """Показ списка чатов"""
        chat_list_screen = ChatListScreen(self)
        self.main_window.content = chat_list_screen.build()
        
    def show_chat(self, chat_id, chat_name):
        """Показ конкретного чата"""
        chat_screen = ChatScreen(self, chat_id, chat_name)
        self.main_window.content = chat_screen.build()
        
    def handle_registration_complete(self, user_data):
        """Обработка завершения регистрации"""
        self.current_user = user_data
        self.is_registered = True
        
        # Генерируем и сохраняем ключи
        key_pair = E2EECrypto.generate_key_pair()
        self.key_manager.save_keys(user_data['id'], key_pair)
        
        # Отправляем публичный ключ на сервер
        self.api_client.register_public_key({
            'user_id': user_data['id'],
            'public_key': key_pair['public_key'].public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode(),
            'key_id': key_pair['key_id']
        })
        
        self.show_main_screen()

def main():
    return VzmakhApp()

if __name__ == '__main__':
    main().main_loop()