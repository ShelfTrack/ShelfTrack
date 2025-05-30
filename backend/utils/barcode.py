import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import uuid

def generate_barcode(book):
    """
    Generate a unique barcode for a book.
    Uses Code128 format which can encode alphanumeric data.
    """
    # Generate a unique identifier
    unique_id = str(uuid.uuid4().hex)[:12]
    
    # Create a unique barcode combining book info and unique ID
    # Format: BTYYYYIIIIIIXX where:
    # BT = Book Type (2 chars)
    # YYYY = Publication Year (4 chars)
    # IIIIII = Unique ID (6 chars)
    # XX = Checksum (2 chars)
    
    book_type_code = book.book_type[:2].upper()
    year_code = str(book.publication_year)[-4:]
    unique_code = unique_id[:6]
    
    # Generate the base barcode
    barcode_data = f"{book_type_code}{year_code}{unique_code}"
    
    # Add checksum
    checksum = sum(ord(c) for c in barcode_data) % 100
    barcode_data = f"{barcode_data}{checksum:02d}"
    
    # Generate barcode image
    code128 = barcode.get('code128', barcode_data, writer=ImageWriter())
    
    # Save to BytesIO
    buffer = BytesIO()
    code128.write(buffer)
    
    return barcode_data
