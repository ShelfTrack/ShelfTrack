from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QLineEdit, QFormLayout, QMessageBox)
from PySide6.QtCore import Qt
import requests

class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("""
            QLabel {
                color: #1a237e;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 16px;
            }
        """)
        layout.addWidget(title)
        
        # Settings form
        form_layout = QFormLayout()
        form_layout.setSpacing(16)
        
        # API URL setting
        self.api_url_input = QLineEdit()
        self.api_url_input.setPlaceholderText("Enter API URL")
        self.api_url_input.setStyleSheet("""
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
        form_layout.addRow("API URL:", self.api_url_input)
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.save_settings)
        
        layout.addLayout(form_layout)
        layout.addWidget(save_btn)
        layout.addStretch()
        
        # Style for the view
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QLabel#sectionTitle {
                color: #1a237e;
                font-size: 18px;
                font-weight: bold;
                margin-top: 24px;
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
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #1a237e;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        
    def save_settings(self):
        api_url = self.api_url_input.text().strip()
        if not api_url:
            self.show_error_dialog("Error", "Please enter an API URL")
            return
            
        # TODO: Implement settings save functionality
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        
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