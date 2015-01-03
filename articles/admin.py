from django.contrib import admin
from articles.models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('intention', 'name', 'cellphone', 'title', 'timestamp')

admin.site.register(Article, ArticleAdmin)
