from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Information(models.Model):
    CREDIBILITY_CHOICES = [
        ('HIGH', 'High Credibility'),
        ('MEDIUM', 'Medium Credibility'),
        ('LOW', 'Low Credibility'),
        ('UNKNOWN', 'Unknown Credibility'),
    ]

    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='information')
    
    # Metadata
    source_type = models.CharField(max_length=50, default='website')
    author = models.CharField(max_length=255, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    credibility_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.5
    )
    credibility_level = models.CharField(
        max_length=10,
        choices=CREDIBILITY_CHOICES,
        default='UNKNOWN'
    )
    
    # Learning tracking
    times_accessed = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(null=True, blank=True)
    verification_status = models.BooleanField(default=False)
    
    # Timestamps
    crawled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional metadata
    metadata = JSONField(default=dict, blank=True)
    tags = JSONField(default=list, blank=True)

    def __str__(self):
        return self.title

    def access(self):
        self.times_accessed += 1
        self.last_accessed = timezone.now()
        self.save()


class ShortTermMemory(models.Model):
    information = models.OneToOneField(Information, on_delete=models.CASCADE, primary_key=True)
    relevance_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    context = models.TextField()
    
    # Learning progress
    comprehension_level = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0
    )
    priority_level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    
    # Temporal aspects
    expiration_time = models.DateTimeField(null=True, blank=True)
    last_reviewed = models.DateTimeField(auto_now=True)
    
    # Additional context
    related_concepts = JSONField(default=list, blank=True)
    learning_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Short-Term Memory of '{self.information.title}'"

    class Meta:
        verbose_name_plural = "Short Term Memories"


class LongTermMemory(models.Model):
    information = models.OneToOneField(Information, on_delete=models.CASCADE, primary_key=True)
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    
    # Knowledge representation
    associations = JSONField(default=dict)
    knowledge_graph = JSONField(default=dict)
    
    # Learning metrics
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.5
    )
    mastery_level = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0
    )
    
    # Reinforcement learning
    reinforcement_count = models.PositiveIntegerField(default=0)
    last_reinforced = models.DateTimeField(null=True, blank=True)
    
    # Validation
    verified_by_sources = models.PositiveIntegerField(default=0)
    verification_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Long-Term Memory of '{self.information.title}'"

    def reinforce(self):
        self.reinforcement_count += 1
        self.last_reinforced = timezone.now()
        self.save()

    class Meta:
        verbose_name_plural = "Long Term Memories"
