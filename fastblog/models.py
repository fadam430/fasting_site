from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

# Create your models here.

class FastingDuration(models.IntegerChoices):
    H18 = 18, '18-hours'
    H24 = 24, '24-hours'
    H36 = 36, '36-hours'


class Fasting_Plan(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE , related_name='fasting_plans')
    # duration is required (no blank/null) and defaults to 18
    duration = models.IntegerField(choices=FastingDuration.choices, default=FastingDuration.H18, null=False, blank=False)
    monday_plan = models.TextField()
    tuesday_plan = models.TextField()
    wednesday_plan = models.TextField()
    thursday_plan = models.TextField()
    friday_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Title of fasting plan: {self.title}"
    
class Reviews(models.Model):
    fasting_plan = models.ForeignKey(Fasting_Plan, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"Review by {self.reviewer.username} with rating {self.rating}"