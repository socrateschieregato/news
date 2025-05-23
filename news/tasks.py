from django.utils import timezone
from .models import News
from jota_news.celery import app

@app.task
def publish_scheduled_news():
    """
    Task que publica notícias agendadas que já passaram da data de publicação
    """
    now = timezone.now()
    scheduled_news = News.objects.filter(
        status='SCHEDULED',
        publish_date__lte=now
    )
    
    print(f"total_scheduled_news = {len(scheduled_news)}")
    for news in scheduled_news:
        news.publish()


@app.task
def schedule_news_publication(news_id, publish_date):
    """
    Task que agenda uma notícia para publicação
    """
    try:
        news = News.objects.get(id=news_id)
        news.schedule_publish(publish_date)
        return f"Notícia {news.title} agendada para publicação em {publish_date}"
    except News.DoesNotExist:
        return f"Notícia com ID {news_id} não encontrada" 