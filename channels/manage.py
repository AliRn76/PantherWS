from django.conf import settings
from django.core.management import execute_from_command_line

settings.configure(
    SECRET_KEY='SecretKey',
    DEBUG=False,
    ALLOWED_HOSTS=['*'],
    INSTALLED_APPS=['channels'],
    ASGI_APPLICATION='app.asgi.application',
)
execute_from_command_line((__name__, 'runserver'))
