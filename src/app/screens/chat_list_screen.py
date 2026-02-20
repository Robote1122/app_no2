import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT, CENTER
from ..widgets.menu_widget import MenuWidget
from ..styles import MobileStyles

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
        # Карточка чата
        chat_box = toga.Box(style=Pack(
            direction=ROW,
            background_color='white',
            margin=(5, 10),
            padding=10,
            border_width=1,
            border_color='#e0e0e0',
            border_radius=8,
            width=360
        ))
        
        # Аватар
        avatar = toga.Box(style=Pack(
            width=50,
            height=50,
            background_color='#4A90E2',
            border_radius=25,
            alignment=CENTER
        ))
        avatar.add(toga.Label(chat['icon'], style=Pack(font_size=24)))
        chat_box.add(avatar)
        
        # Информация о чате
        info_box = toga.Box(style=Pack(direction=COLUMN, flex=1, padding_left=10))
        name_label = toga.Label(
            chat['name'],
            style=Pack(font_weight='bold', font_size=16)
        )
        info_box.add(name_label)
        
        last_msg = toga.Label(
            'Последнее сообщение...',
            style=Pack(color='#666666', font_size=12)
        )
        info_box.add(last_msg)
        chat_box.add(info_box)
        
        # Счетчик и время
        right_box = toga.Box(style=Pack(direction=COLUMN, alignment=RIGHT))
        
        time_label = toga.Label('12:30', style=Pack(font_size=10, color='#999'))
        right_box.add(time_label)
        
        if chat['unread'] > 0:
            unread = toga.Box(style=Pack(
                background_color='#4A90E2',
                width=22,
                height=22,
                border_radius=11,
                alignment=CENTER,
                margin_top=5
            ))
            unread.add(toga.Label(
                str(chat['unread']),
                style=Pack(color='white', font_size=10)
            ))
            right_box.add(unread)
        
        chat_box.add(right_box)
        
        # Добавляем обработчик нажатия
        chat_box.on_press = lambda w, c=chat: self.open_chat(c)
        
        return chat_box
        
    def open_chat(self, chat):
        """Открытие выбранного чата"""
        self.app.show_chat('chat_id_123', chat['name'])