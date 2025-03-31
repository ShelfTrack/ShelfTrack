#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget)
from views.books_view import BooksView
from views.settings_view import SettingsView
from views.home_view import HomeView
from views.login_dialog import LoginDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShelfTrack")
        self.setMinimumSize(1200, 700)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create and add tabs
        self.home_view = HomeView()
        self.books_view = BooksView()
        self.settings_view = SettingsView()
        
        self.tabs.addTab(self.home_view, "Home")
        self.tabs.addTab(self.books_view, "Books")
        self.tabs.addTab(self.settings_view, "Settings")
        
        # Style the tabs with light theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)
        
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #f5f5f5;
            }
            QTabBar::tab {
                background: #ffffff;
                color: #666666;
                padding: 12px 24px;
                border: none;
                min-width: 120px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background: #1a237e;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: #e3f2fd;
                color: #1a237e;
            }
        """)

def main():
    app = QApplication(sys.argv)
    
    # Set application-wide style
    app.setStyle("Fusion")
    
    # Show login dialog first
    login_dialog = LoginDialog()
    if login_dialog.exec() == LoginDialog.DialogCode.Accepted:
        # If login successful, show main window
        window = MainWindow()
        # Pass the token to all views
        window.home_view.token = login_dialog.token
        window.books_view.token = login_dialog.token
        window.settings_view.token = login_dialog.token
        # Update home view stats
        window.home_view.update_stats()
        window.show()
        sys.exit(app.exec())
    else:
        # If login cancelled or failed, exit application
        sys.exit(0)

if __name__ == '__main__':
    main() 