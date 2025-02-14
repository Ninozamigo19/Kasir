from flask import Flask, render_template, request, redirect, flash, url_for
from Page.login import get_db  # Fungsi koneksi database

app = Flask(__name__)
app.secret_key = "SECRET_KEY"  # Ganti dengan secret key yang aman

# Koneksi ke database
conn = get_db()

# Route untuk menampilkan form tambah produk
# @app.route('/tambah_produk', methods=['GET', 'POST'])
def addproduk():
    if request.method == 'POST':
        # Ambil data dari form
        namaproduk = request.form['namaproduk']
        harga = request.form['harga']
        stok = request.form['stok']

        # Insert data ke dalam tabel produk
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO produk (namaproduk, harga, stok)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (namaproduk, harga, stok))
            conn.commit()
            flash("Produk berhasil ditambahkan!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Terjadi kesalahan: {str(e)}", "danger")
        finally:
            cursor.close()

        return redirect(url_for('addbarang'))

    # Render form tambah produk
    return render_template('TambahProdukpage.html')


if __name__ == '__main__':
    app.run(debug=True)