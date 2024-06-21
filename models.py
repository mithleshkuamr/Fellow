# models.py
from django.db import models

class Comment(models.Model):
    work_platform_id = models.CharField(max_length=100)
    content_url = models.URLField()
    text = models.TextField()
    commenter_username = models.CharField(max_length=100)
    commenter_display_name = models.CharField(max_length=100)
    like_count = models.IntegerField()
    reply_count = models.IntegerField()
    published_at = models.DateTimeField()

    def __str__(self):
        return self.text
