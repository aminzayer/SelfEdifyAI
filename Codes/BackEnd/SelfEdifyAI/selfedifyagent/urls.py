from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'information', views.InformationViewSet)
router.register(r'short-term-memory', views.ShortTermMemoryViewSet)
router.register(r'long-term-memory', views.LongTermMemoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('learn/', views.learn_information, name='learn-information'),
    path('consolidate/<int:stm_id>/', views.consolidate_memory, name='consolidate-memory'),
]
