from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                               QComboBox, QFormLayout, QDialog, QMessageBox)
from PySide6.QtCore import Qt
import requests
from .login_dialog import LoginDialog
from .add_user_dialog import AddUserDialog

class UsersView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Users Management")
        title.setStyleSheet("""
            QLabel {
                color: #1a237e;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 16px;
            }
        """)
        layout.addWidget(title)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setSpacing(12)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search users...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet("""
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
        
        search_btn = QPushButton("Search")
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
        search_btn.clicked.connect(self.search_users)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addStretch()
        
        layout.addLayout(search_layout)
        
        # Add User button
        add_btn = QPushButton("Add New User")
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
        layout.addWidget(add_btn)
        
        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
            }
            QTableWidget::item {
                padding: 12px;
                color: black;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
            QTableHeaderView::section {
                background-color: white;
                padding: 12px;
                border-bottom: 2px solid #e0e0e0;
                font-weight: 500;
                color: black;
            }
        """)
        
        # Set up columns
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Username", "Email", "Role", "Progress", "Actions"
        ])
        
        # Set column widths
        self.table.setColumnWidth(0, 200)  # Username
        self.table.setColumnWidth(1, 250)  # Email
        self.table.setColumnWidth(2, 100)  # Role
        self.table.setColumnWidth(3, 200)  # Progress
        self.table.setColumnWidth(4, 180)  # Actions
        
        # Table styling
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
        
        # Load initial data
        self.load_users()
        
    def load_users(self):
        try:
            response = requests.get('http://localhost:8000/api/users/')
            if response.status_code == 200:
                users = response.json()
                self.table.setRowCount(len(users))
                
                for row, user in enumerate(users):
                    self.add_user_to_table(row, user)
            else:
                self.show_error_dialog("Failed to load users", response.text)
        except requests.exceptions.ConnectionError:
            self.show_error_dialog("Connection Error", 
                                 "Could not connect to the backend server. Please make sure it's running.")
            
    def add_user_to_table(self, row, user):
        # Add user data to table
        for col, value in enumerate([
            user.get('username', ''),
            user.get('email', ''),
            'Admin' if user.get('is_staff', False) else 'Staff',
            f"{user.get('progress', 0)}%"
        ]):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.table.setItem(row, col, item)
        
        # Create action buttons widget
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(4, 2, 4, 2)
        actions_layout.setSpacing(8)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("tableButton")
        edit_btn.setFixedSize(75, 32)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(lambda: self.edit_user(user.get('id')))
        edit_btn.setStyleSheet("""
            QPushButton#tableButton {
                background-color: #1a237e;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                font-size: 13px;
                padding: 4px 12px;
                margin: 0px 2px;
            }
            QPushButton#tableButton:hover {
                background-color: #283593;
            }
        """)
        
        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("dangerButton")
        delete_btn.setFixedSize(75, 32)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda: self.delete_user(user.get('id')))
        delete_btn.setStyleSheet("""
            QPushButton#dangerButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                font-size: 13px;
                padding: 4px 12px;
                margin: 0px 2px;
            }
            QPushButton#dangerButton:hover {
                background-color: #c62828;
            }
        """)
        
        # Add buttons to layout
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set the widget in the table
        self.table.setCellWidget(row, 4, actions_widget)
        
    def search_users(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            self.load_users()
            return
            
        try:
            response = requests.get(f'http://localhost:8000/api/users/?search={search_term}')
            if response.status_code == 200:
                users = response.json()
                self.table.setRowCount(len(users))
                
                for row, user in enumerate(users):
                    self.add_user_to_table(row, user)
            else:
                self.show_error_dialog("Search failed", response.text)
        except requests.exceptions.ConnectionError:
            self.show_error_dialog("Connection Error", 
                                 "Could not connect to the backend server. Please make sure it's running.")
            
    def show_add_dialog(self):
        if not self.token:
            self.check_auth()
            if not self.token:
                return
                
        dialog = AddUserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_users()
        
    def edit_user(self, user_id):
        # TODO: Implement EditUserDialog
        QMessageBox.information(self, "Coming Soon", "Edit User functionality will be implemented soon!")
        
    def delete_user(self, user_id):
        if not self.token:
            self.check_auth()
            if not self.token:
                return
                
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this user?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                response = requests.delete(f'http://localhost:8000/api/users/{user_id}/',
                                        headers={'Authorization': f'Bearer {self.token}'})
                if response.status_code == 204:
                    self.load_users()
                else:
                    self.show_error_dialog("Delete failed", response.text)
            except requests.exceptions.ConnectionError:
                self.show_error_dialog("Connection Error", 
                                     "Could not connect to the backend server. Please make sure it's running.")
                
    def check_auth(self):
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