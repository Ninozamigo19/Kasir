from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import psycopg2
from decouple import config

app = Flask(__name__)
app.secret_key = config('SECRET_KEY', default='36bbfeee4f53a83212bbf8a4984e96101983c4b61c39cc19b0d01fead6332272')

# Database connection
def get_db():
    try:
        conn = psycopg2.connect(
            host=config('DB_HOST'),
            port=config('DB_PORT', default=5432),
            database=config('DB_NAME'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD')
        )
        print("Connection successful!")
        return conn
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        if not conn:
            flash('Database connection failed!', 'danger')
            return render_template('loginpage.html')

        cursor = conn.cursor()
        cursor.execute("SELECT userid, hakakses FROM pengguna WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['userid'] = user[0]
            session['hakakses'] = user[1]
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('userid', str(user[0]))  # Simpan user_id di cookie
            flash('Login berhasil!', 'success')
            return resp
        else:
            flash('Username atau password salah!', 'danger')

    return render_template('loginpage.html')

# Logout route
def logout():
    resp = make_response(redirect(url_for('signin')))
    resp.delete_cookie('userid')  # Hapus cookie saat logout
    # flash('You have been logged out.', 'info')
    return resp

# Home route (protected)
@app.route('/home')
def home():
    userid = request.cookies.get('userid')
    if not userid:
        # flash('You must be logged in to access this page.', 'danger')
        return redirect(url_for('signin'))

    return render_template('Homepage.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)