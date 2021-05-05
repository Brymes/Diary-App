import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Diary(models.Model):
    # entry_no is consideration for MongoDB integration
    # entry_id = models.AutoField(primary_key=True)
    entry_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=80)
    entry = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE)
    # FIXME add bookmarks
