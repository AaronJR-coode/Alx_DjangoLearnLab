from django.urls import path
from .views import list_books

urlpatterns = [
    path('books/', views.book_list_view, name='book-list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
]
