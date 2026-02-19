import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
import os

class LoadingScreen:
    def __init__(self, app):
        self.app = app
        
    def build(self):
        main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                alignment=CENTER,
                flex=1,
                background_color='#4A90E2'
            )
        )
        
        # Логотип или картинка загрузки
        try:
            image_path = os.path.join(self.app.paths.app, 'resources', 'logo.png')
            logo = toga.ImageView(
                toga.Image(image_path),
                style=Pack(width=200, height=200)
            )
        except:
            # Заглушка если нет изображения
            logo = toga.Label(
                '🎓',
                style=Pack(font_size=100, color='white')
            )
            
        # Текст загрузки
        loading_label = toga.Label(
            'Взмах',
            style=Pack(
                font_size=32,
                font_weight='bold',
                color='white',
                margin_top=20
            )
        )
        
        progress = toga.ProgressBar(
            style=Pack(width=200, margin_top=20)
        )
        progress.start()
        
        main_box.add(logo)
        main_box.add(loading_label)
        main_box.add(progress)
        
        return main_box