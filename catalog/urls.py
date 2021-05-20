from django.urls import path
from . import views

urlpatterns = [
    # Function path defines:
    #     1. URL pattern: empty string
    #     2. View function thatll be called if the URL pattern is detected
    #     3. Name: unique identifier for this URL mapping
    path('', views.index, name='index'),
    

    # URLS for Books
    # URL for view implemented as a class
    path('books/', views.BookListView.as_view(), name='books'),

    #URL Map for book detail pages
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

    # URLS for Authors
    # URL for view implemented as a class
    path('authors/', views.AuthorListView.as_view(), name='authors'),

    #URL Map for author detail pages
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

#Part8 - path pointing to "on loan" view
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]