from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'news', views.NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 