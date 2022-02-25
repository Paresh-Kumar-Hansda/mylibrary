from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('newbook/',views.newbook, name='newbook'),
    path('register/',views.register, name='register'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('borrowers/', views.BorrowerListView.as_view(), name='borrowers'),
    path('borrower/<int:pk>', views.BorrowerDetailView.as_view(), name='borrower-detail'),
    path('librarians/', views.LibrarianListView.as_view(), name='librarians'),
    path('librarian/<int:pk>', views.LibrarianDetailView.as_view(), name='librarian-detail'),

    #authors url
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    #path('book/<int:pk>', views.book_detail_view, name='book-detail'),
    #author detail
    path('author/<int:pk>',views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('loaned/', views.LoanedBooksListView.as_view(), name='all-borrowed'),
]

urlpatterns += [
    path('myloanedbooks/', views.LoanedBooksByLibrarianListView.as_view(), name='my-loaned'),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
