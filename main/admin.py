from django.contrib import admin

from .models import Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = [
        'word',
        'frequency',
    ]
    search_fields = ['word']

