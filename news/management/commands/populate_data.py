from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Plan, Vertical
from news.models import News
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando dados de exemplo...')

        # Criar Verticais
        verticais = [
            {'name': 'Poder', 'description': 'Notícias sobre política e poder'},
            {'name': 'Tributos', 'description': 'Notícias sobre tributação e impostos'},
            {'name': 'Saúde', 'description': 'Notícias sobre saúde pública e privada'},
            {'name': 'Energia', 'description': 'Notícias sobre setor energético'},
            {'name': 'Trabalhista', 'description': 'Notícias sobre direito trabalhista'},
        ]

        for vertical_data in verticais:
            vertical, created = Vertical.objects.get_or_create(
                name=vertical_data['name'],
                defaults={'description': vertical_data['description']}
            )
            if created:
                self.stdout.write(f'Vertical criada: {vertical.name}')

        # Criar Planos
        planos = [
            {
                'name': 'Básico',
                'description': 'Acesso a conteúdo público',
                'price': 0.00,
                'plan_type': 'INFO'
            },
            {
                'name': 'Premium',
                'description': 'Acesso completo a todo conteúdo',
                'price': 29.90,
                'plan_type': 'PRO'
            },
            {
                'name': 'Personalizado',
                'description': 'Acesso a verticais específicas',
                'price': 19.90,
                'plan_type': 'PRO'
            }
        ]

        for plano_data in planos:
            plano, created = Plan.objects.get_or_create(
                name=plano_data['name'],
                defaults={
                    'description': plano_data['description'],
                    'price': plano_data['price'],
                    'plan_type': plano_data['plan_type']
                }
            )
            if created:
                self.stdout.write(f'Plano criado: {plano.name}')

        # Criar Usuários
        usuarios = [
            {
                'username': 'admin',
                'email': 'admin@jota.com',
                'password': 'admin123',
                'is_staff': True,
                'is_superuser': True,
                'user_type': 'ADMIN',
                'plan': Plan.objects.get(name='Premium')
            },
            {
                'username': 'editor',
                'email': 'editor@jota.com',
                'password': 'editor123',
                'is_staff': True,
                'user_type': 'EDITOR',
                'plan': Plan.objects.get(name='Premium')
            },
            {
                'username': 'usuario_basico',
                'email': 'basico@jota.com',
                'password': 'basico123',
                'user_type': 'READER',
                'plan': Plan.objects.get(name='Básico')
            },
            {
                'username': 'usuario_premium',
                'email': 'premium@jota.com',
                'password': 'premium123',
                'user_type': 'READER',
                'plan': Plan.objects.get(name='Premium')
            }
        ]

        for usuario_data in usuarios:
            user, created = User.objects.get_or_create(
                username=usuario_data['username'],
                defaults={
                    'email': usuario_data['email'],
                    'is_staff': usuario_data.get('is_staff', False),
                    'is_superuser': usuario_data.get('is_superuser', False),
                    'plan': usuario_data['plan'],
                    'user_type': usuario_data['user_type']
                }
            )
            if created:
                user.set_password(usuario_data['password'])
                user.save()
                self.stdout.write(f'Usuário criado: {user.username}')

        # Criar Notícias
        noticias = [
            {
                'title': 'Reforma Tributária é aprovada no Senado',
                'subtitle': 'Proposta simplifica sistema tributário brasileiro',
                'content': 'O Senado aprovou hoje a Reforma Tributária...',
                'vertical': Vertical.objects.get(name='Tributos'),
                'access_type': 'PUBLIC',
                'is_pro': False,
                'author': User.objects.get(username='editor')
            },
            {
                'title': 'Novo ministro da Saúde toma posse',
                'subtitle': 'Mudanças na gestão da saúde pública são esperadas',
                'content': 'O novo ministro da Saúde tomou posse hoje...',
                'vertical': Vertical.objects.get(name='Saúde'),
                'access_type': 'PRO',
                'is_pro': True,
                'author': User.objects.get(username='editor')
            },
            {
                'title': 'Preços da energia elétrica sobem em todo país',
                'subtitle': 'Aumento afeta consumidores residenciais e industriais',
                'content': 'Os preços da energia elétrica subiram em média...',
                'vertical': Vertical.objects.get(name='Energia'),
                'access_type': 'PUBLIC',
                'is_pro': False,
                'author': User.objects.get(username='editor')
            },
            {
                'title': 'STF decide sobre horas extras',
                'subtitle': 'Decisão impacta milhões de trabalhadores',
                'content': 'O Supremo Tribunal Federal decidiu hoje sobre...',
                'vertical': Vertical.objects.get(name='Trabalhista'),
                'access_type': 'PRO',
                'is_pro': True,
                'author': User.objects.get(username='editor')
            }
        ]

        for noticia_data in noticias:
            noticia, created = News.objects.get_or_create(
                title=noticia_data['title'],
                defaults={
                    'subtitle': noticia_data['subtitle'],
                    'content': noticia_data['content'],
                    'vertical': noticia_data['vertical'],
                    'access_type': noticia_data['access_type'],
                    'is_pro': noticia_data['is_pro'],
                    'author': noticia_data['author'],
                    'publish_date': timezone.now()
                }
            )
            if created:
                self.stdout.write(f'Notícia criada: {noticia.title}')

        self.stdout.write(self.style.SUCCESS('Dados de exemplo criados com sucesso!')) 