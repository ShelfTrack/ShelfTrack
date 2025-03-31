from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                               QComboBox, QFormLayout, QDialog, QMessageBox,
                               QHeaderView)
from PySide6.QtCore import Qt
import requests
from .add_book_dialog import AddBookDialog
from .login_dialog import LoginDialog

class BooksView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title and Add Book button row
        header_layout = QHBoxLayout()
        
        # Title
        title = QLabel("Books Management")
        title.setStyleSheet("""
            QLabel {
                color: #1a237e;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(title)
        
        # Add Book button
        add_btn = QPushButton("Add New Book")
        add_btn.setFixedWidth(150)  # Set fixed width
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a237e;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #283593;
            }
        """)
        add_btn.clicked.connect(self.show_add_dialog)
        header_layout.addWidget(add_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(header_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setSpacing(12)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search books...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
            }
            QLineEdit::placeholder {
                color: #757575;
            }
        """)
        
        search_btn = QPushButton("Search")
        search_btn.setFixedWidth(100)  # Set fixed width
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a237e;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #283593;
            }
        """)
        search_btn.clicked.connect(self.search_books)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addStretch()
        
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 8px;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
                color: #333333;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #666666;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1a237e;
            }
        """)
        
        # Set up columns
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Title", "Author", "ISBN", "Publisher", "Status", "Quantity", "Actions"
        ])
        
        # Set column widths
        self.table.setColumnWidth(0, 250)  # Title
        self.table.setColumnWidth(1, 200)  # Author
        self.table.setColumnWidth(2, 120)  # ISBN
        self.table.setColumnWidth(3, 200)  # Publisher
        self.table.setColumnWidth(4, 100)  # Status
        self.table.setColumnWidth(5, 80)   # Quantity
        self.table.setColumnWidth(6, 150)  # Actions
        
        # Table styling
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        
        # Set header alignment
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            if i in [4, 5, 6]:  # Status, Quantity, and Actions columns
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
        
        layout.addWidget(self.table)
        
        # Load initial data
        self.load_books()
        
        # Style for the view
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #1a237e;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #283593;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
            }
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 8px;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
                color: #333333;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #666666;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1a237e;
            }
        """)
        
    def load_books(self):
        """Load books from the API and display them in the table."""
        try:
            headers = {}
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
                
            response = requests.get('http://127.0.0.1:8000/api/books/', headers=headers)
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Handle both list response and paginated response
                    books = data['results'] if isinstance(data, dict) and 'results' in data else data
                    
                    self.table.setRowCount(0)  # Clear existing rows
                    for book in books:
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        self.add_book_to_table(row, book)
                except (ValueError, KeyError) as e:
                    QMessageBox.warning(self, 'Error', f'Failed to parse books data: {str(e)}')
            elif response.status_code == 401:
                # For book viewing, we don't need to authenticate
                # Only try to authenticate for protected operations
                pass
            else:
                try:
                    error_msg = response.json().get('detail', response.text)
                except ValueError:
                    error_msg = response.text
                QMessageBox.warning(self, 'Error', f'Failed to load books: {error_msg}')
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, 'Error', f'Failed to connect to server: {str(e)}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'An unexpected error occurred: {str(e)}')

    def add_book_to_table(self, row, book):
        """Add a book to the specified row in the table."""
        try:
            # Create table items with safe data access
            title = str(book['title']) if 'title' in book else ''
            author = str(book['author']) if 'author' in book else ''
            isbn = str(book['isbn']) if 'isbn' in book else ''
            publisher = str(book['publisher']) if 'publisher' in book else ''
            available = int(book['available']) if 'available' in book else 0
            quantity = int(book['quantity']) if 'quantity' in book else 0
            
            # Create table items
            title_item = QTableWidgetItem(title)
            author_item = QTableWidgetItem(author)
            isbn_item = QTableWidgetItem(isbn)
            publisher_item = QTableWidgetItem(publisher)
            status_item = QTableWidgetItem('Available' if available > 0 else 'Not Available')
            quantity_item = QTableWidgetItem(f'{available}/{quantity}')

            # Set items in the table
            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, author_item)
            self.table.setItem(row, 2, isbn_item)
            self.table.setItem(row, 3, publisher_item)
            self.table.setItem(row, 4, status_item)
            self.table.setItem(row, 5, quantity_item)

            # Create action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 4, 4, 4)

            edit_btn = QPushButton("Edit")
            delete_btn = QPushButton("Delete")
            
            book_id = book.get('id')
            if book_id:
                edit_btn.clicked.connect(lambda: self.edit_book(book))
                delete_btn.clicked.connect(lambda: self.delete_book(book_id))
            else:
                edit_btn.setEnabled(False)
                delete_btn.setEnabled(False)

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 6, action_widget)
        except Exception as e:
            print(f"Error adding book to table: {str(e)}")  # For debugging
            # Create empty row with error message
            for col in range(6):
                self.table.setItem(row, col, QTableWidgetItem("Error"))

    def search_books(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            self.load_books()
            return
            
        try:
            headers = {}
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
                
            response = requests.get(
                f'http://127.0.0.1:8000/api/books/?search={search_term}',
                headers=headers
            )
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Handle both list response and paginated response
                    books = data['results'] if isinstance(data, dict) and 'results' in data else data
                    
                    self.table.setRowCount(0)  # Clear existing rows
                    for book in books:
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        self.add_book_to_table(row, book)
                except (ValueError, KeyError) as e:
                    QMessageBox.warning(self, 'Error', f'Failed to parse search results: {str(e)}')
            elif response.status_code == 401:
                # For book viewing, we don't need to authenticate
                # Only try to authenticate for protected operations
                pass
            else:
                try:
                    error_msg = response.json().get('detail', response.text)
                except ValueError:
                    error_msg = response.text
                self.show_error_dialog("Search failed", error_msg)
        except requests.exceptions.RequestException as e:
            self.show_error_dialog("Connection Error", 
                                 f"Could not connect to the backend server: {str(e)}")
            
    def show_add_dialog(self):
        if not self.token:
            self.check_auth()
            if not self.token:
                return
                
        dialog = AddBookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_books()
        
    def edit_book(self, book):
        # TODO: Implement EditBookDialog
        QMessageBox.information(self, "Coming Soon", "Edit Book functionality will be implemented soon!")
        
    def delete_book(self, book_id):
        if not self.token:
            self.check_auth()
            if not self.token:
                return
                
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this book?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                response = requests.delete(
                    f'http://127.0.0.1:8000/api/books/{book_id}/',
                    headers={'Authorization': f'Bearer {self.token}'}
                )
                if response.status_code == 204:
                    self.load_books()
                else:
                    self.show_error_dialog("Delete failed", response.text)
            except requests.exceptions.ConnectionError:
                self.show_error_dialog("Connection Error", 
                                     "Could not connect to the backend server. Please make sure it's running.")
                
    def check_auth(self):
        """Check authentication and get token."""
        dialog = LoginDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.token = dialog.token
            return True
        return False
        
    def show_error_dialog(self, title, message):
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Icon.Warning)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_box.button(QMessageBox.StandardButton.Ok).setObjectName("okButton")
        error_box.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QLabel {
                color: #2c3e50;
                font-size: 13px;
                padding: 12px;
            }
            QPushButton#okButton {
                background-color: #1a237e;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 24px;
                font-weight: bold;
            }
            QPushButton#okButton:hover {
                background-color: #283593;
            }
        """)
        error_box.exec() 