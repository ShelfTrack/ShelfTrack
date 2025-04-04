# ShelfTrack - Library Management System

ShelfTrack is a modern library management system built with Django and PyQt6, designed to help schools manage their library resources efficiently.

## Features

- **Book Management**
  - Add, edit, and delete books
  - Track book quantity and availability
  - Generate and scan barcodes
  - Search books by title, author, or ISBN
  - Track book conditions and locations

- **User Management**
  - Multiple user roles (Admin, Staff, Teacher)
  - User authentication and authorization
  - Profile management

- **Multi-School Support**
  - Manage multiple school libraries
  - School-specific settings and configurations
  - Independent book catalogs

- **Modern UI**
  - Clean and intuitive interface
  - Responsive design
  - Dark mode support

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Qt 6.5 or higher

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/shelftrack.git
   cd shelftrack
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   cd backend
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Running the Application

1. Start the Django backend:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. Start the PyQt6 frontend:
   ```bash
   cd frontend
   python main.py
   ```

## Development

- Backend API: http://localhost:8000/api/
- Admin interface: http://localhost:8000/admin/
- Frontend: PyQt6 desktop application

## Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

For security concerns, please see our [SECURITY.md](SECURITY.md) file.