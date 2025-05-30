import requests
from urllib.parse import urljoin
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIService:
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', 'http://localhost:8000/api/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
    def _handle_response(self, response):
        """Handle API response and errors"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    error_msg = error_data.get('detail', error_msg)
            except:
                pass
            raise Exception(error_msg)
        
    def login(self, username, password):
        """Login user and get authentication token"""
        url = urljoin(self.base_url, 'auth/login/')
        data = {
            'username': username,
            'password': password
        }
        response = self.session.post(url, json=data)
        result = self._handle_response(response)
        
        # Set authentication token
        if 'token' in result:
            self.session.headers['Authorization'] = f"Token {result['token']}"
        
        return result
    
    def logout(self):
        """Logout user and remove authentication token"""
        url = urljoin(self.base_url, 'auth/logout/')
        response = self.session.post(url)
        self._handle_response(response)
        
        # Remove authentication token
        self.session.headers.pop('Authorization', None)
    
    # Book-related API calls
    def get_books(self, page=1, per_page=10, search=None):
        """Get list of books with pagination and search"""
        url = urljoin(self.base_url, 'books/')
        params = {
            'page': page,
            'per_page': per_page
        }
        if search:
            params['search'] = search
            
        response = self.session.get(url, params=params)
        return self._handle_response(response)
    
    def get_book(self, book_id):
        """Get single book details"""
        url = urljoin(self.base_url, f'books/{book_id}/')
        response = self.session.get(url)
        return self._handle_response(response)
    
    def create_book(self, book_data):
        """Create a new book"""
        url = urljoin(self.base_url, 'books/')
        response = self.session.post(url, json=book_data)
        return self._handle_response(response)
    
    def update_book(self, book_id, book_data):
        """Update an existing book"""
        url = urljoin(self.base_url, f'books/{book_id}/')
        response = self.session.put(url, json=book_data)
        return self._handle_response(response)
    
    def delete_book(self, book_id):
        """Delete a book"""
        url = urljoin(self.base_url, f'books/{book_id}/')
        response = self.session.delete(url)
        return self._handle_response(response)
    
    # User-related API calls
    def get_users(self, page=1, per_page=10):
        """Get list of users with pagination"""
        url = urljoin(self.base_url, 'users/')
        params = {
            'page': page,
            'per_page': per_page
        }
        response = self.session.get(url, params=params)
        return self._handle_response(response)
    
    def get_user(self, user_id):
        """Get single user details"""
        url = urljoin(self.base_url, f'users/{user_id}/')
        response = self.session.get(url)
        return self._handle_response(response)
    
    def create_user(self, user_data):
        """Create a new user"""
        url = urljoin(self.base_url, 'users/')
        response = self.session.post(url, json=user_data)
        return self._handle_response(response)
    
    def update_user(self, user_id, user_data):
        """Update an existing user"""
        url = urljoin(self.base_url, f'users/{user_id}/')
        response = self.session.put(url, json=user_data)
        return self._handle_response(response)
    
    def delete_user(self, user_id):
        """Delete a user"""
        url = urljoin(self.base_url, f'users/{user_id}/')
        response = self.session.delete(url)
        return self._handle_response(response)
