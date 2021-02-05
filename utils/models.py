"""
Utilities for created_at and modified_at fields
"""

# Django
from django.db import models

class TimestampsModel(models.Model):
    """
    UtilsModel provides a base class from which other models will inherit.
    This class provides the following attributes:
    - created_at: timestamp that store th datetime the object was created
    - modified_at: timestamp that store th datetime the object was modified
    """
    created_at = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created'
    )
    modified_at = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was modified'
    )

    class Meta:
        abstract = True

        get_latest_by = 'created_at'
        ordering = ['-created_at', '-modified_at']
