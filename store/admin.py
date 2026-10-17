from django.contrib import admin

from .models import Book, Category, Subscriber


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "price",
                    "is_bestseller", "is_new_arrival", "is_audiobook")
    list_editable = ("is_bestseller", "is_new_arrival", "is_audiobook")
    list_filter = ("category", "is_bestseller", "is_new_arrival", "is_audiobook")
    search_fields = ("title", "author")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    search_fields = ("email",)
    readonly_fields = ("subscribed_at",)
