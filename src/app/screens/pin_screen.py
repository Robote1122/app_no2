import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

class PinScreen:
    def __init__(self, app):
        self.app = app
        self.pin = ""
        self.max_length = 4
        
    def build(self):
        main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                align_items=CENTER,
                flex=1,
                margin=20
            )
        )
        
        # Заголовок
        title = toga.Label(
            'Введите пин-код',
            style=Pack(font_size=24, font_weight='bold', margin_bottom=30)
        )
        
        # Индикаторы ввода пин-кода
        self.pin_dots = toga.Box(style=Pack(direction=ROW, margin_bottom=30))
        self.update_pin_display()
        
        # Клавиатура
        keyboard = toga.Box(style=Pack(direction=COLUMN))
        
        # Строки кнопок
        rows = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['⌫', '0', '✓']
        ]
        
        for row in rows:
            row_box = toga.Box(style=Pack(direction=ROW))
            for key in row:
                button = toga.Button(
                    key,
                    on_press=self.key_press,
                    style=Pack(
                        width=70,
                        height=70,
                        margin=5,
                        font_size=20
                    )
                )
                row_box.add(button)
            keyboard.add(row_box)
            
        main_box.add(title)
        main_box.add(self.pin_dots)
        main_box.add(keyboard)
        
        return main_box
        
    def update_pin_display(self):
        """Обновление отображения точек пин-кода"""
        self.pin_dots.clear()
        
        for i in range(self.max_length):
            if i < len(self.pin):
                dot = toga.Label('●', style=Pack(font_size=30, margin=5))
            else:
                dot = toga.Label('○', style=Pack(font_size=30, margin=5))
            self.pin_dots.add(dot)
            
    def key_press(self, widget):
        """Обработка нажатия кнопок клавиатуры"""
        key = widget.text
        
        if key == '⌫':
            self.pin = self.pin[:-1]
        elif key == '✓':
            if len(self.pin) == self.max_length:
                self.verify_pin()
        else:
            if len(self.pin) < self.max_length:
                self.pin += key
                
        self.update_pin_display()
        
    def verify_pin(self):
        """Проверка пин-кода"""
        # Здесь должна быть проверка через API
        if self.pin == "1234":  # Заглушка
            self.app.show_main_screen()
        else:
            self.app.main_window.error_dialog(
                'Ошибка',
                'Неверный пин-код'
            )
            self.pin = ""
            self.update_pin_display()