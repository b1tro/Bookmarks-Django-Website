from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.auth import get_user_model

from django.db.models.signals import pre_save
from django.dispatch import receiver

from datetime import datetime, timedelta
class Action(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.PositiveSmallIntegerField()
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id'])
        ]

    def __str__(self):
        return f"{self.user} {self.verb} {self.target}"
