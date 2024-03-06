from django.contrib import admin
from django.utils.html import format_html

from accounts.models import (
    GoogleCalendarChannel,
    GoogleCredentials,
    OrganizationProfile,
    User,
)


class GoogleCredentialsInline(admin.StackedInline):
    model = GoogleCredentials
    can_delete = False
    verbose_name_plural = "Google Credentials"


class UserAdmin(admin.ModelAdmin):
    inlines = (GoogleCredentialsInline,)

    list_display = [
        "id",
        "email",
        "username",
        "phone",
        "date_of_birth",
        "profile_picture",
        "email_verified",
        "profile_picture_img",
    ]
    list_filter = ["email_verified", "date_of_birth"]
    search_fields = ["email", "username", "phone"]

    def profile_picture_img(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" />', obj.profile_picture.url
            )
        return "-"

    profile_picture_img.short_description = "Profile Picture"


class GoogleCredentialsAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "access_token",
        "refresh_token",
        "token_expiry",
    ]
    search_fields = ["user__email"]


class GoogleCalendarChannelAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_display = (
        "user",
        "channel_id",
        "resource_id",
        "expiration",
        "verification_token_shortened",
    )
    list_filter = ("user",)
    search_fields = ("user__username", "user__email", "channel_id", "resource_id")
    readonly_fields = ("channel_id", "verification_token", "resource_id")

    def verification_token_shortened(self, obj):
        """Display only the first and last few characters of the verification token."""
        if obj.verification_token:
            return f"{obj.verification_token[:6]}...{obj.verification_token[-6:]}"
        return "-"

    verification_token_shortened.short_description = "Verification Token"


class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "bio", "city", "address", "country", "zip_code"]
    list_filter = ["city", "country"]
    search_fields = ["name", "bio", "city", "address", "zip_code"]
    raw_id_fields = ["user"]


admin.site.register(User, UserAdmin)
admin.site.register(GoogleCredentials, GoogleCredentialsAdmin)
admin.site.register(GoogleCalendarChannel, GoogleCalendarChannelAdmin)
admin.site.register(OrganizationProfile, OrganizationProfileAdmin)
