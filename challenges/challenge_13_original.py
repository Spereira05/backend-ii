# Web application with issues to refactor
from flask import Flask, request, jsonify
import sqlite3
import random
import time

app = Flask(__name__)

# Create a basic database with some data
conn = sqlite3.connect('products.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    stock INTEGER
)
''')

# Add some sample data if table is empty
cursor.execute('SELECT COUNT(*) FROM products')
if cursor.fetchone()[0] == 0:
    products = [
        ('Laptop', 999.99, 10),
        ('Smartphone', 499.99, 20),
        ('Headphones', 99.99, 30),
        ('Tablet', 299.99, 15),
        ('Monitor', 249.99, 5)
    ]
    cursor.executemany('INSERT INTO products (name, price, stock) VALUES (?, ?, ?)', products)
    conn.commit()

conn.close()

@app.route('/products', methods=['GET'])
def get_products():
    # No error handling
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    
    # Inefficient transformation
    result = []
    for product in products:
        result.append({
            'id': product[0],
            'name': product[1],
            'price': product[2],
            'stock': product[3]
        })
    
    # Simulate a slow operation
    time.sleep(0.5)
    
    return jsonify(result)

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # SQL injection vulnerability
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM products WHERE id = {product_id}"
    cursor.execute(query)
    product = cursor.fetchone()
    conn.close()
    
    if product:
        return jsonify({
            'id': product[0],
            'name': product[1],
            'price': product[2],
            'stock': product[3]
        })
    else:
        return "Product not found", 404

@app.route('/product', methods=['POST'])
def add_product():
    # No validation
    data = request.get_json()
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO products (name, price, stock) VALUES (?, ?, ?)',
        (data['name'], data['price'], data['stock'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    # Return minimal response
    return jsonify({'id': new_id})

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Missing error handling
    data = request.get_json()
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?',
        (data['name'], data['price'], data['stock'], product_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    
    # No status code returned
    return jsonify({'deleted': product_id})

@app.route('/search', methods=['GET'])
def search_products():
    # Inefficient search implementation
    query = request.args.get('q', '')
    
    if not query:
        return jsonify([])
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    
    # Filter in Python instead of using SQL
    results = []
    for product in products:
        if query.lower() in product[1].lower():
            results.append({
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'stock': product[3]
            })
    
    return jsonify(results)

@app.route('/random_error')
def random_error():
    # Endpoint that randomly fails
    if random.random() < 0.5:
        x = 1 / 0  # This will cause a division by zero error
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)