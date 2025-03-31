from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management.commands.runserver import BaseRunserverCommand
from django.core.management.base import BaseCommand
import socket

class Command(BaseCommand):
    help = 'Runs the development server with debug output'

    def handle(self, *args, **options):
        # Get all available network interfaces
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        self.stdout.write(self.style.SUCCESS(f'Server will be available at:'))
        self.stdout.write(self.style.SUCCESS(f'http://127.0.0.1:8000/'))
        self.stdout.write(self.style.SUCCESS(f'http://localhost:8000/'))
        self.stdout.write(self.style.SUCCESS(f'http://{local_ip}:8000/'))
        
        # Run the server
        RunserverCommand().handle(*args, **options) 