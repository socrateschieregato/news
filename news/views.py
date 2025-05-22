from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import News
from .serializers import NewsSerializer
from .permissions import IsEditorOrReadOnly, IsAuthorOrReadOnly

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsEditorOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return News.objects.none()
            
        queryset = News.objects.all()
        user = self.request.user
        
        if not user.is_authenticated:
            return queryset.filter(access_type='PUBLIC')
            
        if not user.is_staff:
            queryset = queryset.filter(access_type='PUBLIC')
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
