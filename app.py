from flask import Flask, render_template, redirect, request, url_for, session, jsonify

import os
import pymysql
import bcrypt

app = Flask(__name__)


app.secret_key = os.urandom(24)  # Atur kunci sesi yang aman

# config
db = pymysql.connect(
    host="localhost",
    user="root",
    password="R4hm4d1$",
    database="sic-biona"
)

@app.before_request
def check_login():
    # Daftar halaman yang dapat diakses ketika belum login
    allowed_endpoints = ['login', 'register']

    # Jika pengguna belum login dan bukan di halaman yang diizinkan, arahkan ke halaman login
    if 'user_id' not in session and request.endpoint not in allowed_endpoints:
        return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT saldo FROM tb_users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            if user:
                saldo = user['saldo']
                return render_template('index.html', saldo=saldo)
    
    return render_template('index.html')
    

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/set_scanned_session', methods=['POST'])
def set_scanned_session():
    content = request.json.get('content')
    if content == 'BIONA':
        session['scanned'] = True
        session['scanned_content'] = content
        return jsonify(message="Scanned session set to True")
    else:
        return jsonify(message="Invalid scanned content")
    
@app.route('/data')
def data():
    if session.get('scanned'):
        if session.get('scanned_content') == 'BIONA':
            return render_template('data.html', content=session.get('scanned_content'))
        else:
            return redirect('/scan')
    else:
        return redirect('/scan')

@app.route('/end_session')
def end_session():
    if 'scanned' in session:
        session.pop('scanned', None)
        session.pop('scanned_content', None)  # Menghapus konten juga
        return jsonify(message="Session ended")
    else:
        return jsonify(message="No session to end")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        role = "user"
        saldo = "0"
        konfirm_password = request.form.get('konfirm_password')
        # Check if email already exists in the database
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM tb_users WHERE email = %s", (email,))
            cekEmail = cursor.fetchone()
            if cekEmail:  
                return render_template('auth/register.html', email_error=True)
  
        if password != konfirm_password:
            return render_template('auth/register.html', password_error=True)
        else:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("INSERT INTO tb_users (email, username, password, role, saldo) values (%s,%s, %s,%s, %s)", (email, username, password_hash, role, saldo))
                db.commit()
                return redirect('/register?success=1')  # Redirect with success parameter
            
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if email exists in the database
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM tb_users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                return render_template('auth/login.html', email_error=True)
            else:
                hashed_password = user['password'].encode('utf-8')  # Encode hashed password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    session['user_id'] = user['id']  # Store user ID in session
                    session['username'] = user['username']  # Store username in session
                    session['role'] = user['role']  # Store username in session
                    session['saldo'] = user['saldo']  # Store username in session
                    return redirect('/?success=1')
                else:
                    return render_template('auth/login.html', password_error=True)

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    # Hapus data sesi
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('role', None)
    session.pop('saldo', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
