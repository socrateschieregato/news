import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from news.models import News, Category
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    password = Faker('password')

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker('word')
    slug = Faker('slug')

class NewsFactory(DjangoModelFactory):
    class Meta:
        model = News

    title = Faker('sentence')
    subtitle = Faker('sentence')
    content = Faker('paragraph')
    author = SubFactory(UserFactory)
    category = SubFactory(CategoryFactory)
    status = 'draft'
    is_pro = False

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return UserFactory(is_staff=True, is_superuser=True)

@pytest.fixture
def editor_user():
    return UserFactory(is_staff=True)

@pytest.fixture
def regular_user():
    return UserFactory()

@pytest.fixture
def news_item():
    return NewsFactory()

@pytest.fixture
def category():
    return CategoryFactory() 