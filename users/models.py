from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile.png', blank=True)
    banner_image = models.ImageField(upload_to='banners/', default='default_banner.jpg', blank=True)
    skills_offered = models.TextField(blank=True, help_text="Comma separated skills")
    skills_to_learn = models.TextField(blank=True, help_text="Comma separated skills")
    upcoming_sessions = models.IntegerField(default=0)
    sessions_completed = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class NQueensProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nqueens_progress')
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s NQueens Progress"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
