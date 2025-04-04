from PyQt6.QtCore import QObject, pyqtSignal
from api_service import APIService

class AuthService(QObject):
    # Signals
    logged_in = pyqtSignal(dict)  # Emitted when user logs in successfully
    logged_out = pyqtSignal()     # Emitted when user logs out
    error = pyqtSignal(str)       # Emitted when an error occurs
    
    def __init__(self):
        super().__init__()
        self.api_service = APIService()
        self.current_user = None
        
    def login(self, username, password):
        """
        Attempt to log in user with provided credentials
        """
        try:
            # Call API to login
            response = self.api_service.login(username, password)
            
            # Store user data
            self.current_user = response.get('user')
            
            # Emit success signal
            self.logged_in.emit(self.current_user)
            
            return True
            
        except Exception as e:
            self.error.emit(str(e))
            return False
    
    def logout(self):
        """
        Log out current user
        """
        try:
            # Call API to logout
            self.api_service.logout()
            
            # Clear current user
            self.current_user = None
            
            # Emit logged out signal
            self.logged_out.emit()
            
            return True
            
        except Exception as e:
            self.error.emit(str(e))
            return False
    
    def is_authenticated(self):
        """
        Check if user is currently authenticated
        """
        return self.current_user is not None
    
    def get_current_user(self):
        """
        Get current user data
        """
        return self.current_user
    
    def has_permission(self, permission):
        """
        Check if current user has specific permission
        """
        if not self.current_user:
            return False
            
        # Check user type permissions
        user_type = self.current_user.get('user_type', '')
        
        # Define permission mappings
        permissions = {
            'admin': ['manage_books', 'manage_users', 'view_reports'],
            'staff': ['manage_books', 'view_reports'],
            'teacher': ['view_books']
        }
        
        # Get allowed permissions for user type
        allowed_permissions = permissions.get(user_type, [])
        
        return permission in allowed_permissions
