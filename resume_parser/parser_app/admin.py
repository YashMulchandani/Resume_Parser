from django.contrib import admin
from .models import *

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
