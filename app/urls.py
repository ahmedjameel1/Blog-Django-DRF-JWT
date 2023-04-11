from django.urls import path
from . import views
from .feeds import LatestArticlesFeed

urlpatterns = [
    path('articles/', views.articles, name='articles'),
    path('tag/<slug:tag_slug>/',
         views.articles, name='article_by_tag'),

    path('article/<int:year>/<int:month>/<int:day>/<str:slug>/<int:id>/',
         views.article_detail, name='article_detail'),
    path('<int:article_id>/share/',
         views.article_share, name='article_share'),
    path('<int:article_id>/reply/',
         views.article_reply, name='article_reply'),
    path('feed/', LatestArticlesFeed(), name='article_feed'),
    path('search/', views.article_search, name='article_search'),
]
