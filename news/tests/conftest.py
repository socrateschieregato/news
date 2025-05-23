import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from news.models import News
from users.models import Vertical, Plan
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory

User = get_user_model()

class PlanFactory(DjangoModelFactory):
    class Meta:
        model = Plan

    name = Faker('word')
    description = Faker('text')
    price = Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    plan_type = 'INFO'

class VerticalFactory(DjangoModelFactory):
    class Meta:
        model = Vertical

    name = Faker('word')
    description = Faker('text')

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    password = Faker('password')
    user_type = 'READER'
    plan = SubFactory(PlanFactory)

class NewsFactory(DjangoModelFactory):
    class Meta:
        model = News

    title = Faker('sentence')
    subtitle = Faker('sentence')
    content = Faker('paragraph')
    author = SubFactory(UserFactory)
    vertical = SubFactory(VerticalFactory)
    access_type = 'PUBLIC'

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    plan = PlanFactory(plan_type='PRO')
    return UserFactory(user_type='ADMIN', is_staff=True, is_superuser=True, plan=plan)

@pytest.fixture
def editor_user():
    plan = PlanFactory(plan_type='PRO')
    return UserFactory(user_type='EDITOR', is_staff=True, plan=plan)

@pytest.fixture
def regular_user():
    plan = PlanFactory(plan_type='INFO')
    return UserFactory(user_type='READER', plan=plan)

@pytest.fixture
def pro_user():
    plan = PlanFactory(plan_type='PRO')
    return UserFactory(user_type='READER', plan=plan)

@pytest.fixture
def vertical():
    return VerticalFactory()

@pytest.fixture
def news_item(vertical):
    return NewsFactory(vertical=vertical)
