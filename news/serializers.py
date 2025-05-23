from rest_framework import serializers
from .models import News
from users.serializers import VerticalSerializer
from users.models import Vertical

class NewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    vertical = VerticalSerializer(read_only=True)
    vertical_id = serializers.PrimaryKeyRelatedField(
        queryset=Vertical.objects.all(),
        write_only=True,
        source='vertical'
    )

    class Meta:
        model = News
        fields = [
            'id', 'title', 'subtitle', 'content', 'image',
            'author', 'vertical', 'vertical_id', 'access_type',
            'status', 'publish_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at'] 