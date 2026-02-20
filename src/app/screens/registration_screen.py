import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from ..styles import MobileStyles

class RegistrationScreen:
    def __init__(self, app):
        self.app = app
        self.role = "pupil"
        self.selected_classes = []
        
    def build(self):
        main_container = toga.ScrollContainer(
            style=Pack(flex=1, background_color=MobileStyles.COLORS['background'])
        )
        
        outer_box = toga.Box(style=Pack(direction=COLUMN, alignment='center'))
        main_box = toga.Box(style=Pack(
            direction=COLUMN,
            width=380,
            margin=(0, 'auto'),
            padding=15
        ))
        
        # Шапка с кнопкой назад
        header = toga.Box(style=Pack(
            direction=ROW,
            margin_bottom=20,
            alignment='center'
        ))
        
        # Кнопка "Назад" слева
        back_button = toga.Button(
            '←',
            on_press=self.go_back,
            style=Pack(
                width=44,
                height=44,
                background_color='transparent',
                font_size=24,
                border_radius=22,
                color=MobileStyles.COLORS['primary']
            )
        )
        header.add(back_button)
        
        # Заголовок по центру
        header.add(
            toga.Label(
                'Регистрация',
                style=Pack(
                    font_size=24,
                    font_weight='bold',
                    color=MobileStyles.COLORS['text'],
                    flex=1,
                    text_align='center'
                )
            )
        )
        
        # Пустой элемент для баланса
        spacer = toga.Box(style=Pack(width=44))
        header.add(spacer)
        
        main_box.add(header)
        
        # Карточка с формой
        form_card = toga.Box(style=MobileStyles.card())
        
        # Поля ввода с иконками
        fields = [
            ('👤', 'Имя', 'first_name', 'Введите имя'),
            ('📋', 'Фамилия', 'last_name', 'Введите фамилию'),
            ('🔐', 'Пин-код', 'pin_code', '****')
        ]
        
        for icon, label_text, attr_name, placeholder in fields:
            field_container = toga.Box(style=Pack(direction=COLUMN, margin=5))
            
            label_box = toga.Box(style=Pack(direction=ROW, margin_bottom=2))
            label_box.add(
                toga.Label(
                    f"{icon} {label_text}",
                    style=MobileStyles.label()
                )
            )
            
            if attr_name == 'pin_code':
                input_field = toga.PasswordInput(
                    placeholder=placeholder,
                    style=MobileStyles.input_field()
                )
                setattr(self, attr_name, input_field)
            else:
                input_field = toga.TextInput(
                    placeholder=placeholder,
                    style=MobileStyles.input_field()
                )
                setattr(self, attr_name, input_field)
            
            field_container.add(label_box)
            field_container.add(input_field)
            form_card.add(field_container)
        
        # Выбор роли - разделен на две строки
        role_container = toga.Box(style=Pack(direction=COLUMN, margin=5))
        role_container.add(
            toga.Label(
                '👥 Кто вы:',
                style=MobileStyles.label()
            )
        )
        
        # Первая строка ролей
        role_row1 = toga.Box(style=Pack(
            direction=ROW,
            margin_top=5,
            margin_bottom=3
        ))
        
        # Вторая строка ролей
        role_row2 = toga.Box(style=Pack(
            direction=ROW,
            margin_bottom=5
        ))
        
        roles_row1 = [
            ('👨‍🎓 Ученик', 'pupil', '#E3F2FD', '#1976D2'),
            ('👨‍🏫 Сотрудник', 'employee', '#F3E5F5', '#7B1FA2'),
        ]
        
        roles_row2 = [
            ('👪 Родственник', 'relative', '#E8F5E8', '#2E7D32'),
            ('🎓 Выпускник', 'graduate', '#FFF3E0', '#E65100'),
        ]
        
        self.role_buttons = {}
        
        # Добавляем первую строку
        for text, value, bg_color, color in roles_row1:
            button = toga.Button(
                text,
                on_press=self.select_role,
                style=Pack(
                    margin=3,
                    padding=10,
                    background_color=bg_color,
                    color=color,
                    border_radius=20,
                    font_size=13,
                    font_weight='bold',
                    flex=1
                )
            )
            button._value = value
            role_row1.add(button)
            self.role_buttons[value] = button
        
        # Добавляем вторую строку
        for text, value, bg_color, color in roles_row2:
            button = toga.Button(
                text,
                on_press=self.select_role,
                style=Pack(
                    margin=3,
                    padding=10,
                    background_color=bg_color,
                    color=color,
                    border_radius=20,
                    font_size=13,
                    font_weight='bold',
                    flex=1
                )
            )
            button._value = value
            role_row2.add(button)
            self.role_buttons[value] = button
        
        role_container.add(role_row1)
        role_container.add(role_row2)
        form_card.add(role_container)
        
        # Выбор филиала
        branch_container = toga.Box(style=Pack(direction=COLUMN, margin=5))
        branch_container.add(
            toga.Label(
                '🏫 Филиал:',
                style=MobileStyles.label()
            )
        )
        
        self.branch = toga.Selection(
            items=['Юг', 'Север', 'Центр'],
            style=Pack(
                width=340,
                padding=10,
                border_width=1,
                border_color=MobileStyles.COLORS['border'],
                border_radius=8,
                margin_top=5
            )
        )
        branch_container.add(self.branch)
        form_card.add(branch_container)
        
        # Выбор класса
        class_container = toga.Box(style=Pack(direction=COLUMN, margin=5))
        class_container.add(
            toga.Label(
                '📚 Класс:',
                style=MobileStyles.label()
            )
        )
        
        self.class_selection = toga.Box(style=Pack(direction=COLUMN))
        class_container.add(self.class_selection)
        form_card.add(class_container)
        
        self.update_class_selection()
        main_box.add(form_card)
        
        # Кнопка регистрации
        register_button = toga.Button(
            'Зарегистрироваться',
            on_press=self.register,
            style=MobileStyles.button_primary()
        )
        main_box.add(register_button)
        
        # Подсвечиваем выбранную роль по умолчанию
        self.role_buttons['pupil'].style.background_color = MobileStyles.COLORS['primary']
        self.role_buttons['pupil'].style.color = 'white'
        
        outer_box.add(main_box)
        main_container.content = outer_box
        return main_container
    
    def go_back(self, widget):
        """Возврат на главный экран"""
        self.app.show_main_screen()
    
    def select_role(self, widget):
        self.role = widget._value
        self.update_class_selection()
        
        for value, button in self.role_buttons.items():
            if value == self.role:
                button.style.background_color = MobileStyles.COLORS['primary']
                button.style.color = 'white'
            else:
                # Возвращаем исходные цвета для каждой роли
                if value == 'pupil':
                    button.style.background_color = '#E3F2FD'
                    button.style.color = '#1976D2'
                elif value == 'employee':
                    button.style.background_color = '#F3E5F5'
                    button.style.color = '#7B1FA2'
                elif value == 'relative':
                    button.style.background_color = '#E8F5E8'
                    button.style.color = '#2E7D32'
                elif value == 'graduate':
                    button.style.background_color = '#FFF3E0'
                    button.style.color = '#E65100'
    
    def update_class_selection(self):
        self.class_selection.clear()
        
        if self.role == 'pupil':
            classes = ['1', '2', '3', '4',
                       '5', '6', '7', '8',
                       '9', '10', '11']
            
            class_picker = toga.Selection(
                items=classes,
                style=Pack(
                    width=340,
                    padding=10,
                    border_width=1,
                    border_color=MobileStyles.COLORS['border'],
                    border_radius=8
                )
            )
            self.class_selection.add(class_picker)
            
        elif self.role == 'relative':
            label = toga.Label(
                'Выберите классы (можно несколько):',
                style=Pack(margin=(5, 0, 5, 0), font_size=12, color='#666')
            )
            self.class_selection.add(label)
            
            classes_box = toga.Box(style=Pack(
                direction=ROW,
                flex_wrap='wrap',
                margin_top=5
            ))
            # Показываем больше классов для родителей
            for grade in ['1А', '1Б', '2А', '2Б', '3А', '3Б', '4А', '4Б']:
                checkbox = toga.Switch(
                    grade,
                    style=Pack(margin=5, font_size=12)
                )
                classes_box.add(checkbox)
            self.class_selection.add(classes_box)
        else:
            self.class_selection.add(
                toga.Label(
                    'Не требуется',
                    style=Pack(
                        margin=5,
                        font_size=12,
                        color='#666',
                        font_style='italic'
                    )
                )
            )
    
    def select_photo(self, widget):
        self.app.main_window.info_dialog('Выбор фото', 'Выберите файл изображения')
        self.photo_path = 'path/to/photo.jpg'
    
    def register(self, widget):
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
            self.app.handle_registration_complete({
                'id': 'new_user_id',
                **registration_data
            })
        else:
            self.app.show_completion_screen(registration_data, found_in_list=False)