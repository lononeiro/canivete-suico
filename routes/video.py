# video.py
import os
import uuid
from flask import (
    Blueprint, render_template, request, send_file, jsonify
)
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from scriptsPython.apagarArquivos import apagarArquivosAntigos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '..', 'downloads'))
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

videoRoute = Blueprint('video', __name__)

@videoRoute.route('/', methods=['GET'])
def home():
    return render_template('baixarSite.html')

@videoRoute.route('/download', methods=['GET'])
def download():

    apagarArquivosAntigos(DOWNLOAD_FOLDER, minutos=5)

    url = request.args.get('url', '').strip()
    if not url:
        return jsonify({'error': 'URL vazia'}), 400

    try:
        print(f"Baixando: {url}")
        mp3_path, filename = download_mp3_ytdlp(url, DOWNLOAD_FOLDER)
        print(f"Download OK: {mp3_path}")
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

    return send_file(
        mp3_path,
        as_attachment=True,
        download_name=filename,
        mimetype='application/octet-stream',
        max_age=0
    )

def download_mp3_ytdlp(url: str, dest: str):
    unique_id = str(uuid.uuid4())[:8]
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(dest, f'{unique_id}_%(title)s.%(ext)s'),
        'quiet': True,
        'noprogress': True,
        'ignoreerrors': False,
        'nopart': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
        except DownloadError as e:
            raise Exception(f'Erro ao baixar vídeo: {e}')

    # Busca o caminho real do arquivo baixado
    file_path = None
    if 'requested_downloads' in info and info['requested_downloads']:
        file_path = info['requested_downloads'][0].get('filepath')
    if not file_path or not os.path.isfile(file_path):
        # fallback para o nome padrão
        title = info.get('title', 'audio')
        ext = info.get('ext', 'webm')
        filename = f"{unique_id}_{title}.{ext}"
        file_path = os.path.join(dest, filename)
        if not os.path.isfile(file_path):
            raise Exception('Download falhou ou arquivo não encontrado.')
    else:
        filename = os.path.basename(file_path)

    return file_path, filename
