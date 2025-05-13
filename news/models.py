from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.exceptions import ValidationError

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    vertical = models.CharField(
        max_length=20,
        choices=[
            ('PODER', 'Poder'),
            ('TRIBUTOS', 'Tributos'),
            ('SAUDE', 'Saúde'),
            ('ENERGIA', 'Energia'),
            ('TRABALHISTA', 'Trabalhista'),
        ]
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
    ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_pro = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def publish(self):
        self.status = 'published'
        self.save()

    def unpublish(self):
        self.status = 'draft'
        self.save()

    def make_pro(self):
        self.is_pro = True
        self.save()

    def make_public(self):
        self.is_pro = False
        self.save()

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-publish_date', '-created_at']
