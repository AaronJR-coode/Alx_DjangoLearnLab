import django_filter
from .models import Book

class BookFilter(django_filter.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'author': ['icontains'],
            'publication_year': ['exact', 'gte', 'lte']
        }