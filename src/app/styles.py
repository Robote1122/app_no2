from toga.style.pack import Pack, COLUMN, ROW, CENTER, LEFT

class MobileStyles:
    # Цветовая схема
    COLORS = {
        'primary': '#4A90E2',
        'primary_dark': '#3A70B2',
        'secondary': '#50C878',
        'background': '#F5F7FA',
        'surface': '#FFFFFF',
        'text': '#333333',
        'text_secondary': '#666666',
        'border': '#E0E4E8',
        'error': '#FF6B6B',
        'success': '#4CAF50'
    }
    
    @staticmethod
    def screen_container():
        """Основной контейнер экрана с отступами по бокам"""
        return Pack(
            direction=COLUMN,
            flex=1,
            background_color=MobileStyles.COLORS['background']
        )
    
    @staticmethod
    def content_container():
        """Контейнер для контента с ограничением ширины"""
        outer = Pack(direction=COLUMN, alignment=CENTER)
        inner = Pack(
            direction=COLUMN,
            width=380,
            margin=(0, 'auto')
        )
        return outer, inner
    
    @staticmethod
    def card():
        """Карточка для элементов списка"""
        return Pack(
            background_color=MobileStyles.COLORS['surface'],
            margin=(5, 10),
            padding=15,
            border_width=1,
            border_color=MobileStyles.COLORS['border'],
            border_radius=12,
            width=360
        )
    
    @staticmethod
    def header():
        """Заголовок экрана"""
        return Pack(
            direction=ROW,
            padding=(15, 15),
            background_color=MobileStyles.COLORS['surface'],
            border_width=1,
            border_color=MobileStyles.COLORS['border'],
            margin_bottom=10
        )
    
    @staticmethod
    def title():
        """Заголовок текста"""
        return Pack(
            font_size=24,
            font_weight='bold',
            color=MobileStyles.COLORS['text'],
            padding=(0, 15)
        )
    
    @staticmethod
    def subtitle():
        """Подзаголовок"""
        return Pack(
            font_size=18,
            font_weight='600',
            color=MobileStyles.COLORS['text'],
            margin=(15, 0, 10, 15)
        )
    
    @staticmethod
    def button_primary():
        """Основная кнопка"""
        return Pack(
            background_color=MobileStyles.COLORS['primary'],
            color=MobileStyles.COLORS['surface'],
            padding=14,
            font_size=16,
            font_weight='bold',
            border_radius=25,
            width=250,
            margin=8
        )
    
    @staticmethod
    def button_secondary():
        """Вторичная кнопка"""
        return Pack(
            background_color='transparent',
            color=MobileStyles.COLORS['primary'],
            padding=12,
            font_size=14,
            border_width=2,
            border_color=MobileStyles.COLORS['primary'],
            border_radius=25,
            width=200,
            margin=5
        )
    
    @staticmethod
    def input_field():
        """Поле ввода"""
        return Pack(
            width=340,
            padding=12,
            font_size=16,
            border_width=1,
            border_color=MobileStyles.COLORS['border'],
            border_radius=8,
            margin=5
        )
    
    @staticmethod
    def label():
        """Метка для поля ввода"""
        return Pack(
            font_size=14,
            color=MobileStyles.COLORS['text_secondary'],
            margin=(10, 5, 2, 10)
        )
    
    @staticmethod
    def message_bubble_own():
        """Свое сообщение"""
        return Pack(
            background_color=MobileStyles.COLORS['primary'],
            color=MobileStyles.COLORS['surface'],
            padding=12,
            border_radius=18,
            margin=(2, 10, 2, 50),
            max_width=300
        )
    
    @staticmethod
    def message_bubble_other():
        """Чужое сообщение"""
        return Pack(
            background_color=MobileStyles.COLORS['surface'],
            color=MobileStyles.COLORS['text'],
            padding=12,
            border_radius=18,
            margin=(2, 50, 2, 10),
            border_width=1,
            border_color=MobileStyles.COLORS['border'],
            max_width=300
        )
    
    @staticmethod
    def avatar(size=50):
        """Аватар пользователя"""
        return Pack(
            width=size,
            height=size,
            background_color=MobileStyles.COLORS['primary'],
            border_radius=size // 2,
            alignment=CENTER
        )
    
    @staticmethod
    def menu_bar():
        """Нижнее меню"""
        return Pack(
            direction=ROW,
            background_color=MobileStyles.COLORS['surface'],
            padding=8,
            alignment=CENTER,
            border_width=1,
            border_color=MobileStyles.COLORS['border'],
            margin_top=10
        )
    
    @staticmethod
    def menu_button():
        """Кнопка меню"""
        return Pack(
            width=50,
            height=50,
            margin=(0, 5),
            background_color='transparent',
            font_size=24,
            border_radius=25
        )
    
    @staticmethod
    def badge():
        """Бейдж с числом (непрочитанные)"""
        return Pack(
            background_color=MobileStyles.COLORS['primary'],
            min_width=22,
            height=22,
            border_radius=11,
            alignment=CENTER,
            padding=(4, 8)
        )