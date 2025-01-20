# book/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from book.models import Genre, Book
from django.db import IntegrityError

@pytest.mark.django_db
def test_create_genre():
    genre = Genre.objects.create(name="Fiction")
    assert genre.name == "Fiction"
    assert Genre.objects.count() == 1

@pytest.mark.django_db
def test_create_duplicate_genre():
    Genre.objects.create(name="Fiction")
    with pytest.raises(IntegrityError):  # Ensuring uniqueness constraint
        Genre.objects.create(name="Fiction")

@pytest.mark.django_db
def test_book_str_method(book):
    # Assuming the book fixture is defined elsewhere in the test setup
    assert book.__str__() == "Test Book"  # Book title should match its string representation

@pytest.mark.django_db
def test_book_creation(book, genre):
    assert book.title == "Test Book"
    assert book.genre == genre
    assert book.price == 9.99
    assert book.description == "Test description"
    assert Book.objects.count() == 1

@pytest.mark.django_db
def test_book_image_field(book):
    # Assuming your image field is set up properly, we would test if the image can be accessed
    book.image = "book_images/test_image.jpg"
    book.save()
    assert book.image.url == "/media/book_images/test_image.jpg"

@pytest.mark.django_db
def test_invalid_book_price(book):
    book.price = -5  # Negative price should be invalid
    with pytest.raises(ValidationError):
        book.full_clean()  # This will trigger model validation
