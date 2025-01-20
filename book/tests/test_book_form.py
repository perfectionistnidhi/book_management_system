import pytest
from book.forms import BookForm
from book.models import Genre

@pytest.mark.django_db
def test_book_form_valid():
    genre = Genre.objects.create(name="Fiction")
    form_data = {
        'title': 'Valid Book',
        'genre': genre.id,
        'price': 19.99,
        'description': 'A valid book description',
        'image': None
    }
    form = BookForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_book_form_invalid():
    genre = Genre.objects.create(name="Fiction")
    form_data = {
        'title': '',  # Missing title
        'genre': genre.id,
        'price': 19.99,
        'description': 'Invalid book description',
        'image': None
    }
    form = BookForm(data=form_data)
    assert not form.is_valid()
    assert 'This field is required.' in form.errors['title']
