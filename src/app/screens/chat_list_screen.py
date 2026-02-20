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
        main_container = toga.ScrollContainer(
            style=Pack(flex=1, background_color=MobileStyles.COLORS['background'])
        )
        
        outer_box = toga.Box(style=Pack(direction=COLUMN, alignment='center'))
        main_box = toga.Box(style=Pack(
            direction=COLUMN,
            width=380,
            margin=(0, 'auto')
        ))
        
        # Заголовок с поиском
        header = toga.Box(style=MobileStyles.header())
        header.add(
            toga.Label(
                '💬 Чаты',
                style=Pack(
                    font_size=24,
                    font_weight='bold',
                    color=MobileStyles.COLORS['text'],
                    flex=1
                )
            )
        )
        
        # Кнопка создания нового чата
        new_chat_btn = toga.Button(
            '➕',
            on_press=self.new_chat,
            style=Pack(
                width=44,
                height=44,
                background_color='transparent',
                font_size=24,
                border_radius=22
            )
        )
        header.add(new_chat_btn)
        main_box.add(header)
        
        # Поиск
        search_box = toga.Box(style=Pack(margin=10))
        search_input = toga.TextInput(
            placeholder='🔍 Поиск по чатам...',
            style=Pack(
                width=360,
                padding=12,
                border_width=1,
                border_color=MobileStyles.COLORS['border'],
                border_radius=20,
                background_color='white'
            )
        )
        search_box.add(search_input)
        main_box.add(search_box)
        
        # Статистика
        stats_box = toga.Box(style=Pack(
            direction=ROW,
            margin=(5, 10, 15, 10)
        ))
        stats_box.add(
            toga.Label(
                'Всего чатов: 8',
                style=Pack(
                    font_size=12,
                    color='#666',
                    margin_right=15
                )
            )
        )
        stats_box.add(
            toga.Label(
                'Непрочитанных: 15',
                style=Pack(
                    font_size=12,
                    color=MobileStyles.COLORS['primary'],
                    font_weight='bold'
                )
            )
        )
        main_box.add(stats_box)
        
        # Загружаем чаты
        self.load_chats()
        
        # Отображаем чаты
        for chat in self.chats:
            chat_widget = self.create_chat_widget(chat)
            main_box.add(chat_widget)
        
        outer_box.add(main_box)
        outer_box.add(MenuWidget(self.app).build())
        main_container.content = outer_box
        return main_container
    
    def create_chat_widget(self, chat):
        chat_box = toga.Box(style=Pack(
            direction=ROW,
            background_color='white',
            margin=(5, 10),
            padding=12,
            border_width=1,
            border_color=MobileStyles.COLORS['border'],
            border_radius=12,
            width=360
        ))
        
        # Аватар с эмодзи
        avatar = toga.Box(style=MobileStyles.avatar(50))
        avatar.add(
            toga.Label(
                chat['icon'],
                style=Pack(font_size=24, color='white')
            )
        )
        chat_box.add(avatar)
        
        # Информация о чате
        info_box = toga.Box(style=Pack(direction=COLUMN, flex=1, padding_left=12))
        
        name_box = toga.Box(style=Pack(direction=ROW, margin_bottom=4))
        name_label = toga.Label(
            chat['name'],
            style=Pack(font_weight='bold', font_size=16)
        )
        name_box.add(name_label)
        
        # Последнее сообщение
        last_msg = toga.Label(
            chat.get('last_message', 'Последнее сообщение...'),
            style=Pack(
                color='#666666',
                font_size=13,
                lines=1
            )
        )
        
        info_box.add(name_box)
        info_box.add(last_msg)
        chat_box.add(info_box)
        
        # Правая часть (время и непрочитанные)
        right_box = toga.Box(style=Pack(direction=COLUMN, alignment='center'))
        
        time_label = toga.Label(
            chat.get('time', '12:30'),
            style=Pack(font_size=11, color='#999', margin_bottom=5)
        )
        right_box.add(time_label)
        
        if chat['unread'] > 0:
            unread = toga.Box(style=MobileStyles.badge())
            unread.add(
                toga.Label(
                    str(chat['unread']),
                    style=Pack(color='white', font_size=11, font_weight='bold')
                )
            )
            right_box.add(unread)
        
        chat_box.add(right_box)
        
        # Добавляем обработчик нажатия
        chat_box.on_press = lambda w, c=chat: self.open_chat(c)
        
        return chat_box
    
    def load_chats(self):
        role = getattr(self.app.current_user, 'role', 'pupil')
        
        base_chats = [
            {'name': 'Расписание Юг', 'unread': 3, 'icon': '📅', 'last_message': 'Завтра уроки в 9:00', 'time': '10:30'},
            {'name': 'Расписание Север', 'unread': 1, 'icon': '📅', 'last_message': 'Изменения в расписании', 'time': '09:15'}
        ]
        
        self.chats = base_chats.copy()
        
        if role == 'pupil':
            self.chats.extend([
                {'name': '7А класс', 'unread': 12, 'icon': '👥', 'last_message': 'Классный час в пятницу', 'time': 'Вчера'},
                {'name': 'Математика', 'unread': 0, 'icon': '📐', 'last_message': 'ДЗ на завтра', 'time': '11:45'},
                {'name': 'Физика', 'unread': 2, 'icon': '⚛️', 'last_message': 'Лабораторная работа', 'time': '13:20'}
            ])
    
    def new_chat(self, widget):
        self.app.main_window.info_dialog('Новый чат', 'Создание нового чата')
    
    def open_chat(self, chat):
        self.app.show_chat('chat_id_123', chat['name'])