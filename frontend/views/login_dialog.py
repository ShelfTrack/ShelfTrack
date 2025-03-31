from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, 
                               QPushButton, QLabel, QMessageBox, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor
import requests

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None
        self.setWindowTitle("ShelfTrack Login")
        self.setFixedSize(420, 560)  # Increased size for better spacing
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #f0f6ff, stop:1 #f8f9ff);
            }
        """)
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout with proper spacing
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 50, 40, 50)  # Increased top/bottom margins
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("frontend/assets/logo.png")
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            # Fallback to text if image not found
            logo_label = QLabel("📚")
            logo_label.setStyleSheet("font-size: 56px;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        # App Name with adjusted spacing
        title = QLabel("ShelfTrack")
        title.setStyleSheet("""
            QLabel {
                color: #1e40af;
                font-size: 32px;
                font-weight: 800;
                letter-spacing: -0.5px;
                margin: 16px 0 4px 0;  /* Added top margin */
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Welcome Text
        welcome = QLabel("Welcome back!")
        welcome.setStyleSheet("""
            QLabel {
                color: #475569;
                font-size: 16px;
                font-weight: 500;
                margin-bottom: 24px;
            }
        """)
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)
        
        # Container for input fields using QFrame instead of QLabel
        form_container = QFrame()
        form_container.setFixedWidth(340)  # Fixed width for better control
        form_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.9);
            }
        """)
        
        # Form layout with adjusted spacing
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(16)
        form_layout.setContentsMargins(24, 32, 24, 32)  # Increased padding
        
        # Input fields style
        input_style = """
            QLineEdit {
                padding: 14px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                color: #1e293b;
                background-color: white;
                font-size: 15px;
                font-weight: 500;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
                font-weight: 400;
            }
        """
        
        # Username input with fixed width
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(input_style)
        self.username_input.setFixedHeight(50)
        form_layout.addWidget(self.username_input)
        
        # Password input with fixed width
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)
        self.password_input.setFixedHeight(50)
        form_layout.addWidget(self.password_input)
        
        # Login button
        login_btn = QPushButton("Sign in")
        login_btn.setFixedHeight(50)  # Consistent height with inputs
        login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 15px;
                font-weight: 600;
                margin-top: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #2563eb, stop:1 #1d4ed8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #1d4ed8, stop:1 #1e40af);
            }
        """)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.login)
        form_layout.addWidget(login_btn)
        
        # Center the form container
        layout.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set return key to trigger login
        self.password_input.returnPressed.connect(login_btn.click)
        
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
            
        try:
            response = requests.post(
                'http://localhost:8000/api/token/',
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access')
                self.accept()
            else:
                self.show_error("Invalid username or password")
        except requests.exceptions.ConnectionError:
            self.show_error("Could not connect to the server. Please make sure it's running.")
            
    def show_error(self, message):
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Icon.Warning)
        error_box.setWindowTitle("Login Error")
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_box.button(QMessageBox.StandardButton.Ok).setObjectName("okButton")
        error_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #1e293b;
                font-size: 14px;
                font-weight: 500;
                padding: 16px;
            }
            QPushButton#okButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 24px;
                min-height: 36px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton#okButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)
        error_box.exec() 