from django.contrib import admin
from polls.models import Questions, Choice

# Register your models here.

admin.site.register(Questions)
admin.site.register(Choice)