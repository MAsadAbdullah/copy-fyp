from django.contrib import admin

# Register your models here.
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name',)
    search_fields = ('email', 'name')

admin.site.register(CustomUser, CustomUserAdmin)