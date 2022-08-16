from django.contrib import admin

from .models import Agent, Lead, OrganizerUser


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "organizer", "agent"]


admin.site.register(OrganizerUser)
admin.site.register(Agent)

