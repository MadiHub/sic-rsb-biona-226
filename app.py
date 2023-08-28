from flask import Flask, render_template, redirect, request, session, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Atur kunci sesi yang aman

@app.route('/')
def index():
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


if __name__ == '__main__':
    app.run(debug=True)
