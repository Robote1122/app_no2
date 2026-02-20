from toga.style.pack import Pack, COLUMN, ROW, CENTER

class MobileStyles:
    @staticmethod
    def container():
        return Pack(
            direction=COLUMN,
            flex=1,
            background_color='#f5f5f5'
        )
    
    @staticmethod
    def card():
        return Pack(
            background_color='white',
            margin=(5, 10),
            padding=10,
            border_width=1,
            border_color='#e0e0e0',
            border_radius=8  # Скругленные углы
        )
    
    @staticmethod
    def header():
        return Pack(
            direction=ROW,
            padding=(15, 10),
            background_color='white',
            border_width=1,
            border_color='#e0e0e0'
        )
    
    @staticmethod
    def title():
        return Pack(
            font_size=20,
            font_weight='bold',
            color='#333333',
            padding=(0, 10)
        )
    
    @staticmethod
    def button_primary():
        return Pack(
            background_color='#4A90E2',
            color='white',
            padding=12,
            font_size=16,
            border_radius=25,  # Закругленная кнопка
            width=250,
            margin=5
        )
    
    @staticmethod
    def message_bubble_own():
        return Pack(
            background_color='#4A90E2',
            color='white',
            padding=10,
            border_radius=18,
            margin=(2, 10, 2, 50)  # Справа
        )
    
    @staticmethod
    def message_bubble_other():
        return Pack(
            background_color='white',
            color='black',
            padding=10,
            border_radius=18,
            margin=(2, 50, 2, 10),  # Слева
            border_width=1,
            border_color='#e0e0e0'
        )