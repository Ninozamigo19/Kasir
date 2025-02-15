from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from decouple import config

from Page.app import transaksi
from Page.login import login
from Page.register import signup
from Page.produk import produk
from Page.TambahBarang import addproduk
from Page.HapusEditproduk import hapus_produk, edit_produk

app = Flask (__name__)
app.secret_key = config('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'] )
def signin ():
    return login()

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    resp = make_response(redirect(url_for('signin')))
    resp.delete_cookie('userid')  # Hapus cookie saat logout
    flash('You have been logged out.', 'info')
    return resp

# Home route (protected)
@app.route('/home')
def home():
    userid = request.cookies.get('userid')
    if not userid:
        flash('You must be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    return render_template('Homepage.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return signup()

@app.route('/transaksi', methods=['GET', 'POST'])
def jual():
    return transaksi()

@app.route('/produk', methods=['GET'])
def barang():
    return produk()

@app.route('/addproduk', methods=['GET', 'POST'])
def addbarang():
    return addproduk()

@app.route('/hapus_produk/<int:produk_id>', methods=['POST'])
def hapus(produk_id):
    return hapus_produk(produk_id)

@app.route('/edit_produk/<int:produk_id>', methods=['GET', 'POST'])
def edit(produk_id):
    return edit_produk(produk_id)

if __name__ == '__main__':
    app.run(debug=True)