import toga
from toga.style import Pack
from toga.style.pack import ROW, CENTER

class MenuWidget:
    def __init__(self, app):
        self.app = app
        
    def build(self):
        menu_box = toga.Box(
            style=Pack(
                direction=ROW,
                background_color='#f0f0f0',
                margin=10,
                align_items=CENTER
            )
        )
        
        # Кнопки меню
        menu_items = [
            ('💬', self.show_chats, 'Чаты'),
            ('📊', self.show_exchange, 'Биржа'),
            ('👥', self.show_social, 'Соцсеть'),
            ('🛒', self.show_market, 'Маркет'),
            ('📋', self.show_more, 'Еще')
        ]
        
        for icon, handler, tooltip in menu_items:
            button = toga.Button(
                icon,
                on_press=handler,
                style=Pack(
                    width=40,
                    height=40,
                    margin=(0, 5),
                    background_color='#f0f0f0'
                )
            )
            button.tooltip = tooltip
            menu_box.add(button)
            
        return menu_box
        
    def show_chats(self, widget):
        self.app.show_chat_list()
        
    def show_exchange(self, widget):
        self.app.main_window.info_dialog('Биржа', 'Раздел в разработке')
        
    def show_social(self, widget):
        self.app.main_window.info_dialog('Соцсеть', 'Раздел в разработке')
        
    def show_market(self, widget):
        self.app.main_window.info_dialog('Маркет', 'Раздел в разработке')
        
    def show_more(self, widget):
        self.app.main_window.info_dialog('Еще', 'Дополнительные функции')