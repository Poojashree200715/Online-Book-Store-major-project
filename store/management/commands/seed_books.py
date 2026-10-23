from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import ProtectedError

from store.models import Book, Category

CATEGORIES = [
    ("Fiction", "fiction", "✨"),
    ("Non-fiction", "non-fiction", "📖"),
    ("Education", "education", "🎓"),
    ("Technology", "technology", "💻"),
]

# The earlier sample books (current and previous titles). They are removed.
OLD_SAMPLE_TITLES = [
    "Data Science Basics", "Data Science for Beginners",
    "Ocean of Dreams",
    "The Power of Focus",
    "Python Made Simple", "Python Made Easy",
    "Midnight Stories",
    "Future of AI", "The Future of AI",
    "Learning Every Day", "Learn Something New Every Day",
    "The Silent Garden", "The Silent Gardener",
]

# cover file name (without extension), title, author, category slug, price,
# placeholder colour, description, bestseller, new arrival
BOOKS = [
    ("to-kill-a-mockingbird", "To Kill a Mockingbird", "Harper Lee", "fiction", 349, "#7a5c3e",
     "Harper Lee's classic novel of racial injustice and childhood in the American South, seen through the eyes of young Scout Finch.",
     False, False),
    ("1984", "1984", "George Orwell", "fiction", 299, "#8c2f2f",
     "George Orwell's dystopian novel about total government surveillance, propaganda and the loss of individual freedom.",
     True, False),
    ("the-alchemist", "The Alchemist", "Paulo Coelho", "fiction", 329, "#c27e2c",
     "Paulo Coelho's fable about Santiago, a shepherd boy who travels in search of his Personal Legend.",
     True, False),
    ("pride-and-prejudice", "Pride and Prejudice", "Jane Austen", "fiction", 249, "#9b5d7a",
     "Jane Austen's witty novel of manners about Elizabeth Bennet and Mr. Darcy, and the pressures of class and marriage.",
     False, False),
    ("the-great-gatsby", "The Great Gatsby", "F. Scott Fitzgerald", "fiction", 229, "#2f6f73",
     "F. Scott Fitzgerald's story of the mysterious millionaire Jay Gatsby and the American Dream in the Jazz Age.",
     False, True),

    ("sapiens", "Sapiens: A Brief History of Humankind", "Yuval Noah Harari", "non-fiction", 499, "#c0673a",
     "Yuval Noah Harari traces the history of our species, from early humans to the modern world.",
     True, False),
    ("atomic-habits", "Atomic Habits", "James Clear", "non-fiction", 449, "#d9a441",
     "James Clear explains how small, consistent changes lead to remarkable results, with a practical system for building good habits.",
     True, False),
    ("wings-of-fire", "Wings of Fire: An Autobiography", "A.P.J. Abdul Kalam with Arun Tiwari", "non-fiction", 299, "#e07b39",
     "The autobiography of A.P.J. Abdul Kalam, India's missile scientist and former President, written with Arun Tiwari.",
     False, False),
    ("thinking-fast-and-slow", "Thinking, Fast and Slow", "Daniel Kahneman", "non-fiction", 549, "#3c6e91",
     "Nobel laureate Daniel Kahneman explores the two systems that drive how we think and make decisions.",
     False, True),

    ("a-brief-history-of-time", "A Brief History of Time", "Stephen Hawking", "education", 399, "#2d3a6b",
     "Stephen Hawking explains the Big Bang, black holes and the nature of time for general readers.",
     False, False),
    ("how-to-solve-it", "How to Solve It", "George Polya", "education", 599, "#5b7a4a",
     "George Polya's classic guide to mathematical problem solving, with a step-by-step method that applies far beyond maths.",
     False, True),

    ("clean-code", "Clean Code", "Robert C. Martin", "technology", 699, "#397b83",
     "Robert C. Martin's guide to writing readable, maintainable code, with practical examples and refactoring advice.",
     False, True),
    ("the-pragmatic-programmer", "The Pragmatic Programmer", "David Thomas and Andrew Hunt", "technology", 649, "#685b9b",
     "David Thomas and Andrew Hunt's practical advice on becoming a better, more effective software developer.",
     False, False),
    ("python-crash-course", "Python Crash Course", "Eric Matthes", "technology", 599, "#3b6ea5",
     "Eric Matthes teaches Python through a hands-on, project-based introduction suited to beginners.",
     True, False),
    ("automate-the-boring-stuff", "Automate the Boring Stuff with Python", "Al Sweigart", "technology", 549, "#4f8a5b",
     "Al Sweigart shows beginners how to use Python to automate everyday tasks such as working with files, spreadsheets and the web.",
     False, True),
]

COVER_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def attach_cover(book, file_stem):
    """If media/covers/<file_stem>.jpg (or png/webp) exists and the book has no cover, use it."""
    if book.cover_image:
        return False
    folder = Path(settings.MEDIA_ROOT) / "covers"
    for ext in COVER_EXTENSIONS:
        if (folder / f"{file_stem}{ext}").exists():
            book.cover_image = f"covers/{file_stem}{ext}"
            book.save(update_fields=["cover_image"])
            return True
    return False


class Command(BaseCommand):
    help = "Replace the sample books with 15 real books (safe to run more than once)."

    def handle(self, *args, **options):
        cats = {}
        for name, slug, icon in CATEGORIES:
            cats[slug], _ = Category.objects.get_or_create(
                slug=slug, defaults={"name": name, "icon": icon})

        # 1. Remove the old sample books.
        removed = 0
        for book in Book.objects.filter(title__in=OLD_SAMPLE_TITLES):
            try:
                book.delete()
                removed += 1
            except ProtectedError:
                self.stdout.write(self.style.WARNING(
                    f"Kept '{book.title}' because it is part of an order."))

        # 2. Add or update the real books.
        created = updated = covers = 0
        for stem, title, author, slug, price, color, desc, best, new in BOOKS:
            book = Book.objects.filter(title=title).first()
            if book:
                # Keep the price, featured flags, cover and saved AI summary.
                book.author = author
                book.category = cats[slug]
                book.description = desc
                book.save()
                updated += 1
            else:
                book = Book.objects.create(
                    title=title, author=author, category=cats[slug], price=price,
                    cover_color=color, description=desc,
                    is_bestseller=best, is_new_arrival=new,
                )
                created += 1
            if attach_cover(book, stem):
                covers += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Removed {removed} old, created {created}, updated {updated}, "
            f"attached {covers} cover(s)."))