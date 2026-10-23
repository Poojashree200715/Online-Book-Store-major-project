import json
from decimal import Decimal

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CheckoutForm
from .gemini import get_book_summary
from .models import Book, Category, Order, OrderItem, Subscriber

MAX_QTY_PER_BOOK = 20


def home(request):
    category_slug = request.GET.get("category", "")
    query = request.GET.get("q", "").strip()

    books = Book.objects.select_related("category")
    if category_slug:
        books = books.filter(category__slug=category_slug)
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    all_books = Book.objects.select_related("category")
    context = {
        "categories": Category.objects.all(),
        "books": books,
        "selected_category": category_slug,
        "query": query,
        "bestsellers": all_books.filter(is_bestseller=True)[:4],
        "new_arrivals": all_books.filter(is_new_arrival=True)[:4],
        "audiobooks": all_books.filter(is_audiobook=True)[:4],
    }
    return render(request, "store/home.html", context)


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related("category"), pk=pk)

    # Team 4: fetch the AI summary once, then reuse the saved copy on later visits.
    if not book.summary:
        summary = get_book_summary(book.title, book.author)
        if summary:
            book.summary = summary
            book.save(update_fields=["summary"])

    related = Book.objects.filter(category=book.category).exclude(pk=book.pk)[:4]
    return render(request, "store/book_detail.html", {"book": book, "related": related})


@require_POST
def subscribe(request):
    email = request.POST.get("email", "").strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Please enter a valid email address.")
        return redirect("/#newsletter")

    _, created = Subscriber.objects.get_or_create(email=email)
    if created:
        messages.success(request, "Thank you for subscribing!")
    else:
        messages.info(request, "You are already subscribed.")
    return redirect("/#newsletter")


# ---------------------------------------------------------------- Team 4 ---

def parse_cart(raw):
    """Turn the cart JSON sent by the browser into [(Book, quantity), ...].

    Only book ids and quantities are trusted. Titles and prices always come
    from the database, so a visitor cannot change a price from the browser.
    """
    try:
        data = json.loads(raw)
    except (TypeError, ValueError):
        return []
    if not isinstance(data, list):
        return []

    quantities = {}
    for entry in data:
        if not isinstance(entry, dict):
            continue
        try:
            book_id = int(entry.get("id"))
            qty = int(entry.get("qty", 1))
        except (TypeError, ValueError):
            continue
        if qty < 1:
            continue
        quantities[book_id] = min(quantities.get(book_id, 0) + qty, MAX_QTY_PER_BOOK)

    books = Book.objects.in_bulk(list(quantities))
    return [(books[book_id], qty) for book_id, qty in quantities.items() if book_id in books]


def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            items = parse_cart(form.cleaned_data["cart"])
            if items:
                with transaction.atomic():
                    order = Order.objects.create(
                        customer_name=form.cleaned_data["name"],
                        phone=form.cleaned_data["phone"],
                        address=form.cleaned_data["address"],
                    )
                    total = Decimal("0")
                    for book, qty in items:
                        OrderItem.objects.create(
                            order=order, book=book, title=book.title,
                            price=book.price, quantity=qty,
                        )
                        total += book.price * qty
                    order.total = total
                    order.save(update_fields=["total"])
                request.session["last_order_id"] = order.pk
                return redirect("order_confirmation", pk=order.pk)
            form.add_error(None, "Your cart is empty.")
    else:
        form = CheckoutForm()
    return render(request, "store/checkout.html", {"form": form})


def order_confirmation(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=pk)
    # Only the visitor who just placed the order may see it.
    if request.session.get("last_order_id") != order.pk:
        raise Http404("Order not found.")
    return render(request, "store/order_confirmation.html", {"order": order})
