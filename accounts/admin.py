from django.contrib import admin

from accounts.models import OrganizationCustomer, OrganizationProfile, User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "username",
        "phone",
        "date_of_birth",
        "profile_picture",
        "email_verified",
    ]


class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "bio", "city", "address", "country", "zip_code"]


admin.site.register(User, UserAdmin)
admin.site.register(OrganizationProfile, OrganizationProfileAdmin)
