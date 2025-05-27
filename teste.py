#!/usr/bin/env python3
import os
import sys
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

def download_mp3(url: str, dest: str) -> None:
    """
    Faz download do melhor áudio e converte para .mp3 usando FFmpeg.
    """
    # opções do yt_dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(dest, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,           
        'noprogress': False,      
        'ignoreerrors': False,
        'nopart': True,           
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except DownloadError as e:
        print(f"\n[!] Falha no download/conversão: {e}")
        sys.exit(1)

def main():
    url = input("▶︎ URL do vídeo YouTube: ").strip()
    if not url:
        print("[!] URL vazia. Abortando.")
        sys.exit(1)

    dest = input("▶︎ Pasta de destino (vazio = atual): ").strip() or '.'
    if not os.path.isdir(dest):
        print(f"[!] '{dest}' não é uma pasta válida.")
        sys.exit(1)

    print("\n[i] Iniciando download e conversão...\n")
    download_mp3(url, dest)
    print("\n✅ Concluído! Confira o arquivo .mp3 em:", os.path.abspath(dest))

if __name__ == "__main__":
    main()
