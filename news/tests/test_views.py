import pytest
from django.urls import reverse
from rest_framework import status
from news.models import News

pytestmark = pytest.mark.django_db

class TestNewsAPI:
    def test_list_news_unauthorized(self, api_client):
        url = reverse('news-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0

    def test_list_news_authorized(self, api_client, regular_user, news_item):
        news_item.publish()
        api_client.force_authenticate(user=regular_user)
        url = reverse('news-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_create_news_editor(self, api_client, editor_user, vertical):
        # Garante que o editor tem acesso à vertical
        editor_user.plan.verticais.add(vertical)
        
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-list')
        data = {
            'title': 'Test News',
            'subtitle': 'Test Subtitle',
            'content': 'Test Content',
            'access_type': 'PUBLIC',
            'vertical_id': vertical.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert News.objects.count() == 1
        assert News.objects.first().author == editor_user

    def test_create_news_regular_user(self, api_client, regular_user, vertical):
        # Garante que o usuário regular tem acesso à vertical
        regular_user.plan.verticais.add(vertical)
        
        api_client.force_authenticate(user=regular_user)
        url = reverse('news-list')
        data = {
            'title': 'Test News',
            'subtitle': 'Test Subtitle',
            'content': 'Test Content',
            'access_type': 'PUBLIC',
            'vertical_id': vertical.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_news_without_vertical_access(self, api_client, editor_user, vertical):
        # Remove a vertical do plano do editor
        editor_user.plan.verticais.remove(vertical)
        
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-list')
        data = {
            'title': 'Test News',
            'subtitle': 'Test Subtitle',
            'content': 'Test Content',
            'access_type': 'PUBLIC',
            'vertical_id': vertical.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['detail'] == "Seu plano não tem acesso a esta vertical."

    def test_publish_news(self, api_client, editor_user, news_item):
        # Garante que o editor tem acesso à vertical
        editor_user.plan.verticais.add(news_item.vertical)
        
        news_item.author = editor_user
        news_item.save()
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-publish', kwargs={'pk': news_item.id})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        news_item.refresh_from_db()
        assert news_item.status == 'PUBLISHED'

    def test_schedule_news(self, api_client, editor_user, news_item):
        # Garante que o editor tem acesso à vertical
        editor_user.plan.verticais.add(news_item.vertical)
        
        news_item.author = editor_user
        news_item.save()
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-schedule', kwargs={'pk': news_item.id})
        data = {'publish_date': '2026-12-31T23:59:59Z'}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        news_item.refresh_from_db()
        assert news_item.status == 'DRAFT'
        news_item.schedule_publish(data['publish_date'])
        assert news_item.status == 'SCHEDULED'

    def test_access_pro_content(self, api_client, pro_user, news_item):
        # Garante que o usuário PRO tem acesso à vertical
        pro_user.plan.verticais.add(news_item.vertical)
        
        news_item.access_type = 'PRO'
        news_item.publish()
        news_item.save()
        
        api_client.force_authenticate(user=pro_user)
        url = reverse('news-detail', kwargs={'pk': news_item.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_access_pro_content_regular_user(self, api_client, regular_user, news_item):
        # Garante que o usuário regular tem acesso à vertical
        regular_user.plan.verticais.add(news_item.vertical)
        
        news_item.access_type = 'PRO'
        news_item.save()
        
        api_client.force_authenticate(user=regular_user)
        url = reverse('news-detail', kwargs={'pk': news_item.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_own_news(self, api_client, editor_user, news_item):
        # Garante que o editor tem acesso à vertical
        editor_user.plan.verticais.add(news_item.vertical)
        
        news_item.author = editor_user
        news_item.save()
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-detail', kwargs={'pk': news_item.pk})
        data = {
            'title': 'Updated Title',
            'subtitle': news_item.subtitle,
            'content': news_item.content,
            'access_type': news_item.access_type,
            'vertical_id': news_item.vertical.id
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        news_item.refresh_from_db()
        assert news_item.title == 'Updated Title'

    def test_update_others_news(self, api_client, editor_user, news_item, regular_user):
        news_item.author = regular_user
        news_item.publish()
        news_item.save()
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-detail', kwargs={'pk': news_item.pk})
        data = {
            'title': 'Updated Title',
            'subtitle': news_item.subtitle,
            'content': news_item.content,
            'access_type': news_item.access_type,
            'vertical_id': news_item.vertical.id
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_own_news(self, api_client, editor_user, news_item):
        news_item.author = editor_user
        news_item.save()
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-detail', kwargs={'pk': news_item.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert News.objects.count() == 0

    def test_delete_others_news(self, api_client, editor_user, news_item, regular_user):
        news_item.author = regular_user
        news_item.status = 'PUBLISHED'
        news_item.save()
        api_client.force_authenticate(user=editor_user)
        url = reverse('news-detail', kwargs={'pk': news_item.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert News.objects.count() == 1

    def test_list_news_with_pro_content(self, api_client, regular_user, pro_user, news_item):
        # Garante que o usuário PRO tem acesso à vertical
        pro_user.plan.verticais.add(news_item.vertical)
        
        news_item.publish()
        news_item.save()
        pro_news = News.objects.create(
            title='Pro News',
            subtitle='Pro Subtitle',
            content='Pro Content',
            author=news_item.author,
            vertical=news_item.vertical,
            access_type='PRO',
            status='PUBLISHED'
        )

        api_client.force_authenticate(user=regular_user)
        response = api_client.get(reverse('news-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

        api_client.force_authenticate(user=pro_user)
        response = api_client.get(reverse('news-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2 