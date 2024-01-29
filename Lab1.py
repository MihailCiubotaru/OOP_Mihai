class Book:
    def init(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display_info(self):
        print(f"Title: {self.title}\nAuthor: {self.author}\nISBN: {self.isbn}\n")


class Library:
    def init(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):
        for book in self.books:
            book.display_info()


def main():
    # Input the number of books
    num_ofbooks = int(input("Enter the number of books: "))
    library = Library()

    # Input data for each book
    for  in range(num_of_books):
        title = input("Enter the title: ")
        author = input("Enter the author: ")
        isbn = input("Enter the ISBN: ")

        new_book = Book(title, author, isbn)
        library.add_book(new_book)

    # Output to the console
    library.display_books()


if name == "main":
    main()
