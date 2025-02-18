from flask import Flask, render_template, request, jsonify
from Page.login import get_db

app = Flask(__name__)

conn = get_db()

# @app.route('/member', methods=['GET'])
def member():
    cursor = conn.cursor()
    cursor.execute("SELECT pelangganid, namapelanggan, alamat, nomortelepon FROM pelanggan")
    member_list = cursor.fetchall()
    cursor.close()

    return render_template('Memberpage.html', member_list=member_list)

if __name__ == '__main__':
    app.run(debug=True)