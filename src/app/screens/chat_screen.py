import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from datetime import datetime
import os
import asyncio

from ..crypto.e2ee import E2EECrypto
from ..widgets.menu_widget import MenuWidget

class ChatScreen:
    def __init__(self, app, chat_id, chat_name):
        self.app = app
        self.chat_id = chat_id
        self.chat_name = chat_name
        self.messages = []
        self.subscribers = []
        self.pinned_message = None
    def handle_swipe(self, event):
        """Обработка свайпа влево для возврата"""
        # В Toga нет встроенной поддержки свайпов,
        # но можно использовать аппаратную кнопку "назад" на Android
        pass
        
    def build(self):
        # Основной контейнер
        main_container = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        # Верхняя панель с названием чата
        header = toga.Box(style=Pack(direction=ROW, margin=10, background_color='#f0f0f0'))
        
        back_button = toga.Button(
            '←',
            on_press=self.go_back,
            style=Pack(width=40, background_color='#f0f0f0')
        )
        
        chat_title = toga.Label(
            self.chat_name,
            style=Pack(flex=1, font_size=18, font_weight='bold')
        )
        
        # Кнопки управления чатом
        info_button = toga.Button(
            'ℹ️',
            on_press=self.show_chat_info,
            style=Pack(width=40, background_color='#f0f0f0')
        )
        
        subscribers_button = toga.Button(
            '👥',
            on_press=self.show_subscribers,
            style=Pack(width=40, background_color='#f0f0f0')
        )
        
        header.add(back_button)
        header.add(chat_title)
        header.add(info_button)
        header.add(subscribers_button)
        
        # Область сообщений
        self.message_container = toga.ScrollContainer(style=Pack(flex=1))
        self.message_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        self.message_container.content = self.message_box
        
        # Закрепленное сообщение (если есть)
        self.pinned_box = toga.Box(
            style=Pack(
                direction=ROW,
                margin=5,
                background_color='#fff3cd',
                visibility='hidden'
            )
        )
        
        # Область ввода сообщения
        input_area = toga.Box(style=Pack(direction=ROW, margin=10))
        
        self.message_input = toga.MultilineTextInput(
            placeholder='Введите сообщение...',
            style=Pack(flex=1, height=60)
        )
        
        attach_button = toga.Button(
            '📎',
            on_press=self.attach_file,
            style=Pack(width=40, margin=(0, 5))
        )
        
        send_button = toga.Button(
            'Отправить',
            on_press=self.send_message,
            style=Pack(margin_left=5)
        )
        
        input_area.add(self.message_input)
        input_area.add(attach_button)
        input_area.add(send_button)
        
        # Меню (доступно всегда)
        menu = MenuWidget(self.app).build()
        
        # Сборка основного контейнера
        main_container.add(header)
        main_container.add(self.pinned_box)
        main_container.add(self.message_container)
        main_container.add(input_area)
        main_container.add(menu)
        
        # Загружаем сообщения
        self.app.add_background_task(self.load_messages)
        
        return main_container
        
    async def load_messages(self, widget, **kwargs):
        """Загрузка сообщений чата"""
        # В реальном приложении здесь был бы API запрос
        # Заглушка для демонстрации
        await asyncio.sleep(0.5)
        
        mock_messages = [
            {'text': 'Привет всем!', 'sender': 'user1', 'time': '10:30', 'encrypted': False},
            {'text': 'Как дела?', 'sender': 'user2', 'time': '10:31', 'encrypted': False},
            {'text': 'Завтра собрание в 18:00', 'sender': 'user1', 'time': '10:32', 'encrypted': False},
        ]
        
        for msg in mock_messages:
            self.add_message_to_ui(
                msg['text'],
                msg['sender'],
                msg['time']
            )
            
    def add_message_to_ui(self, text, sender_id, timestamp, is_encrypted=True):
        """Добавление сообщения в UI"""
        message_box = toga.Box(style=Pack(direction=COLUMN, margin=5, width=300))
        
        # Определяем, свое сообщение или чужое
        is_own = sender_id == getattr(self.app.current_user, 'id', None)
        
        # Контейнер сообщения
        msg_container = toga.Box(style=Pack(
            direction=COLUMN,
            background_color='#e3f2fd' if is_own else '#f5f5f5',
            margin=10,
            width=280
        ))
        
        # Заголовок (отправитель и время)
        header = toga.Box(style=Pack(direction=ROW))
        
        sender_label = toga.Label(
            'Вы' if is_own else sender_id,
            style=Pack(font_weight='bold', font_size=12)
        )
        
        time_label = toga.Label(
            timestamp,
            style=Pack(flex=1, text_align=RIGHT, font_size=10, color='#666')
        )
        
        header.add(sender_label)
        header.add(time_label)
        
        # Текст сообщения
        if is_encrypted:
            text = '🔒 ' + text
            
        message_text = toga.Label(
            text,
            style=Pack(margin_top=5, font_size=14)
        )
        
        # Кнопки взаимодействия с сообщением
        actions = toga.Box(style=Pack(direction=ROW, margin_top=5))
        
        reply_btn = toga.Button(
            '↩️',
            on_press=lambda x, t=text: self.reply_to_message(t),
            style=Pack(width=30, background_color='transparent')
        )
        
        react_btn = toga.Button(
            '👍',
            on_press=lambda x, t=text: self.add_reaction(t),
            style=Pack(width=30, background_color='transparent')
        )
        
        forward_btn = toga.Button(
            '↗️',
            on_press=lambda x, t=text: self.forward_message(t),
            style=Pack(width=30, background_color='transparent')
        )
        
        actions.add(reply_btn)
        actions.add(react_btn)
        actions.add(forward_btn)
        
        # Если пользователь администратор, добавляем кнопку удаления
        if self.is_admin():
            delete_btn = toga.Button(
                '🗑️',
                on_press=lambda x, t=text: self.delete_message(t),
                style=Pack(width=30, background_color='transparent')
            )
            actions.add(delete_btn)
            
        msg_container.add(header)
        msg_container.add(message_text)
        msg_container.add(actions)
        
        # Выравнивание (свои справа, чужие слева)
        if is_own:
            message_box.style.alignment = RIGHT
        else:
            message_box.style.alignment = LEFT
            
        message_box.add(msg_container)
        self.message_box.add(message_box)
        
        # Прокрутка вниз к новому сообщению
        # В Toga нет прямого метода прокрутки, но можно обновить
        self.message_container.vertical_position = 1.0
        
    def send_message(self, widget):
        """Отправка сообщения"""
        text = self.message_input.value
        if not text:
            return
            
        # Шифруем сообщение (в реальном приложении)
        # encrypted = E2EECrypto.encrypt_message(text, recipient_public_key)
        
        # Отправляем через API
        message_data = {
            'chat_id': self.chat_id,
            'sender_id': self.app.current_user.get('id', 'current_user'),
            'text': text,  # В реальном приложении здесь будет зашифрованные данные
            'timestamp': datetime.now().strftime('%H:%M')
        }
        
        # response = self.app.api_client.send_message(message_data)
        
        # Добавляем в UI
        self.add_message_to_ui(
            text,
            'current_user',
            datetime.now().strftime('%H:%M'),
            False
        )
        
        # Очищаем поле ввода
        self.message_input.value = ''
        
    def attach_file(self, widget):
        """Прикрепление файла"""
        # В реальном приложении здесь был бы выбор файла
        self.app.main_window.info_dialog(
            'Прикрепление файла',
            'Выберите файл для прикрепления'
        )
        
    def reply_to_message(self, text):
        """Ответ на сообщение"""
        self.message_input.value = f'[Ответ] {text}\n'
        self.message_input.focus()
        
    def add_reaction(self, text):
        """Добавление реакции"""
        self.app.main_window.info_dialog('Реакция', f'👍 на сообщение: {text[:30]}...')
        
    def forward_message(self, text):
        """Пересылка сообщения"""
        self.app.main_window.info_dialog('Пересылка', 'Выберите чат для пересылки')
        
    def delete_message(self, text):
        """Удаление сообщения (для админов)"""
        self.app.main_window.question_dialog(
            'Удаление',
            'Удалить это сообщение?',
            on_result=lambda x: self.confirm_delete(x, text)
        )
        
    def confirm_delete(self, confirmed, text):
        """Подтверждение удаления"""
        if confirmed:
            self.app.main_window.info_dialog('Удалено', 'Сообщение удалено')
            
    def show_chat_info(self, widget):
        """Показать информацию о чате"""
        info_text = f"""
Название: {self.chat_name}
ID чата: {self.chat_id}
Участников: 15
Создан: 01.09.2023
        """
        self.app.main_window.info_dialog('Информация о чате', info_text)
        
    def show_subscribers(self, widget):
        """Показать список подписчиков"""
        # Заглушка
        subscribers = [
            'Иванов Иван (ученик)',
            'Петрова Мария (учитель)',
            'Сидоров Петр (родитель)'
        ]
        
        sub_text = '\n'.join(subscribers)
        self.app.main_window.info_dialog('Подписчики', sub_text)
        
    def is_admin(self):
        """Проверка, является ли пользователь администратором"""
        # В реальном приложении проверять по роли
        return True  # Заглушка
        
    def go_back(self, widget):
        """Возврат к списку чатов"""
        self.app.show_chat_list()