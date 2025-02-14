from flask import Flask, request, redirect, url_for, flash, render_template

from Page.login import get_db
app = Flask(__name__)
app.secret_key = 'SECRET_KEY'  # Ganti dengan kunci rahasia Anda

# Route Signup
# @app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nama = request.form['nama']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']


        # Simpan user ke database
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pengguna (namalengkap, username, password, hakakses) VALUES (%s, %s, %s, %s)", 
                (nama, username, password, role)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Signup berhasil! Silakan login.', 'success')
            return redirect(url_for('signin'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('register'))

    return render_template('Signuppage.html')  # Pastikan template ada
