from django.contrib.auth.models import AbstractUser
from django.db import models

class Vertical(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Vertical'
        verbose_name_plural = 'Verticais'

class Plan(models.Model):
    PLAN_TYPES = [
        ('INFO', 'JOTA Info'),
        ('PRO', 'JOTA PRO'),
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=4, choices=PLAN_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    verticais = models.ManyToManyField(Vertical, related_name='plans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_plan_type_display()} - {self.name}"

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

class User(AbstractUser):
    USER_TYPES = [
        ('ADMIN', 'Administrador'),
        ('EDITOR', 'Editor'),
        ('READER', 'Leitor'),
    ]

    user_type = models.CharField(max_length=6, choices=USER_TYPES, default='READER')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_admin(self):
        return self.user_type == 'ADMIN'

    def is_editor(self):
        return self.user_type == 'EDITOR'

    def is_reader(self):
        return self.user_type == 'READER'

    def has_pro_access(self):
        return self.plan and self.plan.plan_type == 'PRO'

    def can_access_vertical(self, vertical):
        if not self.has_pro_access():
            return False
        return vertical in self.plan.verticais.all()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
