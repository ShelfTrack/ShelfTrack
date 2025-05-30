# Project Structure

```
├── .gitignore                        # Ignore unnecessary files
├── .env                              # Environment variables (DB creds, API keys)
├── LICENSE                           # License for your project
├── README.md                         # Project documentation
├── SECURITY.md                       # Security guidelines
├── requirements.txt                  # Python package dependencies
├── structure.md                      # Project structure documentation

├── backend/                          # Django Backend
│   ├── manage.py                     # Django CLI
│   ├── db.sqlite3                    # Local DB (for dev)
│   ├── backend/                      # Core Django project
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py               # Django settings
│   │   ├── urls.py                   # Root URL routing
│   │   └── wsgi.py                   # WSGI entry point
│   ├── database/                     # Database configurations
│   │   └── db.py                     # DB connection (for direct access, if needed)
│   ├── models/                       # Django models
│   │   ├── book.py                   # Book model
│   │   ├── school.py                 # School model (for multi-school logic)
│   │   └── user.py                   # Custom user model (if needed)
│   ├── services/                     # Service layer for business logic
│   │   ├── book_service.py           # Book-related operations
│   │   └── school_service.py         # School-related operations
│   ├── utils/                        # Utility functions
│   │   ├── barcode.py                # Barcode generator
│   │   └── pagination.py             # Helper for paginated results
│   └── templates/                    # Django templates (if needed for testing)

├── frontend/                         # PyQt6 Frontend
│   ├── main.py                       # Main entry point for PyQt6 app
│   ├── ui/                           # UI components (Qt Designer .ui files)
│   │   ├── book_management.ui
│   │   └── main_window.ui
│   ├── views/                        # PyQt6 view logic
│   │   ├── book_management.py        # Book management UI logic
│   │   └── main_window.py            # Main window handling
│   ├── services/                     # API service handlers
│   │   ├── api_service.py            # Handles API requests
│   │   └── auth_service.py           # Handles login/signup requests
│   └── utils/                        # Frontend utilities
│       └── ui_helpers.py

├── test/                             # Tests
│   ├── __init__.py
│   ├── main.py                       # Test entry point
│   ├── test_backend.py               # Backend test cases
│   └── test_frontend.py              # Frontend test cases
```

## Directory Structure Explanation

### Root Directory
- Configuration files and documentation
- Environment and dependency management
- License and security information

### Backend (`backend/`)
- Django-based REST API
- Database models and migrations
- Business logic services
- Utility functions
- Template files (if needed)

### Frontend (`frontend/`)
- PyQt6-based desktop application
- UI components and layouts
- View logic for different screens
- API service integration
- Authentication handling
- Utility functions

### Tests (`test/`)
- Unit tests for backend
- Integration tests
- Frontend component tests
- Test utilities and helpers

## Key Components

### Backend Components
1. **Models**: Database schema definitions
2. **Services**: Business logic implementation
3. **Utils**: Helper functions and utilities
4. **API Endpoints**: REST API interface

### Frontend Components
1. **UI Files**: Qt Designer layouts
2. **Views**: Screen logic and user interaction
3. **Services**: API communication
4. **Utils**: Helper functions

### Testing Components
1. **Backend Tests**: API and model testing
2. **Frontend Tests**: UI component testing
3. **Integration Tests**: End-to-end testing