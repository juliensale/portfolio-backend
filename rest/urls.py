from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest import views

router = DefaultRouter()
router.register('technology', views.TechnologyItemViewSet)
router.register('skill', views.SkillItemViewSet)

app_name = 'rest'
urlpatterns = [
    path('', include(router.urls))
]
