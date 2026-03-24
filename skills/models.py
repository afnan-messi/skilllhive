from django.db import models
from django.contrib.auth.models import User

class UserSkill(models.Model):
    SKILL_TYPE_CHOICES = [
        ('Teach', 'I can Teach this skill'),
        ('Learn', 'I want to Learn this skill'),
    ]
    
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ]
    
    CATEGORY_CHOICES = [
        ('Programming', 'Programming'),
        ('Design', 'Design'),
        ('Languages', 'Languages'),
        ('Music', 'Music'),
        ('Business', 'Business'),
        ('Marketing', 'Marketing'),
        ('Photography', 'Photography'),
        ('Cooking', 'Cooking'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill_name = models.CharField(max_length=255)
    skill_type = models.CharField(max_length=10, choices=SKILL_TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField()
    demo_file = models.FileField(upload_to='skill_demos/', null=True, blank=True)
    availability = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.skill_name} ({self.skill_type}) - {self.user.username}"
