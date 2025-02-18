from flask import Flask, request, redirect, url_for, flash, render_template

from Page.login import get_db
app = Flask(__name__)
app.secret_key = 'SECRET_KEY'  # Ganti dengan kunci rahasia Anda

# Route Signup
# @app.route('/signup', methods=['GET', 'POST'])
def addmember():
    if request.method == 'POST':
        nama = request.form['namapelanggan']
        alamat = request.form['alamat']
        notlp = request.form['notlp']

        # Simpan user ke database
        try:
            print(nama, alamat, notlp)
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pelanggan (namapelanggan, alamat, nomortelepon) VALUES (%s, %s, %s)", 
                (nama, alamat, notlp)
            )
            conn.commit()
            cursor.close()
            conn.close()
            # flash('Signup berhasil! Silakan login.', 'success')
            return redirect(url_for('pelanggan'))
        except Exception as e:
            print(e)
            # flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('addpelanggan'))

    return render_template('TambahMemberpage.html')  # Pastikan template ada
