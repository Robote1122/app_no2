import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class RegistrationScreen:
    def __init__(self, app):
        self.app = app
        self.role = "pupil"  # По умолчанию
        self.selected_classes = []
        
    def build(self):
        main_container = toga.ScrollContainer(style=Pack(flex=1))
        main_box = toga.Box(style=Pack(direction=COLUMN, margin=20))
        
        # Заголовок
        title = toga.Label(
            'Регистрация',
            style=Pack(font_size=24, font_weight='bold', margin_bottom=20)
        )
        main_box.add(title)
        
        # Поле Имя
        main_box.add(toga.Label('Имя:', style=Pack(margin_top=10)))
        self.first_name = toga.TextInput(
            placeholder='Введите имя (е вместо ё)',
            style=Pack(width=300, margin=5)
        )
        main_box.add(self.first_name)
        
        # Поле Фамилия
        main_box.add(toga.Label('Фамилия:', style=Pack(margin_top=10)))
        self.last_name = toga.TextInput(
            placeholder='Введите фамилию (е вместо ё)',
            style=Pack(width=300, margin=5)
        )
        main_box.add(self.last_name)
        
        # Выбор роли
        main_box.add(toga.Label('Кто вы:', style=Pack(margin_top=10)))
        
        role_box = toga.Box(style=Pack(direction=ROW))
        roles = [
            ('👨‍🎓 Ученик', 'pupil'),
            ('👨‍🏫 Сотрудник', 'employee'),
            ('👪 Родственник', 'relative'),
            ('🎓 Выпускник', 'graduate')
        ]
        
        self.role_buttons = {}
        for text, value in roles:
            button = toga.Button(
                text,
                on_press=self.select_role,
                style=Pack(margin=2, font_size=12)
            )
            button._value = value
            role_box.add(button)
            self.role_buttons[value] = button
            
        main_box.add(role_box)
        
        # Выбор филиала
        main_box.add(toga.Label('Филиал:', style=Pack(margin_top=10)))
        self.branch = toga.Selection(
            items=['Юг', 'Север', 'Центр'],
            style=Pack(width=300, margin=5)
        )
        main_box.add(self.branch)
        
        # Выбор класса (динамический, зависит от роли)
        main_box.add(toga.Label('Класс:', style=Pack(margin_top=10)))
        self.class_selection = toga.Box(style=Pack(direction=COLUMN))
        self.update_class_selection()
        main_box.add(self.class_selection)
        
        # Выбор фото
        main_box.add(toga.Label('Фото для иконки (не обязательно):', style=Pack(margin_top=10)))
        photo_button = toga.Button(
            'Выбрать фото',
            on_press=self.select_photo,
            style=Pack(margin=5)
        )
        main_box.add(photo_button)
        self.photo_path = None
        
        # Пин-код
        main_box.add(toga.Label('Пин-код (4 цифры):', style=Pack(margin_top=10)))
        self.pin_code = toga.PasswordInput(
            placeholder='****',
            style=Pack(width=100, margin=5)
        )
        main_box.add(self.pin_code)
        
        # Кнопка регистрации
        register_button = toga.Button(
            'Зарегистрироваться',
            on_press=self.register,
            style=Pack(
                margin=20,
                background_color='#4A90E2',
                color='white',
                font_size=16
            )
        )
        main_box.add(register_button)
        
        main_container.content = main_box
        return main_container
        
    def select_role(self, widget):
        """Выбор роли"""
        self.role = widget._value
        self.update_class_selection()
        
        # Визуальное выделение выбранной роли
        for value, button in self.role_buttons.items():
            if value == self.role:
                button.style.background_color = '#4A90E2'
                button.style.color = 'white'
            else:
                button.style.background_color = None
                button.style.color = 'black'
                
    def update_class_selection(self):
        """Обновление выбора класса в зависимости от роли"""
        self.class_selection.clear()
        
        if self.role == 'pupil':
            # Для учеников - один класс
            self.class_selection.add(
                toga.Selection(
                    items=['1А', '1Б', '2А', '2Б', '3А', '3Б', '4А', '4Б', 
                           '5А', '5Б', '6А', '6Б', '7А', '7Б', '8А', '8Б', 
                           '9А', '9Б', '10А', '10Б', '11А', '11Б'],
                    style=Pack(width=200)
                )
            )
        elif self.role == 'relative':
            # Для родителей - несколько классов
            label = toga.Label('Выберите классы (можно несколько):')
            self.class_selection.add(label)
            
            # Чекбоксы для классов
            classes_box = toga.Box(style=Pack(direction=COLUMN))
            for grade in ['1А', '1Б', '2А', '2Б', '3А']:
                checkbox = toga.Switch(grade, style=Pack(margin=2))
                classes_box.add(checkbox)
            self.class_selection.add(classes_box)
        else:
            # Для остальных - класс не нужен
            self.class_selection.add(
                toga.Label('Не требуется', style=Pack(margin=5))
            )
            
    def select_photo(self, widget):
        """Выбор фото"""
        # В реальном приложении здесь был бы диалог выбора файла
        self.app.main_window.info_dialog('Выбор фото', 'Выберите файл изображения')
        self.photo_path = 'path/to/photo.jpg'  # Заглушка
        
    def register(self, widget):
        """Регистрация пользователя"""
        # Проверка заполнения полей
        if not self.first_name.value or not self.last_name.value or not self.pin_code.value:
            self.app.main_window.error_dialog(
                'Ошибка',
                'Заполните все обязательные поля'
            )
            return
            
        if len(self.pin_code.value) != 4 or not self.pin_code.value.isdigit():
            self.app.main_window.error_dialog(
                'Ошибка',
                'Пин-код должен состоять из 4 цифр'
            )
            return
            
        # Замена ё на е
        first_name = self.first_name.value.replace('ё', 'е').replace('Ё', 'Е')
        last_name = self.last_name.value.replace('ё', 'е').replace('Ё', 'Е')
        
        # Собираем данные для регистрации
        registration_data = {
            'first_name': first_name,
            'last_name': last_name,
            'role': self.role,
            'branch': self.branch.value,
            'pin_code': self.pin_code.value
        }
        
        # Проверка по спискам через API
        response = self.app.api_client.check_registration(registration_data)
        
        if response.get('found'):
            # Нашли в списках - переходим на главный экран
            self.app.handle_registration_complete({
                'id': 'new_user_id',
                **registration_data
            })
        else:
            # Не нашли в списках - показываем экран с ручным вводом
            self.app.show_completion_screen(registration_data, found_in_list=False)