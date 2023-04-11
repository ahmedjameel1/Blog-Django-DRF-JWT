from django.contrib import admin
from .models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['subject', 'author', 'slug', 'created_at', 'status']
    list_filter = ['status', 'created_at', 'author']
    search_fields = ['subject', 'body']
    prepopulated_fields = {'slug': ('subject',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    ordering = ['status', 'created_at']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'article', 'created_at']
    search_fields = ['author', 'body']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Vote)
# admin.site.register(Tag)
