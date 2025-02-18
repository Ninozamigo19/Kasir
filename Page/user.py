from flask import Flask, render_template
from Page.login import get_db

app = Flask(__name__)

conn = get_db()

# @app.route('/akun', methods=['GET'])
def akun():
    cursor = conn.cursor()
    cursor.execute("SELECT userid, namalengkap, username, password, hakakses FROM pengguna")
    akun_list = cursor.fetchall()
    cursor.close()

    return render_template('Akunpage.html', akun_list=akun_list)

if __name__ == '__main__':
    app.run(debug=True)