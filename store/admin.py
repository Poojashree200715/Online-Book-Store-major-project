from django.contrib import admin

from .gemini import get_book_summary
from .models import Book, Category, Order, OrderItem, Subscriber


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
    actions = ["generate_summaries"]

    @admin.action(description="Generate AI summaries for selected books")
    def generate_summaries(self, request, queryset):
        done = 0
        total = queryset.count()
        for book in queryset:
            summary = get_book_summary(book.title, book.author)
            if summary:
                book.summary = summary
                book.save(update_fields=["summary"])
                done += 1
        self.message_user(request, f"Generated {done} of {total} summaries.")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    search_fields = ("email",)
    readonly_fields = ("subscribed_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("book", "title", "price", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "phone", "total", "created_at")
    search_fields = ("customer_name", "phone")
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]