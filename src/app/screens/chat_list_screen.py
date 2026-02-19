import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT
from ..widgets.menu_widget import MenuWidget

class ChatListScreen:
    def __init__(self, app):
        self.app = app
        self.chats = []
        
    def build(self):
        main_container = toga.ScrollContainer(style=Pack(flex=1))
        main_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        
        # Заголовок
        header = toga.Box(style=Pack(direction=ROW, margin=10))
        title = toga.Label(
            'Чаты',
            style=Pack(font_size=20, font_weight='bold', flex=1)
        )
        header.add(title)
        main_box.add(header)
        
        # Загружаем чаты в зависимости от роли пользователя
        self.load_chats()
        
        # Отображаем чаты
        for chat in self.chats:
            chat_widget = self.create_chat_widget(chat)
            main_box.add(chat_widget)
            
        # Добавляем меню
        menu = MenuWidget(self.app)
        main_box.add(menu.build())
        
        main_container.content = main_box
        return main_container
        
    def load_chats(self):
        """Загрузка чатов в зависимости от роли"""
        # В реальном приложении здесь был бы API запрос
        # Сейчас заглушка для демонстрации
        
        role = getattr(self.app.current_user, 'role', 'pupil')
        
        # Базовые чаты для всех
        base_chats = [
            {'name': 'Расписание Юг', 'unread': 3, 'icon': '📅'},
            {'name': 'Расписание Север', 'unread': 1, 'icon': '📅'}
        ]
        
        self.chats = base_chats.copy()
        
        if role == 'pupil':
            self.chats.extend([
                {'name': '7А класс', 'unread': 12, 'icon': '👥'},
                {'name': 'Математика', 'unread': 0, 'icon': '📐'},
                {'name': 'Физика', 'unread': 2, 'icon': '⚛️'}
            ])
        elif role == 'employee':
            self.chats.extend([
                {'name': 'Преподы', 'unread': 5, 'icon': '👨‍🏫'},
                {'name': 'БШ Юг', 'unread': 2, 'icon': '🏫'},
                {'name': 'БШ Север', 'unread': 0, 'icon': '🏫'}
            ])
        elif role == 'relative':
            self.chats.extend([
                {'name': 'Родительский чат 7А', 'unread': 8, 'icon': '👪'},
                {'name': 'Родительский чат 5Б', 'unread': 3, 'icon': '👪'}
            ])
            
    def create_chat_widget(self, chat):
        """Создание виджета чата"""
        chat_box = toga.Box(
            style=Pack(
                direction=ROW,
                margin=10,
                background_color='#f5f5f5' if self.chats.index(chat) % 2 == 0 else 'white'
            )
        )
        
        # Иконка чата
        icon = toga.Label(
            chat['icon'],
            style=Pack(font_size=24, width=40, text_align='center')
        )
        chat_box.add(icon)
        
        # Информация о чате
        info_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        name_label = toga.Label(
            chat['name'],
            style=Pack(font_weight='bold', font_size=16)
        )
        info_box.add(name_label)
        
        # Последнее сообщение (заглушка)
        last_msg = toga.Label(
            'Последнее сообщение...',
            style=Pack(color='#666666', font_size=12)
        )
        info_box.add(last_msg)
        
        chat_box.add(info_box)
        
        # Счетчик непрочитанных
        if chat['unread'] > 0:
            unread_box = toga.Box(
                style=Pack(
                    background_color='#4A90E2',
                    width=25,
                    height=25,
                    alignment='center'
                )
            )
            unread_box.add(
                toga.Label(
                    str(chat['unread']),
                    style=Pack(color='white', font_size=12)
                )
            )
            chat_box.add(unread_box)
            
        # Кнопка открытия чата
        chat_box.on_press = lambda w, c=chat: self.open_chat(c)
        
        return chat_box
        
    def open_chat(self, chat):
        """Открытие выбранного чата"""
        self.app.show_chat('chat_id_123', chat['name'])