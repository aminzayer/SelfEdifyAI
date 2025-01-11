from rest_framework import serializers
from .models import Category, Information, ShortTermMemory, LongTermMemory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = [
            'id', 'url', 'title', 'content', 'summary', 'categories',
            'source_type', 'author', 'publication_date', 'credibility_score',
            'credibility_level', 'times_accessed', 'last_accessed',
            'verification_status', 'crawled_at', 'updated_at',
            'metadata', 'tags'
        ]
        read_only_fields = ['crawled_at', 'updated_at', 'times_accessed', 'last_accessed']

class ShortTermMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortTermMemory
        fields = [
            'information', 'relevance_score', 'context',
            'comprehension_level', 'priority_level',
            'expiration_time', 'last_reviewed',
            'related_concepts', 'learning_notes'
        ]
        read_only_fields = ['last_reviewed']

class LongTermMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTermMemory
        fields = [
            'information', 'importance', 'associations',
            'knowledge_graph', 'confidence_score', 'mastery_level',
            'reinforcement_count', 'last_reinforced',
            'verified_by_sources', 'verification_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'reinforcement_count', 'last_reinforced']
