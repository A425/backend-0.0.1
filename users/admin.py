from django.contrib import admin
from users.models import Token

# Register your models here.
class TokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'token')

admin.site.register(Token, TokenAdmin)
