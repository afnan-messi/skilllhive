from django.db import models
from django.contrib.auth.models import User

class ResearchPaper(models.Model):
    CATEGORIES = [
        ('AI', 'Artificial Intelligence'),
        ('CS', 'Computer Science'),
        ('ENG', 'Engineering'),
        ('MATH', 'Mathematics'),
        ('PHYS', 'Physics'),
        ('BIO', 'Biology'),
    ]
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    paper_file = models.FileField(upload_to='research_papers/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='papers')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=CATEGORIES)
    points = models.IntegerField(default=20)

    def __str__(self):
        return self.title

class PaperReview(models.Model):
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.paper.title} by {self.reviewer.username}"

class Discussion(models.Model):
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, related_name='discussions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.paper.title}"
