from relationship_app.models import Author, Book, Library, Librarian


author = Author.objects.get(name="Aaron")
books_by_author = author.books.all()  
print(f"Books by {author.name}: {[book.title for book in books_by_author]}")

library = Library.objects.get(name="National Library")
library_books = library.books.all()
print(f"Books in {library.name}: {[book.title for book in library_books]}")

librarian = library.librarian  
print(f"Librarian at {library.name}: {librarian.name}")
