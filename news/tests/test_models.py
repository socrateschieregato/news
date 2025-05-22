import pytest
from django.db import IntegrityError
from news.models import News
from users.models import Vertical
from factory.django import DjangoModelFactory
from factory import Faker
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = Faker('user_name')
    email = Faker('email')
    password = Faker('password')
    user_type = 'READER'

pytestmark = pytest.mark.django_db

class TestNews:
    def test_create_news(self, news_item):
        assert news_item.title
        assert news_item.subtitle
        assert news_item.content
        assert news_item.author
        assert news_item.vertical
        assert news_item.access_type == 'PUBLIC'
        assert not news_item.is_pro

    def test_news_str(self, news_item):
        assert str(news_item) == news_item.title

    def test_news_publish(self, news_item):
        assert news_item.access_type == 'PUBLIC'
        news_item.publish()
        assert news_item.access_type == 'PUBLIC'
        assert not news_item.is_pro

    def test_news_unpublish(self, news_item):
        news_item.publish()
        assert news_item.access_type == 'PUBLIC'
        news_item.unpublish()
        assert news_item.access_type == 'PRO'

    def test_news_pro_content(self, news_item):
        assert not news_item.is_pro
        news_item.make_pro()
        assert news_item.is_pro
        assert news_item.access_type == 'PRO'
        news_item.make_public()
        assert not news_item.is_pro
        assert news_item.access_type == 'PUBLIC'

    def test_news_requires_vertical(self):
        author = UserFactory()
        with pytest.raises(IntegrityError):
            News.objects.create(
                title='Test News',
                subtitle='Test Subtitle',
                content='Test Content',
                author=author
            ) 