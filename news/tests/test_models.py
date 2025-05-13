import pytest
from django.db import IntegrityError
from news.models import News, Category

pytestmark = pytest.mark.django_db

class TestCategory:
    def test_create_category(self, category):
        assert category.name
        assert category.slug
        assert str(category) == category.name

    def test_category_unique_slug(self, category):
        with pytest.raises(IntegrityError):
            Category.objects.create(
                name="Another Category",
                slug=category.slug
            )

class TestNews:
    def test_create_news(self, news_item):
        assert news_item.title
        assert news_item.subtitle
        assert news_item.content
        assert news_item.author
        assert news_item.category
        assert news_item.status == 'draft'
        assert not news_item.is_pro

    def test_news_str(self, news_item):
        assert str(news_item) == news_item.title

    def test_news_publish(self, news_item):
        assert news_item.status == 'draft'
        news_item.publish()
        assert news_item.status == 'published'

    def test_news_unpublish(self, news_item):
        news_item.publish()
        assert news_item.status == 'published'
        news_item.unpublish()
        assert news_item.status == 'draft'

    def test_news_pro_content(self, news_item):
        assert not news_item.is_pro
        news_item.make_pro()
        assert news_item.is_pro
        news_item.make_public()
        assert not news_item.is_pro 