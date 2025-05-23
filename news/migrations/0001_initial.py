# Generated by Django 5.0.2 on 2025-05-22 13:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='news_images/')),
                ('access_type', models.CharField(choices=[('PUBLIC', 'Público'), ('PRO', 'Conteúdo PRO')], default='PUBLIC', max_length=6)),
                ('status', models.CharField(choices=[('DRAFT', 'Rascunho'), ('SCHEDULED', 'Agendado'), ('PUBLISHED', 'Publicado')], default='DRAFT', max_length=10)),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL)),
                ('vertical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='users.vertical')),
            ],
            options={
                'verbose_name': 'Notícia',
                'verbose_name_plural': 'Notícias',
                'ordering': ['-publish_date', '-created_at'],
            },
        ),
    ]
