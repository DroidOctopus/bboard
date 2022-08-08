from django.apps import AppConfig
from django.dispatch import Signal
from django.utils.translation import gettext_lazy as _

from .utilities import send_activation_notification


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = _('Дошка оголошень')


user_registered = Signal('instance')


def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registered.connect(user_registered_dispatcher)
