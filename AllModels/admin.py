from django.contrib import admin
from .models import Post, Comment
# ,Profile

@admin.register(Post)
class authorAdmin(admin.ModelAdmin):
    exlude = ("slug",)
    list_display = ("id","title","status","author","content","trending","category","campus","excerpt")
    prepopulated_fields = {"slug": ("title",)}
    list_display_links= ("id","title","trending")


@admin.register(Comment)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ("id","name","body","comment_date")
    


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ("user","university", "picture", "about","interest")
#     list_display_links = ("user",)
#     prepopulated_fields = {"slug": ("user",)}

