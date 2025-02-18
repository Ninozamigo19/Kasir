from flask import Flask, render_template, request, redirect, url_for
from Page.login import get_db

app = Flask(__name__)

conn = get_db()

# @app.route('/hapus_pelanggan/<int:userid>', methods=['POST'])
def hapus_pelanggan(member_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pelangan WHERE pelangganid = %s", (member_id,))
    conn.commit()
    cursor.close()

    # flash('Akun berhasil dihapus.', 'success')
    return redirect(url_for('pelanggan'))

# @app.route('/edit_pelanggan/<int:userid>', methods=['GET', 'POST'])
def edit_pelanggan(member_id):
    cursor = conn.cursor()
    cursor.execute("SELECT pelangganid, namapelanggan, alamat, nomortelepon FROM pelanggan WHERE pelangganid = %s", (member_id,))
    result = cursor.fetchone()

    if request.method == 'POST':
        namapelanggan = request.form['namapelanggan']
        alamat = request.form['alamat']
        notlp = request.form['notlp']

        cursor.execute(
            "UPDATE pelanggan SET namapelanggan= %s, alamat = %s, nomortelepon= %s WHERE pelangganid = %s",
            (namapelanggan, alamat, notlp, member_id)
        )
        conn.commit()
        cursor.close()
        return redirect(url_for('pelanggan'))
    
    # Ambil data produk
    cursor.execute("SELECT * FROM pelanggan WHERE pelangganid = %s", (member_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    # Bentuk dictionary dari result
    pelanggan = {
        'pelangganid': result[0],
        'namapelanggan': result[1],
        'alamat': result[2],
        'nomortelepon': result[3]
    }

    cursor.close()
    return render_template('EditPelangganpage.html', pelanggan=pelanggan)