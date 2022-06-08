from firebase import Firebase
from fastapi import FastAPI
from docx2pdf import convert
import os

firebaseConfig = {
    'apiKey': "AIzaSyCyby5fV9slANxZGFRxYEUBPDLvtszO64k",
    'authDomain': "storage-jack.firebaseapp.com",
    'databaseURL': "gs://storage-jack.appspot.com",
    'projectId': "storage-jack",
    'storageBucket': "storage-jack.appspot.com",
    'messagingSenderId': "170234004997",
    'appId': "1:170234004997:web:44c0a627cb2fa415057e6c"
}

firebase = Firebase(firebaseConfig)

# configuração
storage = firebase.storage()

storage.child("word").download("downloaded.jpg")
app = FastAPI()


@app.get('/')
def home():
    return {'Olá'}


@app.post("/word-to-pdf/{name_id}")
async def docx_to_pdf(name_id):
    down = f"download/{name_id}"
    up = f"uploads/{name_id[:-5]}.pdf"

    # Baixa o arquivo para a pasta de download
    storage.child(f"{name_id}").download(down)

    # Modificando de DOCX para PDF
    convert(down, up)

    # Enviando para o servidor o arquivo modificado
    storage.child(up).put(up)

    # Pegando a URL do arquivo
    get_url = storage.child(up).get_url(None)

    # Removendo o lixo
    os. remove(down)
    os.remove(up)

    return {'link_download': get_url}
