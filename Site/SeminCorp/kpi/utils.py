from django.urls import path, re_path
from .models import *
from django.core.cache import cache

menu = [{'title': "Добавить сотрудника", 'url_name': 'add_staff'},
        {'title': "Добавить продажу", 'url_name': 'add_sale'},
]
class DataMixin:
    paginate_by = 10
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu
        if not self.request.user.is_authenticated:
            user_menu = []
        context['menu'] = user_menu
        return context
