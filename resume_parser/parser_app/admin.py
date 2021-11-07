from django.contrib import admin
from .models import *

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'username', 'Number_of_Resumes', 'Subscription')
