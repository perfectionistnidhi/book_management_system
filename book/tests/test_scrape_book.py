import pytest
from book.utils import scrape_books
from book.models import Genre, Book


@pytest.mark.django_db
def test_scrape_books():
    genre = Genre.objects.create(name="Fiction")

    # Mock the requests.get and BeautifulSoup behavior here
    with pytest.mock.patch('book.utils.requests.get') as mock_get, \
            pytest.mock.patch('book.utils.BeautifulSoup') as mock_soup:
        # Define mock responses
        mock_get.return_value.status_code = 200
        mock_soup.return_value.find_all.return_value = [
            {'title': 'Test Book', 'price': 9.99, 'description': 'Test description', 'image': 'test_image.jpg'}
        ]

        scrape_books("Fiction")

        # Check if book was added
        book = Book.objects.first()
        assert book.title == 'Test Book'
        assert book.price == 9.99
        assert book.genre.name == "Fiction"
