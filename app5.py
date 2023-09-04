from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from datetime import datetime
import os
import pymysql
import bcrypt

import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
from RPLCD import i2c
from time import sleep
from flask import Flask

app = Flask(__name__)

EMULATE_HX711 = False

referenceUnit = 1

if not EMULATE_HX711:
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

# Inisialisasi HX711
hx711 = HX711(5, 6)
hx711.set_reading_format("MSB", "MSB")
hx711.set_reference_unit(1)
hx711.reset()
hx711.tare()

# Inisialisasi driver LCD
lcd = i2c.CharLCD('PCF8574', 0x27)

# Konfigurasi pin GPIO untuk servo
servo_pin = 18  # Ganti dengan nomor pin GPIO yang sesuai
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Inisialisasi PWM (Pulse Width Modulation) untuk servo
pwm = GPIO.PWM(servo_pin, 50)  # Frekuensi PWM 50 Hz (umum untuk servo)
pwm.start(0)  # Awalnya servo berada di posisi awal (sudut 0 derajat)

def set_servo_angle(angle):
    duty_cycle = (angle / 18) + 2  # Menghitung duty cycle berdasarkan sudut (dalam derajat)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)  # Beri waktu servo untuk bergerak

try:
    while True:
        val = max(0, int(hx711.get_weight(5)))
        lcd.write_string("Berat: {} gram".format(val))
        sleep(2) # Tampilkan selam  # Hapus tampilan pada LCD
        
        lcd.clear()
        sleep(0.1)  # Jeda selama 1 detika 2 detik
        print(val)

        #if val > 5:
            #set_servo_angle(88)  # Jika berat di atas 5 gram, putar servo ke posisi tertentu
       # else:
            #set_servo_angle(-3)  # Jika berat di bawah atau sama dengan 5 gram, kembalikan servo ke posisi awal

        hx711.power_down()
        hx711.power_up()
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()


app.secret_key = os.urandom(24)  # Atur kunci sesi yang aman


UPLOAD_FOLDER = 'static/bukti_tf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# config
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Biona226",
    database="sic-biona"
)

# Validasi harus login

@app.before_request
def check_login():
    # Daftar halaman dan direktori yang dapat diakses ketika belum login
    allowed_endpoints = ['/', 'login', 'register', 'static']
    # Jika pengguna belum login dan bukan di halaman atau direktori yang diizinkan, arahkan ke halaman login
    if 'user_id' not in session and request.endpoint not in allowed_endpoints and not request.path.startswith('/static'):
        return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT saldo FROM tb_users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                saldo = user['saldo']
                # Mengambil semua data dari tabel tb_payment
                return render_template('index.html', saldo=saldo)

    return render_template('index.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/set_scanned_session', methods=['POST'])
def set_scanned_session():
    content = request.json.get('content')
    if content == 'biona':
        session['scanned'] = True
        session['scanned_content'] = content
        return jsonify(message="Scanned session set to True")
    else:
        return jsonify(message="Invalid scanned content")

@app.route('/data')
def data():
    if session.get('scanned'):
        if session.get('scanned_content') == 'biona':
            return render_template('data.html', content=session.get('scanned_content', berat=val))
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
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("INSERT INTO tb_users (email, username, password, role, saldo) values (%s,%s, %s,%s, %s)", (
                    email, username, password_hash, role, saldo))
                db.commit()
                # Redirect with success parameter
                return redirect('/register?success=1')
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
                hashed_password = user['password'].encode(
                    'utf-8')  # Encode hashed password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    session['user_id'] = user['id']  # Store user ID in session
                    # Store username in session
                    session['username'] = user['username']
                    session['role'] = user['role']  # Store username in session
                    # Store username in session
                    session['saldo'] = user['saldo']
                    # Store username in session
                    session['email'] = user['email']
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


@app.route('/tukar_saldo', methods=['GET', 'POST'])
def tukar_saldo():
    payment_method = request.args.get('payment')
    if 'user_id' in session:
        user_id = session['user_id']
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT saldo FROM tb_users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                saldo = user['saldo']
                if saldo < 10000:
                    # Contoh halaman notifikasi saldo tidak mencukupi
                    return render_template('index.html', saldo=saldo, _req=1)
                if payment_method in ['gopay', 'bca', 'mandiri']:
                    if request.method == 'POST':
                        payment = request.form.get('payment')
                        payment_gopay = request.form.get('payment_bca')
                        payment_gopay = request.form.get('payment_mandiri')
                        no_payment = request.form.get('no_payment')
                        email = request.form.get('email')
                        tanggal_transaksi = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        status = 'UNPAID'
                        bukti_pembayaran = 'UNPAID'

                        with db.cursor() as insert_cursor:
                            sql = "INSERT INTO tb_transaksi (email, payment, no_payment, nominal, tanggal_transaksi, status, bukti_pembayaran) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            insert_cursor.execute(
                                sql, (email, payment, no_payment, saldo, tanggal_transaksi, status, bukti_pembayaran))
                            # Operasi UPDATE
                            sql_update = "UPDATE tb_users SET saldo = 0 WHERE id = %s"
                            cursor.execute(sql_update, (user_id,))

                            db.commit()
                            return redirect(url_for('tukar_saldo', payment=payment_gopay, success_req=1))

                    return render_template('tukar_saldo.html', payment_method=payment_method, saldo=saldo)
                else:
                    return redirect(url_for('index', saldo=saldo))
    return render_template('index.html')

# DASHBOARD ADMIN


@app.route('/dashboard')
def dashboard():
    if 'role' in session and session['role'] == 'admin':
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM tb_transaksi")
            transaksi = cursor.fetchall()
        return render_template('admin/dashboard.html', transaksi = transaksi)
    else:
        return "404 NOT FOUND"

# Rute untuk halaman pembaruan
@app.route('/update_request/<int:id>')
def update_request(id):
   # Di sini Anda dapat mengambil data transaksi berdasarkan ID dari database
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM tb_transaksi WHERE id_transaksi = %s", (id,))
            transaksi = cursor.fetchone()
        
        # Selanjutnya, Anda dapat merender halaman pembaruan data dengan data yang sesuai
        return render_template('admin/update_request.html', transaksi=transaksi)

@app.route('/submit_update/<int:id>', methods=['POST'])
def submit_update(id):
    if 'user_id' in session:
        # Pastikan pengguna yang sedang masuk adalah admin atau pemilik transaksi
        user_id = session['user_id']
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT role FROM tb_users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user and (user['role'] == 'admin' or user_id == id):
                # Di sini Anda dapat mengambil data yang diperbarui dari formulir (request.form)
                # Contoh:
                updated_email = request.form.get('email')
                updated_payment = request.form.get('method')
                updated_no_payment = request.form.get('no_payment')
                updated_nominal = request.form.get('nominal')
                updated_tanggal_transaksi = request.form.get('tanggal_transaksi')
                updated_status = request.form.get('status')
                updated_bukti_tf = request.files['bukti_tf'] if 'bukti_tf' in request.files else None

                if updated_bukti_tf:
                    # Pastikan nama file unik, misalnya dengan menggunakan ID transaksi
                    filename = f"bukti_tf_{id}.jpg"  # Ganti dengan ekstensi file yang sesuai

                    # Simpan file di dalam folder bukti_tf
                    updated_bukti_tf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    # Selanjutnya, Anda dapat menyimpan nama file ini dalam database jika perlu.
                    # ...

                # Selanjutnya, lakukan pembaruan data dalam database berdasarkan ID yang diberikan
                with db.cursor() as update_cursor:
                    sql = "UPDATE tb_transaksi SET email = %s, payment = %s, no_payment = %s, nominal = %s, tanggal_transaksi = %s, status = %s, bukti_pembayaran = %s WHERE id_transaksi = %s"
                    update_cursor.execute(sql, (
                        updated_email, updated_payment, updated_no_payment, updated_nominal, updated_tanggal_transaksi, updated_status, filename, id))
                    db.commit()

                # Setelah pembaruan selesai, Anda dapat mengarahkan pengguna kembali ke halaman utama
                return redirect(url_for('dashboard', success_update=True))

    # Jika pengguna tidak memiliki izin atau tidak masuk, arahkan ke halaman utama
    return redirect(url_for('index'))

@app.route('/status_transaksi')
def status_transaksi():
    if 'email' in session:
        email = session['email']
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM tb_transaksi WHERE email = %s", (email))
            semua = cursor.fetchall()
            if email:
                semua_transaksi = semua
                # Mengambil semua data dari tabel tb_payment
                return render_template('status_transaksi.html', semua_transaksi=semua_transaksi)

    return render_template('index.html')

# ... (kode lainnya)
if __name__ == '__main__':
    app.run(debug=True)
