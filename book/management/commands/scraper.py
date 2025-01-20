from django.core.management.base import BaseCommand
from book.utils import scrape_genres, scrape_books
from book.models import Genre

class Command(BaseCommand):
    help = 'Scrape genres and books from the website'

    def handle(self, *args, **kwargs):
        # Step 1: Scrape and populate genres
        self.stdout.write("Scraping genres...\n")
        scrape_genres()

        # Step 2: Scrape books for each genre
        self.stdout.write("Scraping books...\n")
        genres = Genre.objects.all()
        for genre in genres:
            self.stdout.write(f"Scraping books for genre: {genre.name}\n")
            scrape_books(genre.name)

        self.stdout.write(self.style.SUCCESS('Scraping process completed successfully!'))
