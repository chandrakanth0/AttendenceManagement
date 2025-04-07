from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key!

# 🛠️ MySQL Config with clear parameter names
app.config['MYSQL_HOST'] = 'localhost'         # like mysqli: host
app.config['MYSQL_USER'] = 'root'              # like mysqli: user
app.config['MYSQL_PASSWORD'] = '0000'          # like mysqli: password
app.config['MYSQL_DB'] = 'taskdb'              # like mysqli: database

mysql = MySQL(app)

# 📌 Test MySQL Connection
try:
    conn = mysql.connection
    print("✅ Database connection established successfully.")
except Exception as e:
    print("❌ Database connection failed:", e)

# ============================
# Routes
# ============================

@app.route('/')
def home():
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
        user = cursor.fetchone()
        print("👤 Logged-in User Fetched:", user)

        cursor.execute('SELECT * FROM tasks WHERE user_id = %s', (session['user_id'],))
        tasks = cursor.fetchall()
        print("📝 Tasks Fetched:", tasks)

        return render_template('index.html', user=user, tasks=tasks)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        raw_password = request.form['password']
        hashed_password = generate_password_hash(raw_password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        print("🔍 Checking if username exists:", account)

        if account:
            flash('Username already exists!')
            return redirect(url_for('register'))

        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        mysql.connection.commit()
        print("✅ User Registered:", username)
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        print("🔐 Login Attempt for:", username)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            print("✅ Login Successful:", user)
            return redirect(url_for('home'))

        flash('Invalid credentials!')
        print("❌ Login Failed")

    return render_template('login.html')

@app.route('/logout')
def logout():
    print("👋 User logged out:", session.get('user_id'))
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/add-task', methods=['POST'])
def add_task():
    if 'user_id' in session:
        title = request.form['title']
        description = request.form.get('description', '')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO tasks (title, description, user_id) VALUES (%s, %s, %s)',
                       (title, description, session['user_id']))
        mysql.connection.commit()
        print("➕ Task Added:", title)
    return redirect(url_for('home'))

@app.route('/complete-task/<int:task_id>')
def complete_task(task_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE tasks SET is_complete = 1 WHERE id = %s AND user_id = %s',
                   (task_id, session['user_id']))
    mysql.connection.commit()
    print(f"✅ Task {task_id} marked as complete")
    return redirect(url_for('home'))

@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s',
                   (task_id, session['user_id']))
    mysql.connection.commit()
    print(f"🗑️ Task {task_id} deleted")
    return redirect(url_for('home'))

# ============================
# Start the App
# ============================

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(debug=True)
