import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from ..styles import MobileStyles

class RegistrationScreen:
    def __init__(self, app):
        self.app = app
        self.role = "pupil"  # По умолчанию
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
        
        # Заголовок с иконкой
        header_box = toga.Box(style=Pack(
            direction=ROW,
            alignment='center',
            margin_bottom=25
        ))
        header_box.add(
            toga.Label(
                '📝',
                style=Pack(font_size=40, margin_right=10)
            )
        )
        header_box.add(
            toga.Label(
                'Регистрация',
                style=Pack(
                    font_size=28,
                    font_weight='bold',
                    color=MobileStyles.COLORS['text']
                )
            )
        )
        main_box.add(header_box)
        
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
        
        # Выбор роли
        role_container = toga.Box(style=Pack(direction=COLUMN, margin=5))
        role_container.add(
            toga.Label(
                '👥 Кто вы:',
                style=MobileStyles.label()
            )
        )
        
        role_box = toga.Box(style=Pack(
            direction=ROW,
            flex_wrap='wrap',
            margin_top=5
        ))
        
        roles = [
            ('👨‍🎓 Ученик', 'pupil', '#E3F2FD', '#1976D2'),
            ('👨‍🏫 Сотрудник', 'employee', '#F3E5F5', '#7B1FA2'),
            ('👪 Родственник', 'relative', '#E8F5E8', '#2E7D32'),
            ('🎓 Выпускник', 'graduate', '#FFF3E0', '#E65100')
        ]
        
        self.role_buttons = {}
        for text, value, bg_color, color in roles:
            button = toga.Button(
                text,
                on_press=self.select_role,
                style=Pack(
                    margin=3,
                    padding=8,
                    background_color=bg_color,
                    color=color,
                    border_radius=20,
                    font_size=12,
                    width=165
                )
            )
            button._value = value
            role_box.add(button)
            self.role_buttons[value] = button
        
        role_container.add(role_box)
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
        
        outer_box.add(main_box)
        main_container.content = outer_box
        return main_container
    
    # Остальные методы остаются без изменений
    def select_role(self, widget):
        self.role = widget._value
        self.update_class_selection()
        
        for value, button in self.role_buttons.items():
            if value == self.role:
                button.style.background_color = MobileStyles.COLORS['primary']
                button.style.color = 'white'
            else:
                button.style.background_color = '#f0f0f0'
                button.style.color = MobileStyles.COLORS['text']
    
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
            for grade in ['1А', '1Б', '2А', '2Б', '3А']:
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
        
        # Здесь ваша логика регистрации
        response = self.app.api_client.check_registration(registration_data)
        
        if response.get('found'):
            self.app.handle_registration_complete({
                'id': 'new_user_id',
                **registration_data
            })
        else:
            self.app.show_completion_screen(registration_data, found_in_list=False)