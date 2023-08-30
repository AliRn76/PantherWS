from django.conf import settings
from django.core.management import execute_from_command_line


settings.configure(
    SECRET_KEY='SecretKey',
    DEBUG=True,
    INSTALLED_APPS=['channels'],
    ASGI_APPLICATION='panther_ws.asgi.application',
)
execute_from_command_line((__name__, 'runserver'))
