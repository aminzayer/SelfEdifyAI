from django.contrib import admin
from .models import *


class InformationAdmin(admin.ModelAdmin):
    list_per_page = 20


admin.site.register(Information, InformationAdmin)
