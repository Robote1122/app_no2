import toga
from toga.style import Pack
from toga.style.pack import COLUMN

class CompletionScreen:
    def __init__(self, app, registration_data, found_in_list=True):
        self.app = app
        self.registration_data = registration_data
        self.found_in_list = found_in_list
        
    def build(self):
        main_container = toga.ScrollContainer(style=Pack(flex=1))
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment='center'))
        
        if self.found_in_list:
            # Успешная регистрация
            icon = toga.Label('✅', style=Pack(font_size=64, padding=20))
            message = toga.Label(
                'Регистрация успешно завершена!',
                style=Pack(font_size=18, padding=10)
            )
            
            main_box.add(icon)
            main_box.add(message)
            
            # Кнопка перехода на главный экран
            continue_button = toga.Button(
                'Перейти на главный экран',
                on_press=self.go_to_main,
                style=Pack(
                    padding=20,
                    background_color='#4A90E2',
                    color='white',
                    width=250
                )
            )
            main_box.add(continue_button)
            
        else:
            # Не нашли в списках
            icon = toga.Label('❓', style=Pack(font_size=64, padding=20))
            message = toga.Label(
                'Мы не нашли вас в автоматизированных списках.',
                style=Pack(font_size=16, padding=5)
            )
            
            message2 = toga.Label(
                'Напишите подробней – кто вы – и мы зарегистрируем вас вручную.',
                style=Pack(font_size=14, padding=5, text_align='center')
            )
            
            main_box.add(icon)
            main_box.add(message)
            main_box.add(message2)
            
            # Поле для текстового сообщения
            main_box.add(toga.Label('Ваше сообщение:', style=Pack(margin_top=20)))
            self.message_input = toga.MultilineTextInput(
                placeholder='Опишите, кто вы...',
                style=Pack(width=300, height=100, padding=10)
            )
            main_box.add(self.message_input)
            
            # Кнопки
            button_box = toga.Box(style=Pack(direction='row', padding=20))
            
            send_button = toga.Button(
                'Отправить',
                on_press=self.send_request,
                style=Pack(padding=5, background_color='#4A90E2', color='white')
            )
            
            main_button = toga.Button(
                'Перейти на главный экран',
                on_press=self.go_to_main,
                style=Pack(padding=5)
            )
            
            button_box.add(send_button)
            button_box.add(main_button)
            main_box.add(button_box)
            
        main_container.content = main_box
        return main_container
        
    def send_request(self, widget):
        """Отправка запроса на ручную регистрацию"""
        if not self.message_input.value:
            self.app.main_window.error_dialog(
                'Ошибка',
                'Пожалуйста, напишите информацию о себе'
            )
            return
            
        # Отправка через API
        request_data = {
            **self.registration_data,
            'message': self.message_input.value
        }
        
        response = self.app.api_client.manual_registration_request(request_data)
        
        self.app.main_window.info_dialog(
            'Запрос отправлен',
            'Ваш запрос на регистрацию отправлен. Мы свяжемся с вами после проверки.'
        )
        
        self.go_to_main(None)
        
    def go_to_main(self, widget):
        """Переход на главный экран"""
        self.app.show_main_screen()