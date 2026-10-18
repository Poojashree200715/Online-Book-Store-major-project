from django.core.management.base import BaseCommand

from store.models import Book, Category

CATEGORIES = [
    ("Fiction", "fiction", "✨"),
    ("Education", "education", "🎓"),
    ("Technology", "technology", "💻"),
]

# old site title (used to find an existing row), real title, author, category slug,
# price, placeholder colour, description, bestseller, new arrival
BOOKS = [
    ("Data Science Basics", "Data Science for Beginners",
     "Samir Dey, Dibyendu Banerjee, Sourav Kairi", "technology", 449, "#685b9b",
     "A beginner-friendly introduction to data science, covering core concepts, data analysis and visualization.",
     False, True),
    ("Ocean of Dreams", "Ocean of Dreams",
     "Dr. M.S. Shabeer", "fiction", 259, "#39718a",
     "A novel by Dr. M.S. Shabeer.",
     False, True),
    ("The Power of Focus", "The Power of Focus",
     "Jack Canfield, Mark Victor Hansen, Les Hewitt", "education", 325, "#987b42",
     "How to hit your business, personal and financial targets with absolute certainty.",
     False, False),
    ("Python Made Simple", "Python Made Easy",
     "Nilabh Nishchhal", "technology", 399, "#397b83",
     "A step-by-step guide to programming and data analysis using Python, for beginner and intermediate levels.",
     True, False),
    ("Midnight Stories", "Midnight Stories",
     "Su Tong", "fiction", 279, "#754e62",
     "Fiction by the Chinese author Su Tong.",
     False, False),
    ("Future of AI", "The Future of AI",
     "Mohd Anas Arshad, Nidhi, Ashwini Thantri", "technology", 499, "#626c91",
     "Navigating the opportunities and challenges of artificial intelligence.",
     True, True),
    ("Learning Every Day", "Learn Something New Every Day",
     "Kee Malesky", "education", 349, "#bd8050",
     "365 facts to fulfill your life, from an NPR librarian.",
     False, True),
    ("The Silent Garden", "The Silent Gardener",
     "Michael Di Lancar", "fiction", 299, "#426957",
     "A dark, atmospheric fantasy story.",
     True, False),
]


class Command(BaseCommand):
    help = "Load or update sample categories and books (safe to run more than once)."

    def handle(self, *args, **options):
        cats = {}
        for name, slug, icon in CATEGORIES:
            cats[slug], _ = Category.objects.get_or_create(
                slug=slug, defaults={"name": name, "icon": icon})

        created_count = updated_count = 0
        for old_title, title, author, slug, price, color, desc, best, new in BOOKS:
            # Find the book under its old OR new title so reruns never duplicate it.
            book = Book.objects.filter(title__in=[old_title, title]).first()
            if book:
                # Update text fields only; keep the cover image, price and featured flags.
                book.title = title
                book.author = author
                book.category = cats[slug]
                book.description = desc
                book.save()
                updated_count += 1
            else:
                Book.objects.create(
                    title=title, author=author, category=cats[slug], price=price,
                    cover_color=color, description=desc,
                    is_bestseller=best, is_new_arrival=new,
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. {created_count} created, {updated_count} updated."))