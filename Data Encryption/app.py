from flask import Flask,redirect,url_for,render_template,request
from cryptography.fernet import Fernet
import qrcode
import socket

def generate_qr_code(text, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    image.save(filename)

def send___m(message, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        sock.sendall(message)
    finally:
        sock.close()

def receive_message(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", port))
    sock.listen(1)
    conn, addr = sock.accept()
    try:
        data = conn.recv(1024).decode()
        return data
    finally:
        conn.close()


app=Flask(__name__)
key = Fernet.generate_key()
f = Fernet(key)
generate_qr_code(key, 'static\qrcode.png')


@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/send',methods=['POST','GET'])
def send():
    global encrypted_data
    global message
    message=''
    if request.method =='POST':
        message=(request.form['Welcome to The world of privacy'])
        abc=bytes(message,'utf-8')
        encrypted_data = f.encrypt(abc)
    return render_template('selection.html')

@app.route('/key', methods=['POST','GET']) 
def key():   
 text_to_encode = key
 output_filename = "static/qrcode.png"
 generate_qr_code(text_to_encode, output_filename)
 return render_template('key.html', key=key)

@app.route('/qrcode1', methods=['POST','GET'])
def qrcode1():
    return render_template('cachy.html', image_url="static\qrcode.png")

@app.route('/encrypted_message', methods=['POST','GET'])
def encrypted_message():
    return render_template('encryption.html', encrypted_data = encrypted_data)

@app.route('/decrypted_message', methods=['POST','GET'])
def decrypted_message():
    decrypted_data = f.decrypt(encrypted_data)
    ab = decrypted_data.decode()
    return render_template('decryption.html', ab=ab)

@app.route('/send_message', methods=['POST','GET'])
def send_message():
    return render_template('send_message.html')

@app.route('/message_sent', methods=['POST','GET'])
def message_sent():
    message=''
    if request.method =='POST':
        message=(request.form['Welcome'])
        age = encrypted_data
        port = 12345
        send___m(age,message,port)
    return render_template('message_sent.html')

@app.route('/omessage', methods=['POST','GET'])
def omessage():
    return render_template('send_message1.html')

@app.route('/message_sent1', methods=['POST','GET'])
def message_sent1():
    message1=''
    if request.method =='POST':
        message1=(request.form['Welcome'])
        age = message.encode('utf-8')
        port = 12345
        send___m(age,message1,port)
    return render_template('message_sent.html')


if __name__=='__main__':
     app.run(debug=True)