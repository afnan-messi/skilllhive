from django.urls import path
from . import views

urlpatterns = [
    path('', views.research_hub, name='research_hub'),
    path('upload/', views.upload_paper, name='upload_paper'),
    path('paper/<int:paper_id>/', views.paper_detail, name='paper_detail'),
    path('leaderboard/', views.research_leaderboard, name='research_leaderboard'),
]
