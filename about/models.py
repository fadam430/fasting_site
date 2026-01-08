from django.db import models # type: ignore

# Create your models here.
class About(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title