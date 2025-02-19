from flask import Flask, render_template, request, jsonify, send_file, make_response
from Page.login import get_db  # Fungsi koneksi ke database
import locale
import pdfkit
import os

app = Flask(__name__)

# Set locale to Indonesian Rupiah
locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

# Custom filter to format currency
@app.template_filter('currency')
def currency_filter(value):
    return locale.currency(value, grouping=True)

# Koneksi ke PostgreSQL
conn = get_db()

@app.route('/penjualan', methods=['GET'])
def detail_penjualan():
    # Ambil data dari tabel penjualan dan pelanggan
    cursor = conn.cursor()
    query = """
    SELECT p.penjualanid, pl.namapelanggan, p.tanggalpenjualan, p.totalharga
    FROM penjualan p
    JOIN pelanggan pl ON p.pelangganid = pl.pelangganid
    """
    cursor.execute(query)
    penjualan_list = cursor.fetchall()
    cursor.close()

    # Render template dengan data penjualan
    return render_template('DetailPenjualanpage.html', penjualan_list=penjualan_list)

@app.route('/detailjual/<int:penjualan_id>', methods=['GET'])
def detail_jual(penjualan_id):
    cursor = conn.cursor()
    query = """
    SELECT p.penjualanid, pl.namapelanggan, p.tanggalpenjualan, p.totalharga
    FROM penjualan p
    JOIN pelanggan pl ON p.pelangganid = pl.pelangganid
    WHERE p.penjualanid = %s
    """
    cursor.execute(query, (penjualan_id,))
    detail = cursor.fetchone()

    query_detail = """
    SELECT dp.detailid, pr.namaproduk, pr.harga * dp.jumlahproduk AS total_harga, dp.jumlahproduk
    FROM detailpenjualan dp
    JOIN produk pr ON dp.produkid = pr.produkid
    WHERE dp.penjualanid = %s
    """
    cursor.execute(query_detail, (penjualan_id,))
    detail_produk_list = cursor.fetchall()
    cursor.close()

    return render_template('Detailjualpage.html', detail=detail, detail_produk_list=detail_produk_list)

@app.route('/unduh_pdf/<int:penjualan_id>', methods=['GET'])
def unduh_pdf(penjualan_id):
    cursor = conn.cursor()
    query = """
    SELECT p.penjualanid, pl.namapelanggan, p.tanggalpenjualan, p.totalharga
    FROM penjualan p
    JOIN pelanggan pl ON p.pelangganid = pl.pelangganid
    WHERE p.penjualanid = %s
    """
    cursor.execute(query, (penjualan_id,))
    detail = cursor.fetchone()

    query_detail = """
    SELECT dp.detailid, pr.namaproduk, pr.harga * dp.jumlahproduk AS total_harga, dp.jumlahproduk
    FROM detailpenjualan dp
    JOIN produk pr ON dp.produkid = pr.produkid
    WHERE dp.penjualanid = %s
    """
    cursor.execute(query_detail, (penjualan_id,))
    detail_produk_list = cursor.fetchall()
    cursor.close()

    rendered = render_template('Detailjualpage.html', detail=detail, detail_produk_list=detail_produk_list)
    pdf = pdfkit.from_string(rendered, False)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=penjualan_{penjualan_id}.pdf'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
