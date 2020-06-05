from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    img_src = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Sort in descending order
        ordering = ['-created_on']

    def __str__(self):
        return self.title