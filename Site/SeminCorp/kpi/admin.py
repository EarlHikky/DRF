from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Staff, Sales

class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo')
    list_display_links = ('id', 'name', 'get_html_photo')
    # list_display_links = ('id', 'name', 'photo')
    prepopulated_fields = {"slug": ("name",)}
    # fields = ('name', 'photo', 'slug')
    # fields = ('name', 'photo', 'time_create', 'time_update')
    # readonly_fields = ('time_create', 'time_update')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Фото"


class SalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'time_create')
    list_display_links = ('id', 'fio')
    search_fields = ('fio', 'content')
    list_filter = ('fio', 'time_create')
    # fields = ('fio', 'extradition', 'ti', 'time_create', 'time_update')
    # readonly_fields = ('time_create', 'time_update')

admin.site.register(Staff, StaffAdmin)
admin.site.register(Sales, SalesAdmin)

admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Админ-панель'




