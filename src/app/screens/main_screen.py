import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, CENTER
from ..widgets.menu_widget import MenuWidget
import os

class MainScreen:
    def __init__(self, app, is_registered=False):
        self.app = app
        self.is_registered = is_registered
        
    def build(self):
        main_container = toga.ScrollContainer(style=Pack(flex=1))
        main_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        
        # Брендирование (картинка)
        try:
            image_path = os.path.join(self.app.paths.app, 'resources', 'brand.png')
            brand_image = toga.ImageView(
                toga.Image(image_path),
                style=Pack(height=150, width=300)
            )
        except:
            brand_image = toga.Box(
                style=Pack(
                    height=150,
                    background_color='#4A90E2',
                    alignment=CENTER
                )
            )
            brand_image.add(
                toga.Label(
                    'ВЗМАХ',
                    style=Pack(font_size=32, color='white', font_weight='bold')
                )
            )
            
        main_box.add(brand_image)
        
        # Дайджест соцсетей
        digest_label = toga.Label(
            'Последние новости',
            style=Pack(font_size=18, font_weight='bold', margin=(20, 0, 10, 0))
        )
        main_box.add(digest_label)
        
        # Контейнер для новостей
        news_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                margin=10,
                background_color='#f5f5f5'
            )
        )
        
        # Заглушка новостей
        news_items = [
            "📢 1 сентября - начало учебного года",
            "🎉 День учителя 5 октября",
            "🏆 Результаты олимпиад",
            "📅 Родительское собрание 15 октября"
        ]
        
        for news in news_items:
            news_item = toga.Box(
                style=Pack(
                    direction=ROW,
                    margin=5,
                    background_color='white',
                    width=300
                )
            )
            news_item.add(toga.Label(news, style=Pack(margin=5)))
            news_box.add(news_item)
            
        main_box.add(news_box)
        
        if not self.is_registered:
            # Кнопка регистрации для незарегистрированных
            register_button = toga.Button(
                'Зарегистрироваться',
                on_press=self.go_to_registration,
                style=Pack(
                    margin=20,
                    background_color='#4A90E2',
                    color='white',
                    font_size=16
                )
            )
            main_box.add(register_button)
        else:
            # Рабочее меню для зарегистрированных
            menu_label = toga.Label(
                'Рабочее меню',
                style=Pack(font_size=18, font_weight='bold', margin=(20, 0, 10, 0))
            )
            main_box.add(menu_label)
            
            # Кнопки рабочего меню
            menu_items = [
                ('📊 Биржа "АйТигры"', self.open_exchange),
                ('👥 Соцсеть школы', self.open_social),
                ('🛒 Взмах-Маркет', self.open_market),
                ('📋 Корпорации', self.open_corporations),
                ('📁 Загрузка отчетов', self.open_reports)
            ]
            
            for text, handler in menu_items:
                button = toga.Button(
                    text,
                    on_press=handler,
                    style=Pack(
                        margin=5,
                        background_color='#e0e0e0',
                        width=250
                    )
                )
                main_box.add(button)
                
            # Кнопка прокрутки вверх
            scroll_top = toga.Button(
                '↑ Наверх',
                on_press=self.scroll_to_top,
                style=Pack(margin=20, background_color='#f0f0f0')
            )
            main_box.add(scroll_top)
            
        # Добавляем меню (доступно всегда)
        menu = MenuWidget(self.app)
        main_box.add(menu.build())
        
        main_container.content = main_box
        return main_container
        
    def go_to_registration(self, widget):
        self.app.show_registration_screen()
        
    def open_exchange(self, widget):
        self.app.main_window.info_dialog('Биржа', 'Раздел в разработке')
        
    def open_social(self, widget):
        self.app.main_window.info_dialog('Соцсеть', 'Раздел в разработке')
        
    def open_market(self, widget):
        self.app.main_window.info_dialog('Маркет', 'Раздел в разработке')
        
    def open_corporations(self, widget):
        self.app.main_window.info_dialog('Корпорации', 'Раздел в разработке')
        
    def open_reports(self, widget):
        self.app.main_window.info_dialog('Отчеты', 'Раздел в разработке')
        
    def scroll_to_top(self, widget):
        # В Toga нет прямого метода прокрутки, но можно обновить контент
        self.app.show_main_screen()