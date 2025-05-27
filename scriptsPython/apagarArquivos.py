import os 
import time

def apagarArquivosAntigos(pasta: str, minutos: int):
    """
    Apaga arquivos antigos em uma pasta com base no tempo de modificação.
    
    :param pasta: Caminho da pasta onde os arquivos serão verificados.
    :param minutos: Tempo em minutos para considerar um arquivo como antigo.
    """
    agora = time.time()
    for root, dirs, files in os.walk(pasta):
        for file in files:
            caminho_arquivo = os.path.join(root, file)
            if os.path.isfile(caminho_arquivo):
                tempo_modificacao = os.path.getmtime(caminho_arquivo)
                idade_em_minutos = (agora - tempo_modificacao) / 60
                # Só apaga se a idade for maior que o parâmetro
                if idade_em_minutos > minutos:
                    try:
                        os.remove(caminho_arquivo)
                        print(f"Arquivo apagado: {caminho_arquivo}")
                    except Exception as e:
                        print(f"Erro ao apagar {caminho_arquivo}: {e}")
