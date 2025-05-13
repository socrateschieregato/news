from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import News, Category
from .serializers import NewsSerializer, CategorySerializer
from .permissions import IsEditorOrReadOnly, IsAuthorOrReadOnly

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated, IsEditorOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = News.objects.all()
        user = self.request.user
        if not user.is_staff:
            queryset = queryset.filter(status='published')
            # Usuários comuns só veem notícias públicas
            queryset = queryset.filter(is_pro=False)
        return queryset

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if obj.is_pro and not user.is_staff:
            raise PermissionDenied("Conteúdo restrito a usuários PRO.")
        return obj

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
