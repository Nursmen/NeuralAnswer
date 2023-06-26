from django.contrib import admin
from .models import QA, QA_en

# Register your models here.
admin.site.register(QA)
admin.site.register(QA_en)