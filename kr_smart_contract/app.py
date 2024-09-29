import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import chardet

# Configuração do MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['file_db']
files_collection = db['files']
metadata_collection = db['metadata']

# Função para detectar a codificação do arquivo
def detect_encoding(content):
    result = chardet.detect(content)
    return result['encoding']

# Função para carregar arquivos
def upload_file():
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["txt", "pdf", "docx", "json", "xml", "csv"])
    if uploaded_file is not None:
        content = uploaded_file.read()
        st.session_state.file_content = content

        # Tente detectar a codificação e decodificar
        encoding = detect_encoding(content)
        try:
            decoded_content = content.decode(encoding)
            st.write("Conteúdo do arquivo:")
            st.text(decoded_content)
        except (UnicodeDecodeError, TypeError):
            st.warning(f"Não foi possível decodificar o arquivo com codificação {encoding}. Mostrando bytes brutos:")
            decoded_content = content

        # Permitir download do arquivo original
        st.download_button("Baixar Arquivo Original", content, file_name=uploaded_file.name)

# Função para salvar o arquivo no MongoDB
def save_to_mongodb(filename, content):
    # Salvar o arquivo binário na coleção 'files'
    file_id = files_collection.insert_one({
        'filename': filename,
        'content': content
    }).inserted_id
    
    # Salvar os metadados na coleção 'metadata'
    metadata_collection.insert_one({
        'filename': filename,
        'file_id': file_id,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    })
    st.success("Arquivo salvo com sucesso!")

# Função para listar arquivos
def list_files():
    # Buscar metadados dos arquivos
    files = list(metadata_collection.find({}))
    df = pd.DataFrame(files)
    st.write(df)

# Interface do Streamlit
st.sidebar.title("Navegação")
option = st.sidebar.selectbox("Escolha uma opção", ["Upload", "Meus Arquivos"])

if option == "Upload":
    st.title("Upload de Arquivo")
    upload_file()

    if st.button("Salvar Arquivo"):
        content = st.session_state.get('file_content', b'')
        filename = "nome_do_arquivo.txt"  # Modifique conforme necessário
        save_to_mongodb(filename, content)

elif option == "Meus Arquivos":
    st.title("Meus Arquivos")
    list_files()
