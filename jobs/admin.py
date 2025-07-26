from django.contrib import admin
from .models import Job, Application, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "location", "posted_by", "created_at")
    search_fields = ("title", "company_name", "location", "posted_by__username")
    list_filter = ("company_name", "location", "created_at")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "applicant", "applied_at")
    search_fields = ("job__title", "applicant__username")
    list_filter = ("applied_at",)
