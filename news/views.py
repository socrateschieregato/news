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
        
        # Usuário não autenticado só vê conteúdo público
        if not user.is_authenticated:
            return queryset.filter(access_type='PUBLIC')
            
        # Administradores veem tudo
        if user.is_staff and not user.is_editor():
            return queryset
            
        # Editores veem apenas suas próprias postagens
        if user.is_editor():
            return queryset.filter(author=user)
            
        # Leitores
        if user.is_reader():
            # Se tem plano PRO, pode ver conteúdo PRO
            if hasattr(user, 'plan') and user.plan and user.plan.plan_type == 'PRO':
                return queryset.filter(access_type__in=['PUBLIC', 'PRO'])
            # Se não tem plano PRO, só vê conteúdo público
            return queryset.filter(access_type='PUBLIC')
            
        return queryset.filter(access_type='PUBLIC')

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        
        # Verifica acesso para conteúdo PRO
        if obj.access_type == 'PRO' and not user.is_staff and not (hasattr(user, 'plan') and user.plan and user.plan.plan_type == 'PRO'):
            raise PermissionDenied("Conteúdo restrito a usuários PRO.")
        return obj

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
