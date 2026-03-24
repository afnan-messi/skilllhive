from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('matches/', views.matches_view, name='matches'),
    path('game/', views.game_view, name='game'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('how-it-works/', views.how_it_works_view, name='how_it_works'),
    path('skills/', views.skills_view, name='skills'),
    path('matching/', views.matching_view, name='matching'),
    path('about/', views.about_view, name='about'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    path('careers/', views.careers_view, name='careers'),
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
