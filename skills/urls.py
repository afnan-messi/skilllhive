from django.urls import path
from . import views

urlpatterns = [
    path('', views.skills_page, name='skills_page'),
    path('add-skill/', views.add_skill_view, name='add_skill'),
]
