from __future__ import unicode_literals

from django.contrib import admin
from mysite.core import models

admin.site.register(models.Profile)
admin.site.register(models.Languages)