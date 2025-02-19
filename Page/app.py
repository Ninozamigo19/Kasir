from flask import Flask, render_template, request, jsonify
from Page.login import get_db
from datetime import date
from decimal import Decimal, InvalidOperation
import locale

app = Flask(__name__)
app.secret_key = "secret_key"

# Set locale to Indonesian Rupiah
locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

# Custom filter to format currency
@app.template_filter('currency')
def currency_filter(value):
    return locale.currency(value, grouping=True)

# Koneksi ke PostgreSQL
conn = get_db()

@app.route('/transaksi', methods=['POST'])
def transaksi():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type. Please set it to application/json"}), 415
    
    data = request.get_json()
    pelanggan_id = data.get("pelangganId")
    user_id = data.get("userId")
    items = data.get("items")

    if not items:
        return jsonify({"error": "Keranjang kosong!"}), 400

    try:
        cursor = conn.cursor()
        totalharga = Decimal(0)
        for item in items:
            try:
                harga = Decimal(str(item['harga']).replace("Rp", "").replace(".", "").replace(",", ".")).quantize(Decimal('0.01'))
            except (InvalidOperation, TypeError):
                return jsonify({"error": "Invalid price format"}), 400
            jumlah = item['jumlah']
            totalharga += harga * jumlah

        cursor.execute("""
            INSERT INTO penjualan (pelangganid, userid, totalharga, tanggalpenjualan)
            VALUES (%s, %s, %s, NOW())
            RETURNING penjualanid
        """, (pelanggan_id, user_id, totalharga))
        penjualan_id = cursor.fetchone()[0]

        for item in items:
            try:
                harga = Decimal(str(item['harga']).replace("Rp", "").replace(".", "").replace(",", ".")).quantize(Decimal('0.01'))
            except (InvalidOperation, TypeError):
                return jsonify({"error": "Invalid price format"}), 400
            jumlah = item['jumlah']
            subtotal = harga * jumlah
            cursor.execute("""
                INSERT INTO detailpenjualan (penjualanid, produkid, jumlahproduk, subtotal)
                VALUES (%s, %s, %s, %s)
            """, (penjualan_id, item['productId'], jumlah, subtotal))
            
            # Update the product stock
            cursor.execute("""
                UPDATE produk
                SET stok = stok - %s
                WHERE produkid = %s
            """, (jumlah, item['productId']))

        conn.commit()
        cursor.close()
        return jsonify({"message": "Transaksi berhasil disimpan!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/transaksi', methods=['GET'])
def penjualan():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT pelangganid, namapelanggan FROM pelanggan")
        pelanggan_list = cursor.fetchall()

        cursor.execute("SELECT userid, namalengkap FROM pengguna")
        pengguna_list = cursor.fetchall()

        cursor.execute("SELECT produkid, namaproduk, harga, stok FROM produk")
        produk_list = cursor.fetchall()
        cursor.close()

        return render_template('Transaksipage.html', pelanggan_list=pelanggan_list, pengguna_list=pengguna_list, produk_list=produk_list)
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
