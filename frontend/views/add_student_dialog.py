from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
                               QPushButton, QLabel, QMessageBox, QComboBox,
                               QDateEdit, QSpinBox, QFormLayout, QFrame, QWidget, QScrollArea)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor, QScreen
import requests
from datetime import datetime

class FormSection(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("formSection")
        self.setStyleSheet("""
            QFrame#formSection {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                padding: 16px;
                margin: 8px;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(16)
        self.layout.setContentsMargins(16, 16, 16, 16)
        
        # Title with subtitle
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setSpacing(4)
        title_layout.setContentsMargins(0, 0, 0, 8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        title_layout.addWidget(title_label)
        
        subtitle = QLabel("Please fill in all required fields")
        subtitle.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 13px;
            }
        """)
        title_layout.addWidget(subtitle)
        
        self.layout.addWidget(title_container)

class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Student")
        self.setModal(True)
        
        # Set dialog size based on screen size
        if parent:
            screen = parent.screen()
            if screen:
                screen_geometry = screen.geometry()
                self.setMinimumWidth(500)  # Set minimum width
                self.setMinimumHeight(600)  # Set minimum height
                max_width = min(800, int(screen_geometry.width() * 0.6))
                max_height = int(screen_geometry.height() * 0.9)
                self.setMaximumWidth(max_width)
                self.setMaximumHeight(max_height)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f8fafc;
            }
            QLabel {
                color: #1e293b;
                font-size: 14px;
                font-weight: 500;
            }
            QLineEdit, QComboBox, QDateEdit {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #1e293b;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #3b82f6;
                background-color: white;
            }
            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
                border: 1px solid #94a3b8;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
            QComboBox {
                padding-right: 24px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #64748b;
                margin-right: 8px;
            }
            QComboBox:on {
                border: 2px solid #3b82f6;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 4px;
                selection-background-color: #e2e8f0;
                selection-color: #1e293b;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                min-height: 24px;
                padding: 4px 8px;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f1f5f9;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e2e8f0;
            }
            QDateEdit {
                padding-right: 24px;
                background-color: white;
            }
            QDateEdit::drop-down {
                border: none;
                width: 24px;
                background: transparent;
            }
            QDateEdit::down-arrow {
                image: none;
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #64748b;
                margin-right: 8px;
            }
            QDateEdit:on {
                border: 2px solid #3b82f6;
            }
            QCalendarWidget {
                background-color: white;
                min-width: 300px;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: white;
                padding: 8px;
            }
            QCalendarWidget QToolButton {
                color: #1e293b;
                background-color: white;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
                border: none;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #f1f5f9;
            }
            QCalendarWidget QSpinBox {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                color: #1e293b;
                padding: 4px;
            }
            QCalendarWidget QWidget { 
                alternate-background-color: transparent;
                background-color: white;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #1e293b;
                selection-background-color: #3b82f6;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #94a3b8;
            }
            QCalendarWidget QWidget#qt_calendar_calendarview {
                background-color: white;
                border: none;
                outline: none;
            }
            QCalendarWidget QTableView {
                background-color: white;
                outline: none;
                selection-background-color: #3b82f6;
                selection-color: white;
                border: none;
            }
            QCalendarWidget QMenu {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                padding: 4px;
            }
            QCalendarWidget QMenu::item {
                padding: 4px 8px;
            }
            QCalendarWidget QMenu::item:selected {
                background-color: #3b82f6;
                color: white;
            }
            QCalendarWidget QWidget#qt_calendar_prevmonth,
            QCalendarWidget QWidget#qt_calendar_nextmonth {
                border: none;
                background-color: transparent;
                padding: 4px;
                border-radius: 4px;
                qproperty-icon: none;
            }
            QCalendarWidget QWidget#qt_calendar_prevmonth:hover,
            QCalendarWidget QWidget#qt_calendar_nextmonth:hover {
                background-color: #f1f5f9;
            }
            QCalendarWidget QWidget#qt_calendar_monthbutton,
            QCalendarWidget QWidget#qt_calendar_yearbutton {
                color: #1e293b;
                font-weight: bold;
                font-size: 14px;
                padding: 4px 12px;
                border-radius: 4px;
            }
            QCalendarWidget QWidget#qt_calendar_monthbutton:hover,
            QCalendarWidget QWidget#qt_calendar_yearbutton:hover {
                background-color: #f1f5f9;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar > QWidget {
                border: none;
                background: transparent;
            }
        """)
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Add New Student")
        title.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 16px;
            }
        """)
        main_layout.addWidget(title)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #f1f5f9;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Container widget for scroll area
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(16)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Personal Information Section
        personal_section = FormSection("Personal Information")
        
        # Student ID
        id_layout = QVBoxLayout()
        id_label = QLabel("Student ID*")
        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("Enter student ID")
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.student_id)
        personal_section.layout.addLayout(id_layout)
        
        # Name
        name_layout = QVBoxLayout()
        name_label = QLabel("Full Name*")
        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter student's full name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name)
        personal_section.layout.addLayout(name_layout)
        
        # Gender
        gender_layout = QVBoxLayout()
        gender_label = QLabel("Gender*")
        self.gender = QLineEdit()
        self.gender.setPlaceholderText("Enter gender (e.g., Male, Female, Other)")
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender)
        personal_section.layout.addLayout(gender_layout)
        
        # Date of Birth
        dob_layout = QVBoxLayout()
        dob_label = QLabel("Date of Birth*")
        self.dob = QLineEdit()
        self.dob.setPlaceholderText("Enter date of birth (DD-MM-YYYY)")
        dob_layout.addWidget(dob_label)
        dob_layout.addWidget(self.dob)
        personal_section.layout.addLayout(dob_layout)
        
        container_layout.addWidget(personal_section)
        
        # Academic Information Section
        academic_section = FormSection("Academic Information")
        
        # Grade
        grade_layout = QVBoxLayout()
        grade_label = QLabel("Grade*")
        self.grade = QLineEdit()
        self.grade.setPlaceholderText("Enter grade (1-12)")
        grade_layout.addWidget(grade_label)
        grade_layout.addWidget(self.grade)
        academic_section.layout.addLayout(grade_layout)
        
        # Section
        section_layout = QVBoxLayout()
        section_label = QLabel("Section*")
        self.section = QLineEdit()
        self.section.setPlaceholderText("Enter section (e.g., A, B, C)")
        section_layout.addWidget(section_label)
        section_layout.addWidget(self.section)
        academic_section.layout.addLayout(section_layout)
        
        container_layout.addWidget(academic_section)
        
        # Parent Information Section
        parent_section = FormSection("Parent Information")
        
        # Parent Name
        parent_name_layout = QVBoxLayout()
        parent_name_label = QLabel("Parent Name*")
        self.parent_name = QLineEdit()
        self.parent_name.setPlaceholderText("Enter parent's full name")
        parent_name_layout.addWidget(parent_name_label)
        parent_name_layout.addWidget(self.parent_name)
        parent_section.layout.addLayout(parent_name_layout)
        
        # Parent Phone
        parent_phone_layout = QVBoxLayout()
        parent_phone_label = QLabel("Parent Phone*")
        self.parent_phone = QLineEdit()
        self.parent_phone.setPlaceholderText("Enter parent's phone number")
        parent_phone_layout.addWidget(parent_phone_label)
        parent_phone_layout.addWidget(self.parent_phone)
        parent_section.layout.addLayout(parent_phone_layout)
        
        # Parent Email
        parent_email_layout = QVBoxLayout()
        parent_email_label = QLabel("Parent Email*")
        self.parent_email = QLineEdit()
        self.parent_email.setPlaceholderText("Enter parent's email address")
        parent_email_layout.addWidget(parent_email_label)
        parent_email_layout.addWidget(self.parent_email)
        parent_section.layout.addLayout(parent_email_layout)
        
        container_layout.addWidget(parent_section)
        
        # Add container to scroll area
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                min-width: 100px;
                min-height: 36px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #475569;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save Student")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                min-width: 100px;
                min-height: 36px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        save_btn.clicked.connect(self.save_student)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        main_layout.addLayout(button_layout)
        
    def save_student(self):
        # Validate required fields
        required_fields = {
            'Student ID': self.student_id.text().strip(),
            'Full Name': self.name.text().strip(),
            'Gender': self.gender.text().strip(),
            'Date of Birth': self.dob.text().strip(),
            'Grade': self.grade.text().strip(),
            'Section': self.section.text().strip(),
            'Parent Name': self.parent_name.text().strip(),
            'Parent Phone': self.parent_phone.text().strip(),
            'Parent Email': self.parent_email.text().strip()
        }
        
        # Check for empty fields
        empty_fields = [field for field, value in required_fields.items() if not value]
        if empty_fields:
            QMessageBox.warning(
                self,
                "Required Fields",
                f"Please fill in the following required fields:\n{', '.join(empty_fields)}",
                QMessageBox.StandardButton.Ok
            )
            return
            
        # Validate date format (DD-MM-YYYY)
        try:
            datetime.strptime(self.dob.text().strip(), '%d-%m-%Y')
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Date Format",
                "Date of Birth must be in the format DD-MM-YYYY.",
                QMessageBox.StandardButton.Ok
            )
            return
            
        # Validate grade
        try:
            grade = int(self.grade.text().strip())
            if not (1 <= grade <= 12):
                raise ValueError()
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Grade",
                "Grade must be a number between 1 and 12.",
                QMessageBox.StandardButton.Ok
            )
            return
            
        # Validate section format
        section = self.section.text().strip().upper()
        if not (len(section) == 1 and section.isalpha()):
            QMessageBox.warning(
                self,
                "Invalid Section",
                "Section must be a single letter (A-Z).",
                QMessageBox.StandardButton.Ok
            )
            return
            
        # Validate phone number format
        phone = self.parent_phone.text().strip()
        if not (phone.isdigit() and len(phone) == 10):
            QMessageBox.warning(
                self,
                "Invalid Phone Number",
                "Please enter a valid 10-digit phone number.",
                QMessageBox.StandardButton.Ok
            )
            return
            
        # Validate email format
        email = self.parent_email.text().strip()
        if '@' not in email or '.' not in email:
            QMessageBox.warning(
                self,
                "Invalid Email",
                "Please enter a valid email address.",
                QMessageBox.StandardButton.Ok
            )
            return
            
        # Prepare data for API
        data = {
            'student_id': required_fields['Student ID'],
            'name': required_fields['Full Name'],
            'gender': required_fields['Gender'],
            'date_of_birth': self.dob.text().strip(),
            'grade': grade,
            'section': section,
            'parent_name': required_fields['Parent Name'],
            'parent_phone': phone,
            'parent_email': email
        }
        
        try:
            response = requests.post('http://localhost:8000/api/students/', json=data)
            
            if response.status_code == 201:
                QMessageBox.information(
                    self,
                    "Success",
                    f"Student {data['name']} has been added successfully!",
                    QMessageBox.StandardButton.Ok
                )
                self.accept()
            else:
                error_data = response.json()
                error_message = error_data.get('detail', 'An error occurred while adding the student.')
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to add student: {error_message}",
                    QMessageBox.StandardButton.Ok
                )
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to connect to the server: {str(e)}",
                QMessageBox.StandardButton.Ok
            ) 