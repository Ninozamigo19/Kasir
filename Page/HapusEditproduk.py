from flask import Flask, render_template, request, redirect, url_for, flash
from Page.login import get_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Koneksi ke database PostgreSQL
conn = get_db()

@app.route('/hapus_produk/<int:produk_id>', methods=['POST'])
def hapus_produk(produk_id):
    """Menghapus produk berdasarkan ID."""
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM produk WHERE produkid = %s", (produk_id,))
            conn.commit()
            flash("Produk berhasil dihapus!", "success")
    except Exception as e:
        conn.rollback()  # Tambahkan rollback di sini
        print(e)
        flash(f"Terjadi kesalahan saat menghapus produk: {e}", "danger")
    finally:
        conn.close()  # Pastikan koneksi ditutup
    return redirect(url_for('barang'))

def edit_produk(produk_id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Update data
        namaproduk = request.form['namaproduk']
        harga = request.form['harga']
        stok = request.form['stok']
        try:
            cursor.execute(
                "UPDATE produk SET namaproduk = %s, harga = %s, stok = %s WHERE produkid = %s",
                (namaproduk, harga, stok, produk_id)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()  # Tambahkan rollback di sini
            print(e)
            flash(f"Terjadi kesalahan saat mengedit produk: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('barang'))

    # Ambil data produk
    cursor.execute("SELECT * FROM produk WHERE produkid = %s", (produk_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    # Bentuk dictionary dari result
    produk = {
        'produkid': result[0],
        'namaproduk': result[1],
        'harga': result[2],
        'stok': result[3]
    }

    return render_template('EditProduk.html', produk=produk)

if __name__ == '__main__':
    app.run(debug=True)
