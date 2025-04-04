from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer

def show_error(parent, title, message):
    """Show error message box"""
    QMessageBox.critical(parent, title, message)

def show_info(parent, title, message):
    """Show information message box"""
    QMessageBox.information(parent, title, message)

def show_warning(parent, title, message):
    """Show warning message box"""
    QMessageBox.warning(parent, title, message)

def show_confirmation(parent, title, message):
    """Show confirmation dialog and return True if user confirms"""
    reply = QMessageBox.question(
        parent, title, message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    return reply == QMessageBox.StandardButton.Yes

class LoadingDialog(QDialog):
    """Loading dialog with progress bar"""
    def __init__(self, parent=None, message="Loading..."):
        super().__init__(parent)
        self.init_ui(message)
        
    def init_ui(self, message):
        # Set window properties
        self.setWindowTitle("Please Wait")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Add message label
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        # Add progress bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)  # Indeterminate progress
        layout.addWidget(self.progress)
        
        # Set size
        self.setFixedSize(300, 100)
        
    def set_message(self, message):
        """Update loading message"""
        self.label.setText(message)

def debounce(wait_ms):
    """
    Decorator to debounce a function call
    Useful for search input to avoid too many API calls
    """
    def decorator(fn):
        timer = None
        def debounced(*args, **kwargs):
            nonlocal timer
            if timer is not None:
                timer.stop()
            timer = QTimer()
            timer.timeout.connect(lambda: fn(*args, **kwargs))
            timer.setSingleShot(True)
            timer.start(wait_ms)
        return debounced
    return decorator

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def format_date(date_str):
    """Format date string for display"""
    from datetime import datetime
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%B %d, %Y")
    except:
        return date_str
