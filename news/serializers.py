from rest_framework import serializers
from .models import News, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'vertical']

class NewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )

    class Meta:
        model = News
        fields = [
            'id', 'title', 'subtitle', 'content', 'image',
            'author', 'category', 'category_id', 'status',
            'is_pro', 'publish_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at'] 