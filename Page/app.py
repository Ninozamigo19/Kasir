from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from Page.login import get_db
from datetime import date

app = Flask(__name__)
app.secret_key = "secret_key"

# Koneksi ke PostgreSQL
conn = get_db()

@app.route('/jual', methods=['POST'])
def transaksi():
    if request.is_json:
        data = request.get_json()
        items = data.get('items', [])
        pelangganid = data.get('pelangganid')
        userid = data.get('userid')
        totalharga = data.get('totalharga')

        try:
            cursor = conn.cursor()
            # Insert data transaksi ke tabel "penjualan"
            query = """
                INSERT INTO penjualan (tanggalpenjualan, totalharga, pelangganid, userid)
                VALUES (%s, %s, %s, %s) RETURNING penjualanid
            """
            cursor.execute(query, (date.today(), totalharga, pelangganid, userid))
            penjualanid = cursor.fetchone()[0]

            # Insert detail penjualan dan update stok produk
            for item in items:
                namaBarang = item['namaBarang']
                jumlah = item['jumlah']

                # Ambil produkid berdasarkan namaBarang
                cursor.execute("SELECT produkid FROM produk WHERE namaproduk = %s", (namaBarang,))
                produkid = cursor.fetchone()[0]

                # Insert ke detail penjualan
                query = """
                    INSERT INTO detail_penjualan (penjualanid, produkid, jumlah)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (penjualanid, produkid, jumlah))

                # Update stok produk
                query = "UPDATE produk SET stok = stok - %s WHERE produkid = %s"
                cursor.execute(query, (jumlah, produkid))

            conn.commit()
            return jsonify({"message": "Transaksi berhasil disimpan!"})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)})
        finally:
            cursor.close()
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

@app.route('/transaksi', methods=['GET'])
def penjualan():
    # Ambil data pelanggan dan pengguna untuk dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT pelangganid, namapelanggan FROM pelanggan")
    pelanggan_list = cursor.fetchall()

    cursor.execute("SELECT userid, namalengkap FROM pengguna")
    pengguna_list = cursor.fetchall()

    cursor.execute("SELECT produkid, namaproduk, harga, stok FROM produk")
    produk_list = cursor.fetchall()
    cursor.close()

    return render_template('Transaksipage.html', pelanggan_list=pelanggan_list, pengguna_list=pengguna_list, produk_list=produk_list)

if __name__ == '__main__':
    app.run(debug=True)
