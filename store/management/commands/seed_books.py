from django.core.management.base import BaseCommand

from store.models import Book, Category

CATEGORIES = [
    ("Fiction", "fiction", "✨"),
    ("Education", "education", "🎓"),
    ("Technology", "technology", "💻"),
]

# title, author, category slug, price, colour, description, bestseller, new
BOOKS = [
    ("The Silent Garden", "A. Morgan", "fiction", 299, "#426957",
     "A moving story about family, hope and the unexpected paths that lead us home.", True, False),
    ("Learning Every Day", "R. Sharma", "education", 349, "#bd8050",
     "A practical guide to building better learning habits and lifelong curiosity.", False, True),
    ("Future of AI", "K. Williams", "technology", 499, "#626c91",
     "An introduction to artificial intelligence, machine learning and emerging technology.", True, True),
    ("Midnight Stories", "J. Parker", "fiction", 279, "#754e62",
     "A collection of intriguing short stories filled with mystery and imagination.", False, False),
    ("Python Made Simple", "S. Kumar", "technology", 399, "#397b83",
     "Learn programming concepts through clear explanations and beginner-friendly examples.", True, False),
    ("The Power of Focus", "M. Davis", "education", 325, "#987b42",
     "Explore simple strategies for improving focus, planning and personal productivity.", False, False),
    ("Ocean of Dreams", "L. James", "fiction", 259, "#39718a",
     "An adventurous tale of courage, friendship and discovery across the sea.", False, True),
    ("Data Science Basics", "P. Raj", "technology", 449, "#685b9b",
     "Discover data analysis, visualization and core data science concepts.", False, True),
]


class Command(BaseCommand):
    help = "Load sample categories and books."

    def handle(self, *args, **options):
        cats = {}
        for name, slug, icon in CATEGORIES:
            cats[slug], _ = Category.objects.get_or_create(
                slug=slug, defaults={"name": name, "icon": icon})

        added = 0
        for title, author, slug, price, color, desc, best, new in BOOKS:
            _, created = Book.objects.get_or_create(
                title=title,
                defaults={
                    "author": author, "category": cats[slug], "price": price,
                    "cover_color": color, "description": desc,
                    "is_bestseller": best, "is_new_arrival": new,
                },
            )
            added += created
        self.stdout.write(self.style.SUCCESS(f"Done. {added} new book(s) added."))
