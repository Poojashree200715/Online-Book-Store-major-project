from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Book, Category, Subscriber


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
    related = Book.objects.filter(category=book.category).exclude(pk=book.pk)[:4]
    # Team 4: call the Gemini helper here and fill book.summary if it is empty.
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
