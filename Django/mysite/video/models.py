from django.conf import settings
from django.db import models

class Videos(models.Model):
    video_id = models.CharField(blank=False, max_length=32, primary_key=True)
    file_name = models.CharField(blank=False, max_length=500)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.video_id