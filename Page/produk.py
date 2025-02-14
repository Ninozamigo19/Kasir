from flask import Flask, render_template
from Page.login import get_db  # Fungsi koneksi ke database

app = Flask(__name__)

# Koneksi ke PostgreSQL
conn = get_db()

# @app.route('/produk', methods=['GET'])
def produk():
    # Ambil data produk dari tabel "produk"
    cursor = conn.cursor()
    cursor.execute("SELECT produkid, namaproduk, harga, stok FROM produk")
    produk_list = cursor.fetchall()
    cursor.close()

    # Render template dengan data produk
    return render_template('Produkpage.html', produk_list=produk_list)

if __name__ == '__main__':
    app.run(debug=True)
