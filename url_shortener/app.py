import sqlite3
import string
import random
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Function to generate a random 6-character code
def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form.get('url')

    if not original_url:
        flash("Please enter a URL!")
        return redirect('/')

    short_code = generate_short_code()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
        conn.commit()
    except sqlite3.IntegrityError:
        # In case of a collision, try once more
        short_code = generate_short_code()
        cursor.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
        conn.commit()
    finally:
        conn.close()

    short_url = request.host_url + short_code
    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
