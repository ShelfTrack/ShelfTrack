from PyQt6.QtWidgets import (
    QWidget, QTableWidgetItem, QMessageBox,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from services.api_service import APIService

class BookManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.api_service = APIService()
        self.current_page = 1
        self.books_per_page = 10
        self.load_books()
        
    def init_ui(self):
        # Load the UI file
        loadUi('frontend/ui/book_management.ui', self)
        
        # Connect signals
        self.searchButton.clicked.connect(self.search_books)
        self.addBookButton.clicked.connect(self.show_add_book_dialog)
        self.prevButton.clicked.connect(self.previous_page)
        self.nextButton.clicked.connect(self.next_page)
        self.searchInput.returnPressed.connect(self.search_books)
        
        # Setup table
        self.booksTable.setColumnCount(7)
        self.booksTable.setHorizontalHeaderLabels([
            'Title', 'Author', 'ISBN', 'Type', 'Quantity',
            'Available', 'Actions'
        ])
        
    def load_books(self, search_query=None):
        """Load books from the API with pagination"""
        try:
            # Get books from API
            response = self.api_service.get_books(
                page=self.current_page,
                per_page=self.books_per_page,
                search=search_query
            )
            
            books = response.get('results', [])
            total_books = response.get('count', 0)
            total_pages = (total_books + self.books_per_page - 1) // self.books_per_page
            
            # Update table
            self.booksTable.setRowCount(len(books))
            for row, book in enumerate(books):
                self.add_book_to_table(row, book)
            
            # Update pagination
            self.totalLabel.setText(f"Total: {total_books} books")
            self.pageLabel.setText(f"Page {self.current_page} of {total_pages}")
            self.prevButton.setEnabled(self.current_page > 1)
            self.nextButton.setEnabled(self.current_page < total_pages)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load books: {str(e)}")
    
    def add_book_to_table(self, row, book):
        """Add a book to the table at the specified row"""
        # Add book details
        self.booksTable.setItem(row, 0, QTableWidgetItem(book['title']))
        self.booksTable.setItem(row, 1, QTableWidgetItem(book['author']))
        self.booksTable.setItem(row, 2, QTableWidgetItem(book['isbn']))
        self.booksTable.setItem(row, 3, QTableWidgetItem(book['book_type']))
        self.booksTable.setItem(row, 4, QTableWidgetItem(str(book['quantity'])))
        self.booksTable.setItem(row, 5, QTableWidgetItem(str(book['available_quantity'])))
        
        # Add action buttons
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(lambda: self.edit_book(book['id']))
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.delete_book(book['id']))
        
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        self.booksTable.setCellWidget(row, 6, actions_widget)
    
    def search_books(self):
        """Search books based on input text"""
        self.current_page = 1
        self.load_books(search_query=self.searchInput.text())
    
    def show_add_book_dialog(self):
        """Show dialog to add a new book"""
        # TODO: Implement add book dialog
        pass
    
    def edit_book(self, book_id):
        """Show dialog to edit a book"""
        # TODO: Implement edit book dialog
        pass
    
    def delete_book(self, book_id):
        """Delete a book after confirmation"""
        reply = QMessageBox.question(
            self, 'Delete Book',
            'Are you sure you want to delete this book?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.api_service.delete_book(book_id)
                self.load_books()
                QMessageBox.information(self, "Success", "Book deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete book: {str(e)}")
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_books(search_query=self.searchInput.text())
    
    def next_page(self):
        """Go to next page"""
        self.current_page += 1
        self.load_books(search_query=self.searchInput.text())
