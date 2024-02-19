import os
# ANSI escape sequences
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
        """
        Kütüphaneyi başlatır ve kitap listesi için bir dosya açar.

        Parametreler:
        filename (str): Kitapların saklanacağı dosyanın adı. Varsayılan değer 'books.txt'.
        """
        self.file = open(filename, 'a+', encoding='utf-8')
        self.filename = filename

    # Kütüphane nesnesi silindiğinde dosyanın kapatılmasını sağlamak için Destructor method kullanıyoruz.
    def __del__(self):
        self.file.close()

    def list_books(self):
        """
        Kütüphanedeki tüm kitapları listeler. Her kitabın adı ve yazarı ekrana yazdırılır.
        Eğer kütüphanede hiç kitap yoksa, bir uyarı mesajı gösterilir.
        """
        self.file.seek(0) # dosyanın baştan okunması için
        books = self.file.read().splitlines()
        if not books: 
            print(Colors.WARNING + "No books found in the library." + Colors.ENDC)
        else:
            print(Colors.OKBLUE + "Listing all books:" + Colors.ENDC)
            for book in books:
                name, author, _, _ = book.split(', ')
                print(f"{Colors.BOLD}Book Name:{Colors.ENDC} {name}, {Colors.BOLD}Author:{Colors.ENDC} {author}")

    def add_book(self):
        """
        Kullanıcıdan yeni bir kitap eklemek için gerekli bilgileri alır ve bu kitabı kütüphaneye ekler.
        Kullanıcıdan kitabın adı, yazarı, yayın tarihi ve sayfa sayısı istenir.
        Eğer aynı isimde bir kitap zaten mevcutsa, kullanıcıya uyarı verilir ve kitap eklenmez.
        Kullanıcı kitabı eklemek istediğini onaylarsa, kitap kütüphaneye eklenir.
        """
        name = input("Book name: ")
        author = input("Author: ")
        release_date = input("Release date: ")  # Kitabın yayın tarihi
        pages = input("Number of pages: ")  # Syfa sayısı
        
        # Kütüphanede aynı isimde bir kitap olup olmadığını kontrol amaçlı;
        self.file.seek(0)
        books = self.file.read().splitlines()
        for book in books:
            book_name, _, _, _ = book.split(', ', 3) 
            if name.lower() == book_name.lower():  # hepsini küçük harf yaparak standartlaştırma
                print(Colors.WARNING + "A book with the same name already exists in the library." + Colors.ENDC)
                return  # Aynı isimde bir kitap bulunursa, fonksiyondan çıkılır

        # Bir kitap eklemeden emin olup olmadığını sor
        confirmation = input("Are you sure you want to add this book to the library? (y/n): ").lower()
        if confirmation == 'y':
            # Onaylanırsa, kitabı dosyaya ekle
            self.file.write(f"{name}, {author}, {release_date}, {pages}\n")
            self.file.flush()  # Verilerin dosyaya yazıldığından emin ol
            print(Colors.OKGREEN + "Book added successfully!" + Colors.ENDC)
        else:
            print(Colors.WARNING + "Book addition cancelled." + Colors.ENDC)

    def remove_book(self):
        """
        Kullanıcıdan kaldırılacak kitabın adını ister ve bu adı kullanarak kütüphanedeki kitapları arar.
        Eğer eşleşen kitap bulunursa, kullanıcıdan kitabı kaldırmak için onay ister.
        Onay verilirse, eşleşen kitap kütüphaneden kaldırılır.
        Eğer eşleşen kitap bulunamazsa, kullanıcıya bir uyarı mesajı gösterilir.
        """
        title_to_remove = input("Title of the book to remove: ").lower()
        self.file.seek(0)
        books = self.file.read().splitlines()
        books_lower = [book.lower() for book in books]
        matched_books = [book for book in books_lower if title_to_remove in book]

        if matched_books: # eşleşen kitap kontrolü
            confirmation = input(f"Are you sure you want to remove '{title_to_remove}' (y/n)? ").lower()
            if confirmation == 'y': # onay?
                books = [book for book in books if book.lower() not in matched_books]
                with open(self.filename, 'w', encoding='utf-8') as f: # yazma modunda aç ve güncelle
                    for book in books:
                        f.write(book + '\n')
                print(Colors.OKGREEN + "Book removed successfully!" + Colors.ENDC)
            else:
                print(Colors.WARNING + "Book removal cancelled." + Colors.ENDC)
        else:
            print(Colors.FAIL + "Book not found!" + Colors.ENDC)

    def search_books(self):
        """
        Kullanıcıdan bir kitap adı veya yazar ismi istenir.
        Girilen sorgu ile eşleşen tüm kitaplar listelenir.
        Eğer eşleşen kitaplar bulunursa, her birinin adı ve yazarı ekrana yazdırılır.
        Eşleşen kitap bulunamazsa, kullanıcıya bir bilgi mesajı gösterilir.
        """
        search_query = input("Enter book name or author to search: ").lower()  # Sorguyu küçük harfe dönüştür.
        self.file.seek(0)
        books = self.file.read().splitlines()
        found_books = [book for book in books if search_query in book.lower()]  # Verileri küçük harfe çevirip ara
        if found_books:
            print(Colors.OKBLUE + "Books found:" + Colors.ENDC)
            for book in found_books:
                name, author, _, _ = book.split(', ')
                print(f"{Colors.BOLD}Book Name:{Colors.ENDC} {name}, {Colors.BOLD}Author:{Colors.ENDC} {author}")
        else:
            print(Colors.WARNING + "No books matched your search." + Colors.ENDC)

def main_menu(lib):
    """
    Kullanıcıya bir ana menü sunar ve kullanıcıdan seçim yapmasını ister.
    Kullanıcı listeleme, kitap ekleme, kitap kaldırma, kitap arama ve çıkış işlemlerinden birini seçebilir.
    Kullanıcının seçimine bağlı olarak ilgili işlem gerçekleştirilir.

    Parametreler:
    lib (Library): Kütüphane sınıfının bir örneği
    """
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
