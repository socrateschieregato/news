import pytest
from django.db import IntegrityError
from news.models import News
from users.models import Vertical
from factory.django import DjangoModelFactory
from factory import Faker
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = Faker('user_name')
    email = Faker('email')
    password = Faker('password')
    user_type = 'READER'

pytestmark = pytest.mark.django_db

class TestNewsModel:
    def test_create_news(self, editor_user, vertical):
        news = News.objects.create(
            title='Test News',
            subtitle='Test Subtitle',
            content='Test Content',
            author=editor_user,
            vertical=vertical,
            access_type='PUBLIC'
        )
        assert news.title == 'Test News'
        assert news.subtitle == 'Test Subtitle'
        assert news.content == 'Test Content'
        assert news.author == editor_user
        assert news.vertical == vertical
        assert news.access_type == 'PUBLIC'
        assert news.status == 'DRAFT'

    def test_publish_news(self, news_item):
        assert news_item.status == 'DRAFT'
        news_item.publish()
        assert news_item.status == 'PUBLISHED'
        assert news_item.publish_date is not None

    def test_schedule_news(self, news_item):
        future_date = timezone.now() + timezone.timedelta(days=1)
        news_item.schedule_publish(future_date)
        assert news_item.status == 'SCHEDULED'
        assert news_item.publish_date == future_date

    def test_unpublish_news(self, news_item):
        news_item.publish()
        assert news_item.status == 'PUBLISHED'
        news_item.unpublish()
        assert news_item.status == 'DRAFT'
        assert news_item.publish_date is None

    def test_news_str(self, news_item):
        assert str(news_item) == news_item.title

    def test_news_publish(self, news_item):
        assert news_item.access_type == 'PUBLIC'
        news_item.publish()
        assert news_item.access_type == 'PUBLIC'

    def test_news_unpublish(self, news_item):
        news_item.publish()
        assert news_item.access_type == 'PUBLIC'
        news_item.unpublish()
        assert news_item.access_type == 'PUBLIC'

    def test_news_pro_content(self, news_item):
        assert news_item.access_type == 'PUBLIC'
        news_item.access_type = 'PRO'
        news_item.save()
        assert news_item.access_type == 'PRO'
        news_item.access_type = 'PUBLIC'
        news_item.save()
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