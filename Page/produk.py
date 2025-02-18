from flask import Flask, render_template, request, jsonify
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

keranjang = []

# @app.route('/tambah_keranjang', methods=['POST'])
def tambah_ke_keranjang(produk_list):
    data = request.json
    produk_id = data.get("produk_id")
    jumlah = data.get("jumlah", 1)

    # Cari produk berdasarkan ID
    produk = next((p for p in produk_list if p["id"] == produk_id), None)

    if not produk:
        return jsonify({"error": "Produk tidak ditemukan"}), 404

    # Cek stok
    if produk["stok"] < jumlah:
        return jsonify({"error": "Stok tidak mencukupi"}), 400

    # Tambahkan barang ke keranjang (jika sudah ada, tambahkan jumlahnya)
    item_keranjang = next((item for item in keranjang if item["id"] == produk_id), None)
    if item_keranjang:
        if item_keranjang["jumlah"] + jumlah > produk["stok"]:
            return jsonify({"error": "Stok tidak mencukupi"}), 400
        item_keranjang["jumlah"] += jumlah
    else:
        keranjang.append({"id": produk_id, "nama": produk["nama"], "harga": produk["harga"], "jumlah": jumlah})

    # Kurangi stok produk
    produk["stok"] -= jumlah

    return jsonify({"message": "Barang ditambahkan ke keranjang", "keranjang": keranjang})

if __name__ == '__main__':
    app.run(debug=True)
