import csv

from django.contrib import admin
from django.http import HttpResponse

from .models_newsletter import Subscriber


@admin.action(description='Export selected subscribers to CSV')
def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email', 'Subscribed at', 'Active'])
    for s in queryset:
        writer.writerow([s.email, s.subscribed_at, s.is_active])
    return response


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    actions = [export_csv]


# Admin site branding
admin.site.site_header = 'BookHaven Admin'
admin.site.site_title = 'BookHaven'
admin.site.index_title = 'Manage your bookstore'
