class Navigation:
    def __init__(self, app):
        self.app = app
        self.history = []
        
    def push(self, screen_name, *args, **kwargs):
        """Переход на новый экран"""
        self.history.append((screen_name, args, kwargs))
        self._show_screen(screen_name, *args, **kwargs)
        
    def pop(self):
        """Возврат на предыдущий экран"""
        if len(self.history) > 1:
            self.history.pop()
            screen_name, args, kwargs = self.history[-1]
            self._show_screen(screen_name, *args, **kwargs)
        elif len(self.history) == 1:
            # Возврат на главный экран
            self.history = []
            self.app.show_main_screen()
            
    def _show_screen(self, screen_name, *args, **kwargs):
        """Показать экран по имени"""
        screen_methods = {
            'main': self.app.show_main_screen,
            'chats': self.app.show_chat_list,
            'chat': lambda: self.app.show_chat(*args, **kwargs),
            'registration': self.app.show_registration_screen,
            'pin': self.app.show_pin_screen,
        }
        
        if screen_name in screen_methods:
            screen_methods[screen_name]()