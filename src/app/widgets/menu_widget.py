import toga
from toga.style import Pack
from toga.style.pack import ROW, COLUMN
from ..styles import MobileStyles

class MenuWidget:
    def __init__(self, app):
        self.app = app
        
    def build(self):
        menu_box = toga.Box(style=MobileStyles.menu_bar())
        
        menu_items = [
            ('🏠', self.show_main, 'Главная', MobileStyles.COLORS['primary']),
            ('💬', self.show_chats, 'Чаты', '#50C878'),
            ('📊', self.show_exchange, 'Биржа', '#FF9800'),
            ('🛒', self.show_market, 'Маркет'),
            ('👤', self.show_profile, 'Профиль', '#9C27B0'),
        ]
        
        for icon, handler, tooltip, color in menu_items:
            button_container = toga.Box(style=Pack(
                direction=COLUMN,
                alignment='center',
                flex=1
            ))
            
            button = toga.Button(
                icon,
                on_press=handler,
                style=Pack(
                    width=44,
                    height=44,
                    background_color='transparent',
                    font_size=24,
                    border_radius=22
                )
            )
            button.tooltip = tooltip
            
            # Подпись под иконкой
            label = toga.Label(
                tooltip[:2] if len(tooltip) > 2 else tooltip,
                style=Pack(
                    font_size=10,
                    color='#666',
                    text_align='center'
                )
            )
            
            button_container.add(button)
            button_container.add(label)
            menu_box.add(button_container)
        
        # Индикатор активного пункта (можно добавить логику подсветки)
        return menu_box
    
    def show_main(self, widget):
        self.app.show_main_screen()
    
    def show_chats(self, widget):
        self.app.show_chat_list()
        
    def show_market(self, widget):
        self.app.main_window.info_dialog('Маркет', 'Раздел в разработке')
    
    def show_exchange(self, widget):
        self.app.main_window.info_dialog('Биржа', 'Раздел в разработке')
    
    def show_profile(self, widget):
        self.app.main_window.info_dialog('Профиль', 'Информация о пользователе')