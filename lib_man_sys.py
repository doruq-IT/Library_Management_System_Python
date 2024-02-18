import os

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Library:
    def __init__(self, filename='books.txt'):
        self.file = open(filename, 'a+', encoding='utf-8')
        self.filename = filename

    def __del__(self):
        self.file.close()

    def list_books(self):
        self.file.seek(0)
        books = self.file.read().splitlines()
        if not books:
            print(Colors.WARNING + "No books found in the library." + Colors.ENDC)
        else:
            print(Colors.OKBLUE + "Listing all books:" + Colors.ENDC)
            for book in books:
                name, author, _, _ = book.split(', ')
                print(f"{Colors.BOLD}Book Name:{Colors.ENDC} {name}, {Colors.BOLD}Author:{Colors.ENDC} {author}")

    def add_book(self):
        name = input("Book name: ")
        author = input("Author: ")
        release_date = input("Release date: ")  # Receive information from the user for publication date
        pages = input("Number of pages: ")  # Get information from the user for the number of pages
        
        # Check if a book with the same name is already in the library
        self.file.seek(0)
        books = self.file.read().splitlines()
        for book in books:
            book_name, _, _, _ = book.split(', ', 3)  # Only extract the book name
            if name.lower() == book_name.lower():  # Convert to lowercase for case-insensitive comparison
                print(Colors.WARNING + "A book with the same name already exists in the library." + Colors.ENDC)
                return  # If a book with the same name is found, exit the function

        # Ask for confirmation before adding the book
        confirmation = input("Are you sure you want to add this book to the library? (y/n): ").lower()
        if confirmation == 'y':
            # If confirmed, add the book to the file
            self.file.write(f"{name}, {author}, {release_date}, {pages}\n")
            self.file.flush()  # Ensure data is written to the file
            print(Colors.OKGREEN + "Book added successfully!" + Colors.ENDC)
        else:
            print(Colors.WARNING + "Book addition cancelled." + Colors.ENDC)

    def remove_book(self):
        title_to_remove = input("Title of the book to remove: ").lower()
        self.file.seek(0)
        books = self.file.read().splitlines()
        books_lower = [book.lower() for book in books]  # Kitapları küçük harfe çevir
        matched_books = [book for book in books_lower if title_to_remove in book]

        if matched_books:
            confirmation = input(f"Are you sure you want to remove '{title_to_remove}' (y/n)? ").lower()
            if confirmation == 'y':
                books = [book for book in books if book.lower() not in matched_books]
                with open(self.filename, 'w', encoding='utf-8') as f:
                    for book in books:
                        f.write(book + '\n')
                print(Colors.OKGREEN + "Book removed successfully!" + Colors.ENDC)
            else:
                print(Colors.WARNING + "Book removal cancelled." + Colors.ENDC)
        else:
            print(Colors.FAIL + "Book not found!" + Colors.ENDC)

    def search_books(self):
        search_query = input("Enter book name or author to search: ").lower()  # Convert user query to lowercase
        self.file.seek(0)
        books = self.file.read().splitlines()
        found_books = [book for book in books if search_query in book.lower()]  # Lowercase the data in the file and search
        if found_books:
            print(Colors.OKBLUE + "Books found:" + Colors.ENDC)
            for book in found_books:
                name, author, _, _ = book.split(', ')
                print(f"{Colors.BOLD}Book Name:{Colors.ENDC} {name}, {Colors.BOLD}Author:{Colors.ENDC} {author}")
        else:
            print(Colors.WARNING + "No books matched your search." + Colors.ENDC)

def main_menu(lib):
    while True:
        print("\n" + Colors.HEADER + "*** MENU ***" + Colors.ENDC)
        print("1) List Books\n2) Add Book\n3) Remove Book\n4) Search Books\nq) Exit")
        choice = input("Please choose an option (1-4, q): ")

        if choice == '1':
            lib.list_books()
        elif choice == '2':
            lib.add_book()
        elif choice == '3':
            lib.remove_book()
        elif choice == '4':
            lib.search_books()
        elif choice.lower() == 'q':
            print("Exiting the system...")
            break
        else:
            print(Colors.FAIL + "Invalid selection! Please enter a number between 1-4 or 'q'." + Colors.ENDC)

if __name__ == '__main__':
    lib = Library()
    main_menu(lib)
