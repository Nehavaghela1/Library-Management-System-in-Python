import json
from datetime import datetime, timedelta


class User:
    def __init__(self):
        self.users = {}  # Store username: password

    def register(self, username, password):
        """Register a new user."""
        if username in self.users:
            print("Username already exists. Please choose another.")
        else:
            self.users[username] = password
            print("Registration successful!")

    def login(self, username, password):
        """Authenticate a user."""
        if username in self.users and self.users[username] == password:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password.")
            return False


class Library:
    FINE_PER_DAY = 5  # Fine amount in ₹ per day
    LOAN_PERIOD_DAYS = 30  # Loan period in days

    def __init__(self, list_of_books):
        self.books = list_of_books  # List of available books
        self.borrowed_books = {}  # Borrowed books with borrowers
        self.due_dates = {}  # Due dates for borrowed books
        self.borrow_history = {}  # Count of how often each book has been borrowed

    def display_available_books(self):
        """Display all available books in the library."""
        print("\nBooks available in the library:")
        if not self.books:
            print("No books available.")
        for book in self.books:
            print(f" * {book}")

    def borrow_book(self, book_name, borrower_name):
        """Borrow a book from the library."""
        book_name_lower = book_name.lower()
        available_books_lower = [book.lower() for book in self.books]
        borrowed_books_lower = [book.lower() for book in self.borrowed_books]

        if book_name_lower in available_books_lower:
            actual_book_name = self.books[available_books_lower.index(book_name_lower)]
            due_date = datetime.now() + timedelta(days=self.LOAN_PERIOD_DAYS)
            self.books.remove(actual_book_name)
            self.borrowed_books[actual_book_name] = borrower_name
            self.due_dates[actual_book_name] = due_date
            self.borrow_history[actual_book_name] = self.borrow_history.get(actual_book_name, 0) + 1
            print(f"\nYou have borrowed '{actual_book_name}'. Please return it by {due_date.strftime('%d-%m-%Y')}.")
        elif book_name_lower in borrowed_books_lower:
            print(f"\nSorry, '{book_name}' is already borrowed.")
        else:
            print("\nSorry, this book is not available in the library.")

    def return_book(self, book_name):
        """Return a borrowed book to the library."""
        book_name_lower = book_name.lower()
        borrowed_books_lower = [book.lower() for book in self.borrowed_books]

        if book_name_lower in borrowed_books_lower:
            actual_book_name = list(self.borrowed_books.keys())[borrowed_books_lower.index(book_name_lower)]
            borrower = self.borrowed_books.pop(actual_book_name)
            due_date = self.due_dates.pop(actual_book_name)
            days_late = (datetime.now() - due_date).days
            fine = max(0, days_late * self.FINE_PER_DAY)  
            self.books.append(actual_book_name)
            print(f"\nThank you, {borrower}, for returning '{actual_book_name}'.")
            if days_late > 0:
                print(f"You returned it {days_late} days late. Fine: ₹{fine}.")
        else:
            print("\nThis book is not registered as borrowed.")

    def add_book(self, book_name):
        """Add a new book to the library."""
        if book_name.lower() in [book.lower() for book in self.books + list(self.borrowed_books.keys())]:
            print(f"\n'{book_name}' is already in the library.")
        else:
            self.books.append(book_name)
            print(f"\n'{book_name}' has been added to the library.")

    def search_book(self, keyword):
        """Search for books by a keyword."""
        matching_books = [book for book in self.books if keyword.lower() in book.lower()]
        print("\nSearch results:")
        if matching_books:
            for book in matching_books:
                print(f" * {book}")
        else:
            print("No books found.")

    def recommend_books(self):
        """Display the most popular books based on borrow history."""
        print("\nMost popular books:")
        if not self.borrow_history:
            print("No books have been borrowed yet.")
        else:
            popular_books = sorted(self.borrow_history.items(), key=lambda x: x[1], reverse=True)
            for book, count in popular_books[:5]:  
                print(f" * {book} (borrowed {count} times)")

    def display_borrowed_books(self):
        """Display all currently borrowed books."""
        print("\nBorrowed books:")
        if not self.borrowed_books:
            print("No books are currently borrowed.")
        else:
            for book, borrower in self.borrowed_books.items():
                print(f" * '{book}' borrowed by {borrower}")

    def save_data(self):
        """Save library data to a JSON file."""
        data = {
            "books": self.books,
            "borrowed_books": self.borrowed_books,
            "due_dates": {k: v.strftime("%Y-%m-%d") for k, v in self.due_dates.items()},
            "borrow_history": self.borrow_history,
        }
        with open("library_data.json", "w") as file:
            json.dump(data, file)
        print("\nLibrary data has been saved.")

    def load_data(self):
        """Load library data from a JSON file."""
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)
                self.books = data["books"]
                self.borrowed_books = data["borrowed_books"]
                self.due_dates = {k: datetime.strptime(v, "%Y-%m-%d") for k, v in data["due_dates"].items()}
                self.borrow_history = data["borrow_history"]
            print("\nLibrary data has been loaded.")
        except FileNotFoundError:
            print("\nNo saved data found. Starting with default settings.")


def display_menu():
    """Display the library menu."""
    print('''\n=== Central Library Menu ===
1. Display all books
2. Borrow a book
3. Return a book
4. Add a new book
5. Search for a book
6. Recommend popular books
7. Display borrowed books
8. Save & Exit''')


def main():
    user_manager = User()
    library = Library(["Python Basics", "Django Essentials", "JavaScript Guide", "C++ Advanced", "Algorithms 101"])
    library.load_data()

    while True:
        print("\n=== Welcome to the Central Library ===")
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            user_manager.register(username, password)
        elif choice == "2":
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            if user_manager.login(username, password):
                break  
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            library.display_available_books()
        elif choice == "2":
            book_name = input("Enter the name of the book to borrow: ").strip()
            library.borrow_book(book_name, username)
        elif choice == "3":
            book_name = input("Enter the name of the book to return: ").strip()
            library.return_book(book_name)
        elif choice == "4":
            book_name = input("Enter the name of the book to add: ").strip()
            library.add_book(book_name)
        elif choice == "5":
            keyword = input("Enter a keyword to search for books: ").strip()
            library.search_book(keyword)
        elif choice == "6":
            library.recommend_books()
        elif choice == "7":
            library.display_borrowed_books()
        elif choice == "8":
            library.save_data()
            print("\nThank you for visiting the Central Library!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
