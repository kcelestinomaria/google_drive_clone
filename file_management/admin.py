from django.contrib import admin

from .models import * 

admin.site.register([Folder, File, SharedItem])

