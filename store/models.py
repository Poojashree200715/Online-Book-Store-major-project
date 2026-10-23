from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True)
    icon = models.CharField(max_length=4, blank=True, help_text="Optional emoji, e.g. 📚")

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="books")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    cover_color = models.CharField(
        max_length=7, default="#426957",
        help_text="Hex colour used for the placeholder cover when there is no image.",
    )
    # Featured sections
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_audiobook = models.BooleanField(default=False)
    # Team 4: cache for the Gemini summary so the API is not called on every page view
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email


# ---------------------------------------------------------------- Team 4 ---

class Order(models.Model):
    """A dummy order created at checkout (no real payment is taken)."""
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    # Title and price are copied at purchase time, so later edits to the book
    # do not change past orders.
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.title}"
