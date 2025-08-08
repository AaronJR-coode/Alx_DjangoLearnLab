from rest_framework import serializers
from datetime import date
from .models import Author, Book


# BookSerializer serializes all fields of the Book model.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        mode = Book
        fields = "__all__"

# Includes custom validation to ensure publication_year is not in the future.
    def validate_publication_year(self, value):
        curent_yrs = date.today().year
        if value > curent_yrs:
            raise serializers.ValidationError("Wrong publication year!")
        return value
# AuthorSerializer serializes the name field and includes a nested list of books.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

# Uses BookSerializer to dynamically serialize related Book instances.
    class Meta:
        model = Author
        fields = ['name', 'books']