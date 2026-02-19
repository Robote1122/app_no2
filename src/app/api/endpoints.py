# Эндпоинты API (все начинаются с https://vzmakh.su/api/)

API_ENDPOINTS = {
    # Регистрация и аутентификация
    'register': '/auth/register',
    'verify_pin': '/auth/verify-pin',
    'login': '/auth/login',
    
    # Пользователи
    'get_user': '/users/{user_id}',
    'update_user': '/users/{user_id}',
    'get_user_by_key': '/users/key/{key_id}',
    
    # Ключи шифрования
    'register_public_key': '/keys/register',
    'get_public_key': '/keys/{user_id}',
    
    # Чаты
    'get_chats': '/chats',
    'get_chat': '/chats/{chat_id}',
    'create_chat': '/chats/create',
    'get_chat_messages': '/chats/{chat_id}/messages',
    
    # Сообщения
    'send_message': '/messages/send',
    'get_message': '/messages/{message_id}',
    'delete_message': '/messages/{message_id}',
    
    # Подписки на чаты
    'subscribe_to_chat': '/chats/{chat_id}/subscribe',
    'unsubscribe_from_chat': '/chats/{chat_id}/unsubscribe',
    'get_subscribers': '/chats/{chat_id}/subscribers',
    
    # Администрирование чатов
    'add_admin': '/chats/{chat_id}/admins',
    'remove_admin': '/chats/{chat_id}/admins/{user_id}',
    'pin_message': '/chats/{chat_id}/pin/{message_id}',
    'restrict_user': '/chats/{chat_id}/restrict/{user_id}',
    
    # Дайджест соцсетей
    'get_digest': '/digest/latest',
    
    # Регистрация пользователей (проверка по спискам)
    'check_registration': '/registration/check',
    'manual_registration_request': '/registration/manual-request',
    
    # Филиалы и классы
    'get_branches': '/branches',
    'get_classes': '/branches/{branch_id}/classes',
    
    # Меню и дополнительные функции
    'get_menu_items': '/menu/items',
    'get_exchange_data': '/exchange/data',
    'get_market_items': '/market/items'
}

# Описания API запросов
API_REQUESTS = {
    'register': {
        'method': 'POST',
        'body': {
            'first_name': 'string',
            'last_name': 'string',
            'role': 'string',  # pupil/employee/relative/graduate
            'branch': 'string',
            'classes': 'array',  # для родителей может быть несколько
            'pin_code': 'string',
            'public_key': 'string',  # PEM формат
            'key_id': 'string'
        },
        'response': {
            'user_id': 'string',
            'status': 'string',
            'message': 'string'
        }
    },
    
    'check_registration': {
        'method': 'POST',
        'body': {
            'first_name': 'string',
            'last_name': 'string',
            'role': 'string',
            'branch': 'string',
            'class': 'string/array'
        },
        'response': {
            'found': 'boolean',
            'matches': 'array',  # список найденных совпадений
            'suggestions': 'array'  # предложения при частичном совпадении
        }
    },
    
    'register_public_key': {
        'method': 'POST',
        'body': {
            'user_id': 'string',
            'public_key': 'string',  # PEM формат
            'key_id': 'string',
            'signature': 'string'  # подпись для верификации
        },
        'response': {
            'status': 'string',
            'message': 'string'
        }
    },
    
    'send_message': {
        'method': 'POST',
        'body': {
            'chat_id': 'string',
            'sender_id': 'string',
            'encrypted_key': 'string',  # зашифрованный симметричный ключ
            'iv': 'string',  # вектор инициализации
            'encrypted_message': 'string',  # зашифрованное сообщение
            'recipient_key_ids': 'array',  # ID ключей получателей
            'timestamp': 'integer',
            'reply_to': 'string/optional'  # ID сообщения, на которое отвечаем
        },
        'response': {
            'message_id': 'string',
            'status': 'string',
            'timestamp': 'integer'
        }
    },
    
    'get_chat_messages': {
        'method': 'GET',
        'params': {
            'chat_id': 'string',
            'limit': 'integer',
            'offset': 'integer',
            'after_timestamp': 'integer'
        },
        'response': {
            'messages': 'array',  # массив зашифрованных сообщений
            'total_count': 'integer',
            'has_more': 'boolean'
        }
    }
}