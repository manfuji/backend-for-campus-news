from django.contrib import admin
from AllModels.models import Profile


@admin.register(Profile)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ("image", "prouser", "bio", "interest")
    list_display_links = ("prouser",)
    
