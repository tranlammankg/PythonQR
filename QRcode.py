# Import necessary libraries
from flask import Flask, request, render_template, send_file
import qrcode
import io
from PIL import Image
from urllib.parse import unquote
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os
import sys
import html

# Create a Flask app instance
app = Flask(__name__)

# Load default configuration
# This configuration can be overridden by a config file or environment variables.
app.config.from_pyfile('config.cfg')

# Set up logging
# Create a rotating file handler to log messages to a file.
# The file will be rotated when it reaches a certain size or number of backups.
LOG_FILE = f"app_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
handler = RotatingFileHandler(LOG_FILE, maxBytes=40 * 1024 * 1024, backupCount=5)  # 40MB per file, 5 backups
handler.setLevel(logging.DEBUG)

# Create a formatter to format log messages.
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)

# Add the handler to the app's logger.
app.logger.addHandler(handler)

# Set the app's logger level to DEBUG.
app.logger.setLevel(logging.DEBUG)

# Log every request's URL before handling it
@app.before_request
def log_request_info():
    """Log the full URL of incoming requests."""
    app.logger.debug(f"Request URL: {request.url}")

# Define the home route
@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

# Define the QR code generation route
@app.route('/generate', methods=['GET'])
def generate():
    """Generate a QR code image."""

    # Get data and size from request, fallback to default if missing
    data = request.args.get('data', app.config['DEFAULT_DATA'])
    size = request.args.get('size', app.config['DEFAULT_SIZE'])
    border = request.args.get('border', app.config['DEFAULT_BORDER'])

    # Decode the URL-encoded data and escape HTML
    data = unquote(data)
    data = html.escape(data, quote=False)

    # Validate and convert size to integer
    try:
        size = int(size)
        border = int(border)
    except ValueError:
        app.logger.error('Invalid size value provided')
        return "Size must be an integer", 400

    # Calculate box size for QR code
    #total_box_size = size - (2 * border)  # Total size minus the borders
    box_size = size
    #box_size = size // 33  # Adjust this based on your desired scaling

    if box_size <= 0:
        app.logger.error('Box size too small to generate a QR code')
        return "Size too small to generate a QR code", 400

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        #box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill='black', back_color='white')
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Save image to memory buffer
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    app.logger.debug(f"Generated QR code with data: {data} and size: {size}")

    return send_file(img_io, mimetype='image/png')

# Run the app in debug mode
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['DEFAULT_PORT'], debug=app.config['DEBUG'])
# Lấy đường dẫn đến tệp .exe đang chạy
if getattr(sys, 'frozen', False):
    # Đang chạy từ tệp .exe
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    # Đang chạy từ mã nguồn
    base_path = os.path.dirname(os.path.abspath(__file__))

# Tạo đường dẫn cho tệp cấu hình
config_path = os.path.join(base_path, 'config.cfg')

# Kiểm tra xem tệp cấu hình có tồn tại không
if not os.path.isfile(config_path):
    print(f"Config file not found: {config_path}")
    sys.exit(1)
app.config.from_pyfile(config_path)
#app.config.from_pyfile('config.cfg')

Port = app.config['DEFAULT_PORT']
DEBUG = app.config['DEBUG']
# Set up logging
LOG_FILE = f"app_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
handler = RotatingFileHandler(LOG_FILE, maxBytes=40 * 1024 * 1024, backupCount=5)  # 40MB per file, 5 backups
handler.setLevel(logging.DEBUG)

# Adjust the formatter (removed the invalid URL attribute)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Ensure the logger level is set to DEBUG
app.logger.setLevel(logging.DEBUG)

# Log every request's URL before handling it
@app.before_request
def log_request_info():
    """Log the full URL of incoming requests."""
    app.logger.debug(f"Request URL: {request.url}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate():
    # Get data and size from request, fallback to default if missing
    data = request.args.get('data', app.config['DEFAULT_DATA'])
    size = request.args.get('size', app.config['DEFAULT_SIZE'])
    border = request.args.get('border', app.config['DEFAULT_BORDER'])
    
    # Decode the URL-encoded data and escape HTML
    data = unquote(data)
    data = html.escape(data, quote=False)

    # Validate and convert size to integer
    try:
        size = int(size)
        border = int(border)
    except ValueError:
        app.logger.error('Invalid size value provided')
        return "Size must be an integer", 400

    # Calculate box size for QR code
    #total_box_size = size - (2 * border)  # Total size minus the borders
    box_size = size
    #box_size = size // 33  # Adjust this based on your desired scaling

    if box_size <= 0:
        app.logger.error('Box size too small to generate a QR code')
        return "Size too small to generate a QR code", 400

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        #box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill='black', back_color='white')
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Save image to memory buffer
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    app.logger.debug(f"Generated QR code with data: {data} and size: {size}")

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Port, debug=DEBUG)
