# book/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # URL for listing books
    path('scrape/', views.scrape_book_view, name='scrape_books'),  # URL for scraping books
    path('manage/', views.manage_books, name='manage_books'),  # URL for managing books
    path('add/', views.add_book, name='add_book'),  # URL for adding a book
    path('remove/<int:book_id>/', views.remove_book, name='remove_book'),  # URL for removing a book
    path('update/<int:book_id>/', views.update_book, name='update_book'),  # URL for updating a book
    path('test_redirect/', views.test_redirect, name='test_redirect'),

]
