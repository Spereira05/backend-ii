# Refactored web application with improved error handling, logging, and performance
from flask import Flask, request, jsonify, g
import sqlite3
import logging
import time
from functools import wraps
from werkzeug.exceptions import HTTPException
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create the Flask application
app = Flask(__name__)

# Application configuration
DATABASE = 'products.db'
ROWS_PER_PAGE = 20
app.config['JSON_SORT_KEYS'] = False  # Preserve key order in JSON responses

# Database initialization
def init_db():
    """Initialize the database with sample data if empty"""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Create products table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Add index for search optimization
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_product_name ON products(name)')
        
        # Add some sample data if table is empty
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            logger.info("Initializing database with sample data")
            products = [
                ('Laptop', 999.99, 10),
                ('Smartphone', 499.99, 20),
                ('Headphones', 99.99, 30),
                ('Tablet', 299.99, 15),
                ('Monitor', 249.99, 5)
            ]
            cursor.executemany(
                'INSERT INTO products (name, price, stock) VALUES (?, ?, ?)', 
                products
            )
            db.commit()

# Database connection management
def get_db():
    """Get database connection for the current request"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Enable row factory for dict-like access
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection when application context ends"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Performance monitoring decorator
def timing_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Function {f.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Request validation functions
def validate_product_data(data):
    """Validate product data from request"""
    errors = []
    
    if not data:
        errors.append("No data provided")
        return errors
    
    if 'name' not in data or not data['name']:
        errors.append("Product name is required")
    elif not isinstance(data['name'], str):
        errors.append("Product name must be a string")
    
    if 'price' not in data:
        errors.append("Product price is required")
    elif not isinstance(data['price'], (int, float)) or data['price'] < 0:
        errors.append("Product price must be a positive number")
    
    if 'stock' not in data:
        errors.append("Product stock is required")
    elif not isinstance(data['stock'], int) or data['stock'] < 0:
        errors.append("Product stock must be a non-negative integer")
    
    return errors

# Routes
@app.route('/products', methods=['GET'])
@timing_decorator
def get_products():
    """Get all products with pagination"""
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
            
        offset = (page - 1) * ROWS_PER_PAGE
        
        db = get_db()
        cursor = db.cursor()
        
        # Get total count for pagination info
        cursor.execute('SELECT COUNT(*) FROM products')
        total_count = cursor.fetchone()[0]
        
        # Get paginated results with proper parameter binding
        cursor.execute(
            'SELECT * FROM products ORDER BY id LIMIT ? OFFSET ?', 
            (ROWS_PER_PAGE, offset)
        )
        
        # Use dictionary cursor for efficient JSON conversion
        products = [dict(zip(['id', 'name', 'price', 'stock', 'created_at'], row)) for row in cursor.fetchall()]
        
        # Return with pagination metadata
        return jsonify({
            'products': products,
            'pagination': {
                'page': page,
                'per_page': ROWS_PER_PAGE,
                'total_count': total_count,
                'total_pages': (total_count + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting products: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/product/<int:product_id>', methods=['GET'])
@timing_decorator
def get_product(product_id):
    """Get a single product by ID"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Use parameter binding to prevent SQL injection
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        
        if product:
            # Convert to dictionary for JSON response
            product_dict = dict(zip(['id', 'name', 'price', 'stock', 'created_at'], product))
            return jsonify(product_dict), 200
        else:
            logger.info(f"Product not found: {product_id}")
            return jsonify({'error': 'Product not found'}), 404
            
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/product', methods=['POST'])
@timing_decorator
def add_product():
    """Add a new product"""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_product_data(data)
        if errors:
            return jsonify({'errors': errors}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # Use proper parameter binding
        cursor.execute(
            'INSERT INTO products (name, price, stock) VALUES (?, ?, ?)',
            (data['name'], data['price'], data['stock'])
        )
        db.commit()
        new_id = cursor.lastrowid
        
        # Fetch the new product to return
        cursor.execute('SELECT * FROM products WHERE id = ?', (new_id,))
        new_product = cursor.fetchone()
        product_dict = dict(zip(['id', 'name', 'price', 'stock', 'created_at'], new_product))
        
        logger.info(f"Created new product: {new_id}")
        return jsonify(product_dict), 201
        
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/product/<int:product_id>', methods=['PUT'])
@timing_decorator
def update_product(product_id):
    """Update an existing product"""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_product_data(data)
        if errors:
            return jsonify({'errors': errors}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # Check if product exists
        cursor.execute('SELECT id FROM products WHERE id = ?', (product_id,))
        if not cursor.fetchone():
            logger.info(f"Product not found for update: {product_id}")
            return jsonify({'error': 'Product not found'}), 404
        
        # Update product with parameter binding
        cursor.execute(
            'UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?',
            (data['name'], data['price'], data['stock'], product_id)
        )
        db.commit()
        
        # Get updated product
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        updated_product = cursor.fetchone()
        product_dict = dict(zip(['id', 'name', 'price', 'stock', 'created_at'], updated_product))
        
        logger.info(f"Updated product: {product_id}")
        return jsonify(product_dict), 200
        
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/product/<int:product_id>', methods=['DELETE'])
@timing_decorator
def delete_product(product_id):
    """Delete a product"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Check if product exists
        cursor.execute('SELECT id FROM products WHERE id = ?', (product_id,))
        if not cursor.fetchone():
            logger.info(f"Product not found for deletion: {product_id}")
            return jsonify({'error': 'Product not found'}), 404
        
        # Delete product
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        db.commit()
        
        logger.info(f"Deleted product: {product_id}")
        return jsonify({'message': f'Product {product_id} deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/search', methods=['GET'])
@timing_decorator
def search_products():
    """Search products by name (optimized)"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'products': [], 'count': 0}), 200
        
        db = get_db()
        cursor = db.cursor()
        
        # Use SQL LIKE for efficient searching with parameter binding
        search_param = f'%{query}%'
        cursor.execute(
            'SELECT * FROM products WHERE name LIKE ? ORDER BY name LIMIT 100',
            (search_param,)
        )
        
        products = [dict(zip(['id', 'name', 'price', 'stock', 'created_at'], row)) for row in cursor.fetchall()]
        
        return jsonify({
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching products: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

# Error handlers
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Handle HTTP exceptions"""
    response = jsonify({'error': e.description})
    response.status_code = e.code
    logger.warning(f"HTTP error: {e.code} - {e.description}")
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    }), 200

# Initialize the database before first request
@app.before_first_request
def before_first_request():
    """Initialize the database before first request"""
    init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)