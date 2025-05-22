from django.db import models
from django.contrib.auth import get_user_model
from users.models import Vertical
from django.utils import timezone

User = get_user_model()

class News(models.Model):
    ACCESS_TYPES = [
        ('PUBLIC', 'Público'),
        ('PRO', 'Conteúdo PRO'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Rascunho'),
        ('SCHEDULED', 'Agendado'),
        ('PUBLISHED', 'Publicado'),
    ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    vertical = models.ForeignKey(Vertical, on_delete=models.CASCADE, related_name='news')
    access_type = models.CharField(max_length=6, choices=ACCESS_TYPES, default='PUBLIC')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def publish(self):
        self.status = 'PUBLISHED'
        self.publish_date = timezone.now()
        self.save()

    def schedule_publish(self, publish_date):
        self.status = 'SCHEDULED'
        self.publish_date = publish_date
        self.save()

    def unpublish(self):
        self.status = 'DRAFT'
        self.publish_date = None
        self.save()

    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'
        ordering = ['-publish_date', '-created_at']
