from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                               QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Qt
import requests

class AddBookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Book")
        self.setFixedWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Add New Book")
        title.setStyleSheet("""
            QLabel {
                color: #1a237e;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 16px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Book form
        form_layout = QFormLayout()
        form_layout.setSpacing(16)
        
        # Style for form labels
        label_style = """
            QLabel {
                color: #1a237e;
                font-weight: 500;
                font-size: 14px;
                background-color: transparent;
            }
        """
        
        # Create and style labels
        title_label = QLabel("Title:")
        title_label.setStyleSheet(label_style)
        author_label = QLabel("Author:")
        author_label.setStyleSheet(label_style)
        isbn_label = QLabel("ISBN:")
        isbn_label.setStyleSheet(label_style)
        year_label = QLabel("Publication Year:")
        year_label.setStyleSheet(label_style)
        publisher_label = QLabel("Publisher:")
        publisher_label.setStyleSheet(label_style)
        quantity_label = QLabel("Quantity:")
        quantity_label.setStyleSheet(label_style)
        
        # Input fields with white background
        input_style = """
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                color: black;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
            }
            QLineEdit::placeholder {
                color: #757575;
            }
        """
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter title")
        self.title_input.setStyleSheet(input_style)
        
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Enter author")
        self.author_input.setStyleSheet(input_style)
        
        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("Enter ISBN")
        self.isbn_input.setStyleSheet(input_style)
        
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Enter publication year")
        self.year_input.setStyleSheet(input_style)
        
        self.publisher_input = QLineEdit()
        self.publisher_input.setPlaceholderText("Enter publisher")
        self.publisher_input.setStyleSheet(input_style)
        
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setStyleSheet(input_style)
        
        # Add rows to form layout with styled labels
        form_layout.addRow(title_label, self.title_input)
        form_layout.addRow(author_label, self.author_input)
        form_layout.addRow(isbn_label, self.isbn_input)
        form_layout.addRow(year_label, self.year_input)
        form_layout.addRow(publisher_label, self.publisher_input)
        form_layout.addRow(quantity_label, self.quantity_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        # Add button
        add_btn = QPushButton("Add Book")
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
        add_btn.clicked.connect(self.add_book)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_btn)
        
        layout.addLayout(button_layout)
        
    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        isbn = self.isbn_input.text().strip()
        year = self.year_input.text().strip()
        publisher = self.publisher_input.text().strip()
        quantity = self.quantity_input.text().strip()
        
        if not all([title, author, isbn, year, publisher, quantity]):
            self.show_error_dialog("Error", "Please fill in all fields")
            return
            
        try:
            year = int(year)
            quantity = int(quantity)
        except ValueError:
            self.show_error_dialog("Error", "Year and quantity must be numbers")
            return
            
        try:
            response = requests.post('http://localhost:8000/api/books/', 
                                  json={
                                      'title': title,
                                      'author': author,
                                      'isbn': isbn,
                                      'publication_year': year,
                                      'publisher': publisher,
                                      'quantity': quantity,
                                      'available': quantity
                                  })
            
            if response.status_code == 201:
                self.accept()
            else:
                self.show_error_dialog("Error", response.text)
        except requests.exceptions.ConnectionError:
            self.show_error_dialog("Connection Error", 
                                 "Could not connect to the backend server. Please make sure it's running.")
            
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