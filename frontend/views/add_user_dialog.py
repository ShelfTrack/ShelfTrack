from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                               QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QComboBox)
from PySide6.QtCore import Qt
import requests

class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New User")
        self.setFixedWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Add New User")
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
        
        # User form
        form_layout = QFormLayout()
        form_layout.setSpacing(16)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
            }
            QLineEdit::placeholder {
                color: #757575;
            }
        """)
        form_layout.addRow("Username:", self.username_input)
        
        # Email field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
            }
            QLineEdit::placeholder {
                color: #757575;
            }
        """)
        form_layout.addRow("Email:", self.email_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
            }
            QLineEdit::placeholder {
                color: #757575;
            }
        """)
        form_layout.addRow("Password:", self.password_input)
        
        # Role field
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Staff", "Admin"])
        self.role_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                color: black;
            }
            QComboBox:focus {
                border: 2px solid #1a237e;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        form_layout.addRow("Role:", self.role_combo)
        
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
        add_btn = QPushButton("Add User")
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
        add_btn.clicked.connect(self.add_user)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_btn)
        
        layout.addLayout(button_layout)
        
    def add_user(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText().lower()
        
        if not username or not email or not password:
            self.show_error_dialog("Error", "Please fill in all fields")
            return
            
        try:
            response = requests.post('http://localhost:8000/api/users/', 
                                  json={
                                      'username': username,
                                      'email': email,
                                      'password': password,
                                      'is_staff': role == 'admin'
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