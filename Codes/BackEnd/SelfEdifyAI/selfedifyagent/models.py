from django.db import models
from django.contrib.postgres.fields import JSONField


class Information(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    crawled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ShortTermMemory(models.Model):
    information = models.OneToOneField(Information, on_delete=models.CASCADE, primary_key=True)
    relevance_score = models.FloatField()
    context = models.TextField()

    def __str__(self):
        return f"Short-Term Memory of '{self.information.title}'"


class LongTermMemory(models.Model):
    information = models.OneToOneField(Information, on_delete=models.CASCADE, primary_key=True)
    importance = models.IntegerField()
    associations = JSONField(default=dict)

    def __str__(self):
        return f"Long-Term Memory of '{self.information.title}'"
