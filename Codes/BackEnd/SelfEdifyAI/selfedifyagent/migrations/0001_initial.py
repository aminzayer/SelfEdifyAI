# Generated by Django 4.2.7 on 2025-02-14 18:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subcategories",
                        to="selfedifyagent.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Information",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField(unique=True)),
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("summary", models.TextField(blank=True)),
                ("source_type", models.CharField(default="website", max_length=50)),
                ("author", models.CharField(blank=True, max_length=255)),
                ("publication_date", models.DateField(blank=True, null=True)),
                (
                    "credibility_score",
                    models.FloatField(
                        default=0.5,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "credibility_level",
                    models.CharField(
                        choices=[
                            ("HIGH", "High Credibility"),
                            ("MEDIUM", "Medium Credibility"),
                            ("LOW", "Low Credibility"),
                            ("UNKNOWN", "Unknown Credibility"),
                        ],
                        default="UNKNOWN",
                        max_length=10,
                    ),
                ),
                ("times_accessed", models.PositiveIntegerField(default=0)),
                ("last_accessed", models.DateTimeField(blank=True, null=True)),
                ("verification_status", models.BooleanField(default=False)),
                ("crawled_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("tags", models.JSONField(blank=True, default=list)),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="information", to="selfedifyagent.category"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LongTermMemory",
            fields=[
                (
                    "information",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="selfedifyagent.information",
                    ),
                ),
                (
                    "importance",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ]
                    ),
                ),
                ("associations", models.JSONField(default=dict)),
                ("knowledge_graph", models.JSONField(default=dict)),
                (
                    "confidence_score",
                    models.FloatField(
                        default=0.5,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "mastery_level",
                    models.FloatField(
                        default=0.0,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                ("reinforcement_count", models.PositiveIntegerField(default=0)),
                ("last_reinforced", models.DateTimeField(blank=True, null=True)),
                ("verified_by_sources", models.PositiveIntegerField(default=0)),
                ("verification_notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Long Term Memories",
            },
        ),
        migrations.CreateModel(
            name="ShortTermMemory",
            fields=[
                (
                    "information",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="selfedifyagent.information",
                    ),
                ),
                (
                    "relevance_score",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ]
                    ),
                ),
                ("context", models.TextField()),
                (
                    "comprehension_level",
                    models.FloatField(
                        default=0.0,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
                (
                    "priority_level",
                    models.PositiveSmallIntegerField(
                        default=5,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                ("expiration_time", models.DateTimeField(blank=True, null=True)),
                ("last_reviewed", models.DateTimeField(auto_now=True)),
                ("related_concepts", models.JSONField(blank=True, default=list)),
                ("learning_notes", models.TextField(blank=True)),
            ],
            options={
                "verbose_name_plural": "Short Term Memories",
            },
        ),
    ]
