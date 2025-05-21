import pytest
from django.urls import reverse
from rest_framework import status
from news.models import News

pytestmark = pytest.mark.django_db

class TestNewsAPI:
    def test_list_news_unauthorized(self, api_client):
        url = reverse('news-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_news_authorized(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        url = reverse('news-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_news_editor(self, api_client, editor_user, category):
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-list')
        data = {
            'title': 'Test News',
            'subtitle': 'Test Subtitle',
            'content': 'Test Content',
            'status': 'draft',
            'is_pro': False,
            'category_id': category.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert News.objects.count() == 1
        assert News.objects.first().author == editor_user

    def test_create_news_regular_user(self, api_client, regular_user, category):
        api_client.force_authenticate(user=regular_user)
        url = reverse('news-list')
        data = {
            'title': 'Test News',
            'subtitle': 'Test Subtitle',
            'content': 'Test Content',
            'status': 'draft',
            'is_pro': False,
            'category_id': category.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_own_news(self, api_client, editor_user, news_item):
        news_item.author = editor_user
        news_item.save()
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-detail', kwargs={'pk': news_item.pk})
        data = {
            'title': 'Updated Title',
            'subtitle': news_item.subtitle,
            'content': news_item.content,
            'status': news_item.status,
            'is_pro': news_item.is_pro,
            'category_id': news_item.category.id
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        news_item.refresh_from_db()
        assert news_item.title == 'Updated Title'

    def test_update_others_news(self, api_client, editor_user, news_item):
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-detail', kwargs={'pk': news_item.pk})
        data = {
            'title': 'Updated Title',
            'subtitle': news_item.subtitle,
            'content': news_item.content,
            'status': news_item.status,
            'is_pro': news_item.is_pro,
            'category_id': news_item.category.id
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_own_news(self, api_client, editor_user, news_item):
        news_item.author = editor_user
        news_item.save()
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-detail', kwargs={'pk': news_item.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert News.objects.count() == 0

    def test_delete_others_news(self, api_client, editor_user, news_item):
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-detail', kwargs={'pk': news_item.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert News.objects.count() == 1

    def test_pro_content_access(self, api_client, regular_user, news_item):
        news_item.is_pro = True
        news_item.save()
        api_client.force_authenticate(user=regular_user)
        url = reverse('news-detail', kwargs={'pk': news_item.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND 