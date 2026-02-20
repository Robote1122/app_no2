import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from ..widgets.menu_widget import MenuWidget
from ..styles import MobileStyles
import os

class MainScreen:
    def __init__(self, app, is_registered=False):
        self.app = app
        self.is_registered = is_registered
        
    def build(self):
        # Основной контейнер
        main_container = toga.ScrollContainer(
            style=Pack(flex=1, background_color=MobileStyles.COLORS['background'])
        )
        
        # Внешний бокс для центрирования
        outer_box = toga.Box(style=Pack(direction=COLUMN, alignment='center'))
        
        # Внутренний бокс с ограниченной шириной
        main_box = toga.Box(style=Pack(
            direction=COLUMN,
            width=380,
            margin=(0, 'auto')
        ))
        
        # Шапка с градиентным фоном
        header_box = toga.Box(style=Pack(
            direction=COLUMN,
            background_color=MobileStyles.COLORS['primary'],
            padding=20,
            border_radius=(0, 0, 20, 20),
            margin_bottom=20
        ))
        
        # Логотип или заголовок
        try:
            image_path = os.path.join(self.app.paths.app, 'resources', 'brand.png')
            brand_image = toga.ImageView(
                toga.Image(image_path),
                style=Pack(height=80, width=240)
            )
            header_box.add(brand_image)
        except:
            header_box.add(
                toga.Label(
                    'ВЗМАХ',
                    style=Pack(
                        font_size=36,
                        font_weight='bold',
                        color='white',
                        text_align='center'
                    )
                )
            )
        
        # Приветствие
        welcome_text = "Добро пожаловать!" if not self.is_registered else f"Здравствуйте, {getattr(self.app.current_user, 'first_name', 'пользователь')}!"
        welcome_label = toga.Label(
            welcome_text,
            style=Pack(
                font_size=16,
                color='white',
                margin_top=10,
                text_align='center'
            )
        )
        header_box.add(welcome_label)
        main_box.add(header_box)
        
        if not self.is_registered:
            # Блок для незарегистрированных
            info_card = toga.Box(style=MobileStyles.card())
            info_card.add(
                toga.Label(
                    'Присоединяйтесь к сообществу школы "Взмах"!',
                    style=Pack(
                        font_size=16,
                        color=MobileStyles.COLORS['text'],
                        margin_bottom=15
                    )
                )
            )
            
            register_button = toga.Button(
                'Зарегистрироваться',
                on_press=self.go_to_registration,
                style=MobileStyles.button_primary()
            )
            info_card.add(register_button)
            main_box.add(info_card)
        
        # Дайджест соцсетей
        digest_card = toga.Box(style=MobileStyles.card())
        
        digest_header = toga.Box(style=Pack(direction=ROW, margin_bottom=15))
        digest_header.add(
            toga.Label('📰 Последние новости', style=Pack(
                font_size=18,
                font_weight='bold',
                color=MobileStyles.COLORS['text']
            ))
        )
        digest_card.add(digest_header)
        
        # Новости в виде красивых карточек
        news_items = [
            ("📢 1 сентября", "Начало учебного года", "2 часа назад"),
            ("🎉 День учителя", "Праздничный концерт в 15:00", "Вчера"),
            ("🏆 Олимпиады", "Результаты доступны", "2 дня назад"),
            ("📅 Собрание", "Родительское собрание 15 октября", "3 дня назад")
        ]
        
        for title, desc, time in news_items:
            news_item = toga.Box(style=Pack(
                direction=ROW,
                margin=5,
                padding=10,
                background_color='#F8F9FA',
                border_radius=8
            ))
            
            news_content = toga.Box(style=Pack(direction=COLUMN, flex=1))
            news_content.add(
                toga.Label(title, style=Pack(font_weight='bold', font_size=14))
            )
            news_content.add(
                toga.Label(desc, style=Pack(font_size=12, color='#666'))
            )
            
            time_label = toga.Label(
                time,
                style=Pack(font_size=10, color='#999', text_align='right')
            )
            
            news_item.add(news_content)
            news_item.add(time_label)
            digest_card.add(news_item)
        
        main_box.add(digest_card)
        
        if self.is_registered:
            # Рабочее меню для зарегистрированных
            menu_card = toga.Box(style=MobileStyles.card())
            
            menu_card.add(
                toga.Label(
                    '⚡ Быстрые действия',
                    style=Pack(
                        font_size=18,
                        font_weight='bold',
                        color=MobileStyles.COLORS['text'],
                        margin_bottom=15
                    )
                )
            )
            
            # Сетка кнопок 2x2
            grid = toga.Box(style=Pack(direction=COLUMN))
            
            # Первая строка
            row1 = toga.Box(style=Pack(direction=ROW))
            
            exchange_btn = toga.Button(
                '📊 Биржа "АйТигры',
                on_press=self.open_exchange,
                style=Pack(
                    flex=1,
                    margin=5,
                    padding=12,
                    background_color='#E3F2FD',
                    color='#1976D2',
                    border_radius=10,
                    font_size=14
                )
            )
            
            social_btn = toga.Button(
                '👥 Соцсеть школы',
                on_press=self.open_social,
                style=Pack(
                    flex=1,
                    margin=5,
                    padding=12,
                    background_color='#F3E5F5',
                    color='#7B1FA2',
                    border_radius=10,
                    font_size=14
                )
            )
            
            row1.add(exchange_btn)
            row1.add(social_btn)
            grid.add(row1)
            
            # Вторая строка
            row2 = toga.Box(style=Pack(direction=ROW))
            
            market_btn = toga.Button(
                '🛒 Взмах-Маркет',
                on_press=self.open_market,
                style=Pack(
                    flex=1,
                    margin=5,
                    padding=12,
                    background_color='#E8F5E8',
                    color='#2E7D32',
                    border_radius=10,
                    font_size=14
                )
            )
            
            corps_btn = toga.Button(
                '📋 Корпорации',
                on_press=self.open_corporations,
                style=Pack(
                    flex=1,
                    margin=5,
                    padding=12,
                    background_color='#FFF3E0',
                    color='#E65100',
                    border_radius=10,
                    font_size=14
                )
            )
            
            row2.add(market_btn)
            row2.add(corps_btn)
            grid.add(row2)
            
            menu_card.add(grid)
            main_box.add(menu_card)
        
        # Добавляем меню
        outer_box.add(main_box)
        outer_box.add(MenuWidget(self.app).build())
        main_container.content = outer_box
        
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
        
    # def scroll_to_top(self, widget):
    #     # В Toga нет прямого метода прокрутки, но можно обновить контент
    #     self.app.show_main_screen()