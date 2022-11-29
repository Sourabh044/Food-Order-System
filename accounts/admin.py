from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import UserProfile, User
<<<<<<< HEAD
from mapwidgets import GooglePointFieldWidget
from django.contrib.gis.db import models
=======

>>>>>>> c64ac00cf1bee929791284b6fa6d91e088e004ab
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "role", "is_active")
    ordering = ("-date_joined",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)

<<<<<<< HEAD

class CustomUserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_fullname', ]
    ordering = ('-modified_date',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget},
    }

    def get_fullname(self, obj):
        return obj.user.get_fullname


admin.site.register(UserProfile, CustomUserProfileAdmin)
=======
# class CustomUserProfileAdmin(UserAdmin):
#     list_display = ("email", "first_name", "last_name", "role", "is_active")
#     ordering = ("-date_joined",)
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

admin.site.register(UserProfile)
>>>>>>> c64ac00cf1bee929791284b6fa6d91e088e004ab
