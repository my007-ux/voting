from django.db import models
from core.settings import AUTH_USER_MODEL
class Base(models.Model):
    created_by = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True,
                                   related_name="%(app_label)s_%(class)s_created_by", on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(AUTH_USER_MODEL, blank=True, related_name="%(app_label)s_%(class)s_modified_by",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=2, null=True, blank=True)

    class Meta:
        abstract = True