from flask import Flask, render_template, request, redirect, url_for, flash
from Page.login import get_db
from datetime import date

app = Flask(__name__)
app.secret_key = "secret_key"

# Koneksi ke PostgreSQL
conn = get_db()

# @app.route('/transaksi', methods=['GET', 'POST'])
def transaksi():
    if request.method == 'POST':
        # Ambil data dari form
        pelangganid = request.form['pelangganid']
        userid = request.form['userid']
        totalharga = request.form['totalharga']

        # Insert data transaksi ke tabel "penjualan"
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO penjualan (tanggalpenjualan, totalharga, pelangganid, userid)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (date.today(), totalharga, pelangganid, userid))
            conn.commit()
            flash("Transaksi berhasil disimpan!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            cursor.close()

        return redirect(url_for('jual'))

    # Ambil data pelanggan dan pengguna untuk dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT pelangganid, namapelanggan FROM pelanggan")
    pelanggan_list = cursor.fetchall()

    cursor.execute("SELECT userid, namalengkap FROM pengguna")
    pengguna_list = cursor.fetchall()
    cursor.close()

     # Ambil data produk dari tabel "produk"
    cursor = conn.cursor()
    cursor.execute("SELECT produkid, namaproduk, harga, stok FROM produk")
    produk_list = cursor.fetchall()
    cursor.close()

    return render_template('Transaksipage.html', pelanggan_list=pelanggan_list, pengguna_list=pengguna_list, produk_list=produk_list)

if __name__ == '__main__':
    app.run(debug=True)
