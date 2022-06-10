from django.apps import AppConfig
import sys, os
sys.path.append(os.path.abspath('.'))

class PostAddConfig(AppConfig):
    name = 'simpleapp'

    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import signals


class SimpleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleapp'


