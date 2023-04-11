from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('routes/', views.GetRoutes.as_view(), name='routes'),
    path('articles/', views.ArticleList.as_view(), name='api-articles'),
    path('article/<str:pk>/', views.ArticleDetails.as_view(), name='api-article'),
    path('reply/<str:pk>/', views.ReplyDetails.as_view(), name='api-reply'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
