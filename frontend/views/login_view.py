from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect

class LoginView(QWidget):
    loginSuccessful = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Login container
        login_container = QFrame()
        login_container.setObjectName("loginContainer")
        login_container.setStyleSheet("""
            QFrame#loginContainer {
                background-color: white;
                border-radius: 8px;
                min-width: 340px;
                max-width: 340px;
            }
        """)
        
        # Add subtle shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 40))
        login_container.setGraphicsEffect(shadow)
        
        # Login form layout
        form_layout = QVBoxLayout(login_container)
        form_layout.setSpacing(16)
        form_layout.setContentsMargins(24, 32, 24, 32)
        
        # Logo and title section
        logo_label = QLabel("ShelfTrack")
        logo_label.setStyleSheet("""
            QLabel {
                color: #2563eb;
                font-size: 28px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
        """)
        logo_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(logo_label)
        
        subtitle = QLabel("Welcome back! Please login to continue.")
        subtitle.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 14px;
                margin-bottom: 8px;
            }
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(subtitle)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background-color: #f8fafc;
                font-size: 14px;
                color: #334155;
                margin-top: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
                background-color: white;
                padding: 11px 15px;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
        """)
        form_layout.addWidget(self.username_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background-color: #f8fafc;
                font-size: 14px;
                color: #334155;
                margin-top: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
                background-color: white;
                padding: 11px 15px;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
        """)
        form_layout.addWidget(self.password_input)
        
        # Error message (hidden by default)
        self.error_label = QLabel()
        self.error_label.setStyleSheet("""
            QLabel {
                color: #dc2626;
                font-size: 13px;
                padding: 8px 12px;
                border-radius: 4px;
                background-color: #fef2f2;
                border: 1px solid #fee2e2;
                margin-top: 8px;
            }
        """)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()
        form_layout.addWidget(self.error_label)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
                margin-top: 16px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        form_layout.addWidget(self.login_button)
        
        # Set the background color for the entire view
        self.setStyleSheet("""
            LoginView {
                background-color: #f1f5f9;
            }
        """)
        
        main_layout.addStretch()
        main_layout.addWidget(login_container, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        
        # Connect the login button to the login method
        self.login_button.clicked.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
        
    def hide_error(self):
        self.error_label.hide()
        
    def handle_login(self):
        self.hide_error()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
            
        self.loginSuccessful.emit(f"{username}:{password}") 