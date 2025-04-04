from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Load the UI file
        loadUi('frontend/ui/main_window.ui', self)
        
        # Set window properties
        self.setWindowTitle('ShelfTrack - Library Management System')
        self.setMinimumSize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create sidebar
        sidebar = QWidget()
        sidebar.setMaximumWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Add navigation buttons
        nav_buttons = [
            ('Dashboard', self.show_dashboard),
            ('Books', self.show_books),
            ('Users', self.show_users),
            ('Reports', self.show_reports),
            ('Settings', self.show_settings),
        ]
        
        for text, slot in nav_buttons:
            btn = QPushButton(text)
            btn.setMinimumHeight(40)
            btn.clicked.connect(slot)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        
        # Add widgets to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)
        
    def show_dashboard(self):
        # TODO: Implement dashboard view
        pass
        
    def show_books(self):
        # TODO: Implement books view
        pass
        
    def show_users(self):
        # TODO: Implement users view
        pass
        
    def show_reports(self):
        # TODO: Implement reports view
        pass
        
    def show_settings(self):
        # TODO: Implement settings view
        pass
        
    def closeEvent(self, event):
        """Handle application closing"""
        reply = QMessageBox.question(
            self, 'Exit',
            'Are you sure you want to exit?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
