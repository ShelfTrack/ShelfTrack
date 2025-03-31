from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QFrame, QPushButton, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect
import requests
from datetime import datetime
from .add_student_dialog import AddStudentDialog

class StatCard(QFrame):
    def __init__(self, title, value, icon, color):
        super().__init__()
        self.setObjectName("statCard")
        self.setStyleSheet(f"""
            QLabel {{
                color: #333333;
                background-color: transparent;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a cleaner look
        
        # Icon and title row
        header = QHBoxLayout()
        header.setSpacing(6)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(""" QLabel { font-size: 20px; padding: 2px; background-color: transparent; } """)
        header.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(""" QLabel { font-size: 14px; font-weight: 600; background-color: transparent; } """)
        header.addWidget(title_label)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(""" QLabel { font-size: 24px; font-weight: 700; padding: 4px 0; } """)
        layout.addWidget(self.value_label)
        
    def setValue(self, value):
        self.value_label.setText(str(value))

class ActionButton(QPushButton):
    def __init__(self, text, icon, color, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: {color};
                border: none;
                border-radius: 12px;
                padding: 16px 24px;
                font-size: 15px;
                font-weight: 600;
                text-align: left;
                min-width: 180px;
            }}
            QPushButton:hover {{
                background-color: {color};
                color: white;
            }}
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)
        self.setCursor(Qt.PointingHandCursor)

class ActivityCard(QFrame):
    def __init__(self, title, description, time, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #333333; font-weight: bold;")
        layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #666666;")
        layout.addWidget(desc_label)
        
        time_label = QLabel(time)
        time_label.setStyleSheet("color: #999999; font-size: 12px;")
        layout.addWidget(time_label)

class HomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None
        self.books_card = None  # Initialize here
        self.students_card = None  # Initialize here
        self.staff_card = None  # Initialize here
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(32)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Main content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(32)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Welcome section
        welcome = QLabel("Welcome to ShelfTrack")
        welcome.setStyleSheet(""" QLabel { color: #1a237e; font-size: 36px; font-weight: 800; } """)
        content_layout.addWidget(welcome)

        subtitle = QLabel("Here's an overview of your library")
        subtitle.setStyleSheet(""" QLabel { color: #666666; font-size: 18px; margin-bottom: 24px; } """)
        content_layout.addWidget(subtitle)

        # Stats cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(32)

        # Initialize the StatCards
        self.books_card = StatCard("Total Books", "0", "📚", "#1e88e5")
        self.students_card = StatCard("Students", "0", "👥", "#7b1fa2")
        self.staff_card = StatCard("Staff Members", "0", "👨‍🏫", "#43a047")

        stats_layout.addWidget(self.books_card)
        stats_layout.addWidget(self.students_card)
        stats_layout.addWidget(self.staff_card)
        stats_layout.addStretch()

        content_layout.addLayout(stats_layout)

        # Quick Actions section
        actions_label = QLabel("Quick Actions")
        actions_label.setStyleSheet(""" QLabel { color: #333333; font-size: 24px; font-weight: bold; margin-top: 40px; } """)
        content_layout.addWidget(actions_label)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(24)

        add_book_btn = ActionButton("Add New Book", "📚", "#1e88e5")
        self.add_student_btn = ActionButton("Add Student", "👥", "#7b1fa2")
        issue_book_btn = ActionButton("Issue Book", "📖", "#43a047")

        # Connect the add student button
        self.add_student_btn.clicked.connect(self.show_add_student_dialog)

        actions_layout.addWidget(add_book_btn)
        actions_layout.addWidget(self.add_student_btn)
        actions_layout.addWidget(issue_book_btn)
        actions_layout.addStretch()

        content_layout.addLayout(actions_layout)
        content_layout.addStretch()

        # Add the content widget to the main layout
        main_layout.addWidget(content_widget)

        # Set modern background color
        self.setStyleSheet(""" QWidget { background-color: #f8f9fa; } """)

    def show_add_student_dialog(self):
        dialog = AddStudentDialog(self)
        if dialog.exec() == AddStudentDialog.DialogCode.Accepted:
            self.update_stats()  # Refresh stats after adding a student
            
    def update_stats(self):
        try:
            # Get total books count
            response = requests.get('http://localhost:8000/api/books/')
            if response.status_code == 200:
                data = response.json()
                books_count = len(data['results']) if isinstance(data, dict) and 'results' in data else len(data)
                self.books_card.setValue(books_count)
            else:
                self.books_card.setValue(0)  # Set to 0 if there's an error

            # Get total students count
            response = requests.get('http://localhost:8000/api/students/')
            if response.status_code == 200:
                data = response.json()
                students_count = len(data['results']) if isinstance(data, dict) and 'results' in data else len(data)
                self.students_card.setValue(students_count)
            else:
                self.students_card.setValue(0)  # Set to 0 if there's an error

            # Get total staff count
            response = requests.get('http://localhost:8000/api/staff/')
            if response.status_code == 200:
                data = response.json()
                staff_count = len(data['results']) if isinstance(data, dict) and 'results' in data else len(data)
                self.staff_card.setValue(staff_count)
            else:
                self.staff_card.setValue(0)  # Set to 0 if there's an error
                
        except requests.exceptions.RequestException as e:
            self.books_card.setValue(0)  # Set to 0 on error
            self.students_card.setValue(0)  # Set to 0 on error
            self.staff_card.setValue(0)      # Set to 0 on error 