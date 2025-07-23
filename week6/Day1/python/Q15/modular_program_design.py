# Library inventory is stored as a list of dictionaries
library = []

def add_book():
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    year = input("Enter publication year: ").strip()
    
    book = {"title": title, "author": author, "year": year}
    library.append(book)
    print(f"✅ Book '{title}' added successfully.\n")

def search_book():
    search_title = input("Enter title to search: ").strip().lower()
    found_books = [book for book in library if search_title in book["title"].lower()]

    if found_books:
        print("🔍 Search Results:")
        for idx, book in enumerate(found_books, 1):
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']})")
    else:
        print("❌ No books found with that title.")
    print()

def list_inventory():
    if not library:
        print("📚 Inventory is empty.\n")
        return

    print("📚 Library Inventory:")
    for idx, book in enumerate(library, 1):
        print(f"{idx}. {book['title']} by {book['author']} ({book['year']})")
    print()

def main():
    while True:
        print("===== Library Menu =====")
        print("1. Add Book")
        print("2. Search Book")
        print("3. List Inventory")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            add_book()
        elif choice == '2':
            search_book()
        elif choice == '3':
            list_inventory()
        elif choice == '4':
            print("👋 Exiting Library System. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please select 1–4.\n")

# Run the program
main()
