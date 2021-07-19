from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest import views

router = DefaultRouter()
router.register('technology', views.TechnologyItemViewSet)
router.register('skill', views.SkillItemViewSet)
router.register('project', views.ProjectItemViewSet)
router.register('review', views.ReviewItemViewSet)

app_name = 'rest'
urlpatterns = [
    path('', include(router.urls))
]
