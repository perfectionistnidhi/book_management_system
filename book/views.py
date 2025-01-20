from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Book, Genre
from .utils import scrape_books
from .forms import BookForm


from django.http import HttpResponse

@login_required
def test_redirect(request):
    return redirect('manage_books')

def role_required(roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Fetching the user's role from the `CustomUser` model
            user_role = getattr(request.user, 'role', None)
            if user_role not in roles:
                return HttpResponse('Unauthorized access', status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



@login_required
@role_required(['admin', 'superadmin'])
def scrape_book_view(request):
    print(f"Logged in user: {request.user.username}, Role: {request.user.role}")
    genres = Genre.objects.all()
    if request.method == 'POST':
        category = request.POST.get('category')
        if not Genre.objects.filter(name=category).exists():
            messages.error(request, 'Invalid category selected!')
            return redirect('scrape_books')

        try:
            scrape_books(category)
            messages.success(request, f"Books for {category} scraped successfully.")
        except Exception as e:
            messages.error(request, f"Error scraping books for {category}: {e}")

        return redirect('book_list')

    return render (request, 'book/scrape_books.html', {'genres': genres})


def book_list(request):
    books = Book.objects.all()
    categories = Genre.objects.all()
    print(f"Books: {books.count()}")
    print(f"categories: {categories.count()}")
    selected_category = request.GET.get('category')
    if selected_category:
        books = books.filter(genre__name__iexact=selected_category)
    else:
        books = []

    return render(request, 'book/book_list.html', {'books': books, 'categories': categories, 'selected_category': selected_category, })


@login_required
@role_required(['admin', 'superadmin'])
def manage_books(request):
    books = Book.objects.all()
    return render(request, 'book/manage_books.html', {'books': books})

@login_required
@role_required(['admin', 'superadmin'])
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # Ensure you handle file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('manage_books')
    else:
        form = BookForm()

    return render(request, 'book/add_book.html', {'form': form})


@login_required
@role_required(['superadmin'])
def remove_book(request, book_id):
    # Get the book object or return a 404 error if not found
    book = get_object_or_404(Book, id=book_id)

    # If it's a POST request, delete the book
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('manage_books')

    # If it's a GET request, show the confirmation page
    return render(request, 'book/remove_book.html', {'book': book})



@login_required
@role_required(['admin', 'superadmin'])
def update_book(request, book_id):
    # Get the book object or return a 404 error if not found
    book = get_object_or_404(Book, id=book_id)
    genres = Genre.objects.all()  # Fetch all genres for the dropdown

    if request.method == 'POST':
        # Bind the POST data to the form
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('/book/manage/')  # Redirect to the manage books page
        else:
            messages.error(request, 'There was an error updating the book. Please try again.')
    else:
        form = BookForm(instance=book)

    # Pass the form and genres to the template
    return render(request, 'book/update_book.html', {
        'form': form,
        'book': book,
        'genres': genres,  # Pass genres to the template
    })
