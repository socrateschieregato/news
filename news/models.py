from django.db import models
from django.contrib.auth import get_user_model
from users.models import Vertical

User = get_user_model()

class News(models.Model):
    ACCESS_TYPES = [
        ('PUBLIC', 'Público'),
        ('PRO', 'Conteúdo PRO'),
    ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    vertical = models.ForeignKey(Vertical, on_delete=models.CASCADE, related_name='news')
    access_type = models.CharField(max_length=6, choices=ACCESS_TYPES, default='PUBLIC')
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def publish(self):
        self.access_type = 'PUBLIC'
        self.save()

    def unpublish(self):
        self.access_type = 'PRO'
        self.save()

    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'
        ordering = ['-publish_date', '-created_at']
