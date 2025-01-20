import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from book.models import Genre, Book


@pytest.mark.django_db
def test_scrape_book_view_access(client):
    # Create users
    admin_user = get_user_model().objects.create_user(username='admin', password='password', role='admin')
    regular_user = get_user_model().objects.create_user(username='user', password='password', role='user')

    # Create genre
    genre = Genre.objects.create(name="Fiction")

    # Test admin access
    client.login(username='admin', password='password')
    response = client.get(reverse('scrape_books'))
    assert response.status_code == 200

    # Test non-admin access
    client.login(username='user', password='password')
    response = client.get(reverse('scrape_books'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_book_view(client):
    # Create admin user and genre
    admin_user = get_user_model().objects.create_user(username='admin', password='password', role='admin')
    genre = Genre.objects.create(name="Fiction")

    client.login(username='admin', password='password')

    # Create book data
    book_data = {
        'title': 'New Book',
        'genre': genre.id,
        'price': 19.99,
        'description': 'A great book!',
        'image': None
    }

    response = client.post(reverse('add_book'), book_data)
    assert response.status_code == 302  # Redirect to 'manage_books'
    assert Book.objects.count() == 1
    assert Book.objects.first().title == 'New Book'


@pytest.mark.django_db
def test_manage_books_view(client):
    # Create admin user, genre and book
    admin_user = get_user_model().objects.create_user(username='admin', password='password', role='admin')
    genre = Genre.objects.create(name="Fiction")
    book = Book.objects.create(
        title="Test Book", genre=genre, price=9.99, description="Test description"
    )

    client.login(username='admin', password='password')
    response = client.get(reverse('manage_books'))
    assert response.status_code == 200
    assert "Test Book" in response.content.decode()


@pytest.mark.django_db
def test_remove_book_view(client):
    # Create admin user, genre, and book
    admin_user = get_user_model().objects.create_user(username='admin', password='password', role='admin')
    genre = Genre.objects.create(name="Fiction")
    book = Book.objects.create(
        title="Test Book", genre=genre, price=9.99, description="Test description"
    )

    client.login(username='admin', password='password')
    response = client.post(reverse('remove_book', args=[book.id]))
    assert response.status_code == 302  # Redirect to 'manage_books'
    assert Book.objects.count() == 0
