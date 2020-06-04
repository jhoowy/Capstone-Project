from django.conf import settings
from django.db import models
import os

class Videos(models.Model):
    video_id = models.CharField(blank=False, max_length=32, primary_key=True)
    file_name = models.CharField(blank=False, max_length=500)
    processed = models.BooleanField(default='False')
    progress_time = models.IntegerField(default=0)
    total_frame = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.video_id

    def get_path(self):
        formats = os.path.splitext(self.file_name)[-1].lower()
        return self.video_id + formats