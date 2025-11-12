from django.contrib import admin
from .models import *


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(UserProfile)