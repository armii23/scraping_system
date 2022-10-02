from django.contrib import admin
from .models import *


class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'category')


admin.site.register(Category)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Internship, InternshipAdmin)
