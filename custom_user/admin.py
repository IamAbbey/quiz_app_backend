import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse, path
from django.contrib import messages
from django.utils import timezone

from django.http import HttpResponseRedirect, JsonResponse

from .models import EmailRecord

# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    # JSON endpoint for generating chart data that is used for dynamic loading
    # via JS.
    def chart_data_endpoint(self, request):
        past_24hrs = self.chart_data(days=1)
        past_week = self.chart_data(days=7)
        past_month = self.chart_data(days=31)

        return JsonResponse([past_24hrs, past_week, past_month], safe=False)

    def chart_data(self, days):
        date_from = timezone.now() - datetime.timedelta(days=days)
        return User.objects.filter(date_joined__gte=date_from).count()

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            self.message_user(
                request,
                "User with ID “{0}” doesn’t exist. Perhaps it was deleted?".format(pk),
                level=messages.WARNING,
            )
            return HttpResponseRedirect(reverse("admin:auth_user_changelist"))

    def set_active(self, request, pk):
        user = self.get_user(pk)
        user.is_active = True
        user.save()
        self.message_user(
            request,
            "User with ID “{0}” has been succesfully changed to active.".format(pk),
            level=messages.INFO,
        )
        return HttpResponseRedirect(reverse("admin:auth_user_changelist"))

    def set_inactive(self, request, pk):
        user = self.get_user(pk)
        user.is_active = False
        user.save()
        self.message_user(
            request,
            "User with ID “{0}” has been succesfully changed to not active.".format(pk),
            level=messages.INFO,
        )
        return HttpResponseRedirect(reverse("admin:auth_user_changelist"))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("set/active/<int:pk>", self.set_active, name="set-active"),
            path("set/inactive/<int:pk>", self.set_inactive, name="set-inactive"),
            path("chart/data", self.chart_data_endpoint, name="chart-data"),
        ]
        return my_urls + urls

    change_list_template = "custom_admin/change_list.html"

    search_fields = ["email"]

    UserAdmin.list_display += (
        "is_active",
        "change_active_status_btn",
    )

    def change_active_status_btn(self, obj):
        if obj.is_active:
            return format_html(
                '<a class="button" href="{}" style="background: red">Set Inactive</a>',
                reverse("admin:set-inactive", args=[obj.pk]),
            )
        else:
            return format_html(
                '<a class="button" href="{}">Set Active</a>',
                reverse("admin:set-active", args=[obj.pk]),
            )

    change_active_status_btn.short_description = "Change Active Status"


@admin.register(EmailRecord)
class EmailRecordAdmin(admin.ModelAdmin):
    readonly_fields = [
        "no_of_user",
    ]

    list_display = [
        "subject",
        "message",
        "no_of_user",
        "created_date",
        "updated_date",
    ]
