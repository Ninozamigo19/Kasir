from flask import Flask, render_template, request, redirect, url_for, flash
from Page.login import get_db

app = Flask(__name__)

conn = get_db()

# @app.route('/hapus_akun/<int:userid>', methods=['POST'])
def hapus_akun(user_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pengguna WHERE userid = %s", (user_id,))
    conn.commit()
    cursor.close()

    # flash('Akun berhasil dihapus.', 'success')
    return redirect(url_for('account'))

# @app.route('/edit_akun/<int:userid>', methods=['GET', 'POST'])
def edit_akun(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT userid, namalengkap, username, password, hakakses FROM pengguna WHERE userid = %s", (user_id,))
    result = cursor.fetchone()

    if request.method == 'POST':
        namalengkap = request.form['namalengkap']
        username = request.form['username']
        password = request.form['password']
        hakakses = request.form['hakakses']

        cursor.execute(
            "UPDATE pengguna SET namalengkap = %s, username = %s, password = %s, hakakses = %s WHERE userid = %s",
            (namalengkap, username, password, hakakses, user_id)
        )
        conn.commit()
        cursor.close()
        return redirect(url_for('account'))
    
    # Ambil data produk
    cursor.execute("SELECT * FROM pengguna WHERE userid = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    # Bentuk dictionary dari result
    akun = {
        'userid': result[0],
        'namalengkap': result[1],
        'username': result[2],
        'password': result[3],
        'hakakses': result[4]
    }

    cursor.close()
    return render_template('Editakun.html', akun=akun)