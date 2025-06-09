from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', img_data=None)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form['data']
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Salvar a imagem em um objeto BytesIO
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Codificar a imagem em base64
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return render_template('index.html', img_data=img_base64)

if __name__ == '__main__':
    app.run(debug=True)