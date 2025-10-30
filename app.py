import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'products.db')
ALLOWED_EXT = {'png','jpg','jpeg','gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB limit
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL DEFAULT 0,
            image TEXT
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_conn()
    products = conn.execute('SELECT * FROM products ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/add', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '0').strip()
        file = request.files.get('image')
        filename = None
        if not name:
            flash('Product name is required', 'error')
            return redirect(request.url)
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # If filename exists, add a suffix
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(save_path):
                    filename = f"{base}_{counter}{ext}"
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    counter += 1
                file.save(save_path)
            else:
                flash('File type not allowed', 'error')
                return redirect(request.url)
        try:
            price_val = float(price) if price else 0.0
        except:
            price_val = 0.0
        conn = get_db_conn()
        conn.execute('INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)',
                     (name, description, price_val, filename))
        conn.commit()
        conn.close()
        flash('Product added', 'success')
        return redirect(url_for('index'))
    return render_template('add_product.html')

if __name__ == '__main__':
    init_db()
    # Useful for local dev. In production use a WSGI server (gunicorn)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
