import requests
from bs4 import BeautifulSoup
from .models import Book, Genre

def scrape_genres():
    """Scrape genres from the website and store them in the Genre model."""
    try:
        url = "https://books.toscrape.com/index.html"
        response = requests.get(url)

        if response.status_code != 200:
            print("Failed to access the website. Please check the URL.")
            return

        content = response.content
        print(response.content)
        soup = BeautifulSoup(content, 'html.parser')

        # Locate the genres section in the sidebar
        genre_links = soup.select("div.side_categories ul li ul li a")
        print(f"Found genres: {len(genre_links)}")

        for genre_link in genre_links:
            genre_name = genre_link.text.strip()
            genre_slug = genre_link['href'].split('/')[-2]  # Extract slug from the link

            # Add the genre to the database
            genre, created = Genre.objects.get_or_create(name=genre_name)
            if created:
                print(f"Added genre: {genre_name}")
            else:
                print(f"Genre already exists: {genre_name}")

    except Exception as e:
        print(f"Error while scraping genres: {e}")

def scrape_books(genre_name):
    """Scrape books for a specific genre and store them in the Book model."""
    try:
        # Get the genre object from the database
        genre = Genre.objects.get(name=genre_name)

        # Calculate the start page based on the genre's ID
        # Add 1 to the genre's ID to get the correct page number
        start_page = genre.id + 1  # Adjust the page number by adding 1
        genre_slug = genre_name.lower().replace(' ', '-')
        print(f"Starting to scrape books for genre: {genre_name} from page {start_page}")

        page = start_page  # Start scraping from the calculated start page

        while True:
            url = f"https://books.toscrape.com/catalogue/category/books/{genre_slug}_{page}/index.html"
            response = requests.get(url)
            print(f"Requesting: {url}")
            print(f"Response code: {response.status_code}")

            # If the response is not 200, stop scraping (page does not exist)
            if response.status_code != 200:
                print(f"No more pages to scrape for {genre_name}. Stopping scrape.")
                break

            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            books = soup.find_all("article", class_="product_pod")

            if not books:  # If no books are found on the page, stop scraping
                print(f"No books found for page {page}. Stopping scrape.")
                break

            # Process each book found on the page
            for book in books:
                try:
                    image = book.find('img')['src']
                    title = book.find('img')['alt']
                    price_raw = book.find("p", class_="price_color").text
                    price = float(price_raw.replace('£', ''))
                    description = "Sample description"  # Placeholder for description

                    print(f"Scraping book: {title}, Price: {price}")

                    # Store the book in the database
                    book_obj, created = Book.objects.get_or_create(
                        title=title,
                        genre=genre,
                        price=price,
                        description=description,
                        image=image,
                    )

                    if created:
                        print(f"Added book: {title}")
                    else:
                        print(f"Book already exists: {title}")

                except Exception as e:
                    print(f"Error while processing a book: {e}")

            print(f"Successfully scraped page {page} for genre: {genre_name}")
            page += 1  # Move to the next page

    except Genre.DoesNotExist:
        print(f"Genre {genre_name} not found in the database.")
    except Exception as e:
        print(f"Error while scraping books for {genre_name}: {e}")