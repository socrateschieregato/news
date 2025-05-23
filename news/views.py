from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.utils import timezone
from .models import News
from .serializers import NewsSerializer
from .permissions import IsEditorOrReadOnly, IsAuthorOrReadOnly
from .tasks import schedule_news_publication


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsEditorOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return News.objects.none()
            
        queryset = News.objects.all()
        user = self.request.user
        
        # Usuário não autenticado só vê conteúdo público e publicado
        if not user.is_authenticated:
            return queryset.filter(access_type='PUBLIC', status='PUBLISHED')
            
        # Administradores veem tudo
        if user.is_staff and not user.is_editor():
            return queryset
            
        # Editores veem apenas suas próprias postagens
        if user.is_editor():
            return queryset.filter(author=user)
            
        # Leitores
        if user.is_reader():
            # Se tem plano PRO, pode ver conteúdo PRO publicado
            if hasattr(user, 'plan') and user.plan and user.plan.plan_type == 'PRO':
                return queryset.filter(
                    status='PUBLISHED',
                    access_type__in=['PUBLIC', 'PRO']
                )
            # Se não tem plano PRO, só vê conteúdo público publicado
            return queryset.filter(access_type='PUBLIC', status='PUBLISHED')
            
        return queryset.filter(access_type='PUBLIC', status='PUBLISHED')

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        
        # Verifica acesso para conteúdo PRO
        if obj.access_type == 'PRO' and not user.is_staff and not (hasattr(user, 'plan') and user.plan and user.plan.plan_type == 'PRO'):
            raise PermissionDenied("Conteúdo restrito a usuários PRO.")
        return obj

    def perform_create(self, serializer):
        # Verifica se o usuário tem acesso à vertical
        vertical = serializer.validated_data.get('vertical')
        user = self.request.user
        
        # Se o usuário não tem plano ou o plano não tem acesso à vertical
        if not user.plan or not user.can_access_vertical(vertical):
            raise PermissionDenied("Seu plano não tem acesso a esta vertical.")
            
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        news = self.get_object()
        if news.author != request.user and not request.user.is_staff:
            raise PermissionDenied("Apenas o autor ou administradores podem publicar esta notícia.")
        
        news.publish()
        return Response({'status': 'notícia publicada'})

    @action(detail=True, methods=['post'])
    def schedule(self, request, pk=None):
        news = self.get_object()
        if news.author != request.user and not request.user.is_staff:
            raise PermissionDenied("Apenas o autor ou administradores podem agendar esta notícia.")
        
        publish_date = request.data.get('publish_date')
        if not publish_date:
            return Response(
                {'error': 'Data de publicação é obrigatória'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            publish_date = timezone.datetime.fromisoformat(publish_date)
            if publish_date <= timezone.now():
                return Response(
                    {'error': 'Data de publicação deve ser futura'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Formato de data inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Agenda a publicação usando Celery
        schedule_news_publication.delay(news.id, publish_date.isoformat())
        
        return Response({
            'status': 'notícia agendada para publicação',
            'publish_date': publish_date
        })
