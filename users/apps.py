import importlib
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    importlib.import_module("user.signals")
