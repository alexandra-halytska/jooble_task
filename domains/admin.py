from django.contrib import admin

from .models import Url, Domain

admin.site.register(Url)
admin.site.register(Domain)
