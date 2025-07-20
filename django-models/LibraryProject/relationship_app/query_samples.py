from relationship_app.models import Author, Book, Library, Librarian


author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
print(f"Books by {author.name}: {[book.title for book in books_by_author]}")
books_by_author = author.books.all()  
print(f"Books by {author.name}: {[book.title for book in books_by_author]}")

library = Library.objects.get(name=library_name)
library_books = library.books.all()
print(f"Books in {library.name}: {[book.title for book in library_books]}")

librarian = library.librarian  
print(f"Librarian at {library.name}: {librarian.name}")
librarian = Librarian.objects.get(library=library)
print(f"Librarian at {library.name}: {librarian.name}")
