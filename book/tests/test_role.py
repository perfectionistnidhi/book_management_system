import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_role_required_decorator():
    user = get_user_model().objects.create_user(username='testuser', password='password', role='user')

    client.login(username='testuser', password='password')
    response = client.get(reverse('scrape_books'))
    assert response.status_code == 403  # Unauthorized
