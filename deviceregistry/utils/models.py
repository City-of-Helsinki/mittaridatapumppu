from django.db import models


# Base class for all models, which have created_at and updated_at fields
class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This model will not be created in the database
