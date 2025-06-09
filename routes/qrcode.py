# routes/qrcode.py
import io
import base64
import qrcode
from flask import Blueprint, render_template, request

qrcodeRoute = Blueprint('qrcode', __name__)

@qrcodeRoute.route('/qrcode', methods=['GET', 'POST'])
def generate_qrcode():
    img_data = None
    if request.method == 'POST':
        data = request.form['data']
        if not data:  # Verifique se o campo está vazio
            return render_template('geradorqrcode.html', img_data=None, error="Campo vazio!")

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Salvar a imagem em um objeto BytesIO
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Codificar a imagem em base64
        img_data = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return render_template('geradorqrcode.html', img_data=img_data)