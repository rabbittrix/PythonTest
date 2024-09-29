import os
import json
import requests
import streamlit as st
import pyrebase
from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o Pyrebase
firebase = pyrebase.initialize_app(
    json.load(open("./api-tippay-firebase-adminsdk.json")))
auth = firebase.auth()

# Carregar variáveis de ambiente do TipPay
TIPPAY_CLIENT_ID = os.getenv('TIPPAY_CLIENT_ID')
TIPPAY_SECRET = os.getenv('TIPPAY_SECRET')

# Funções de integração com TipPay (mantidas como estão)


def create_link_token():
    url = "https://sandbox.tippay.com/link/token/create"
    headers = {"Content-Type": "application/json"}
    body = {
        "client_id": TIPPAY_CLIENT_ID,
        "secret": TIPPAY_SECRET,
        "user": {"client_user_id": "user-id"},
        "client_name": "TipPay",
        "products": ["auth"],
        "country_codes": ["US"],
        "language": "en",
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()


def exchange_public_token(public_token):
    url = "https://sandbox.tippay.com/item/public_token/exchange"
    headers = {"Content-Type": "application/json"}
    body = {
        "client_id": TIPPAY_CLIENT_ID,
        "secret": TIPPAY_SECRET,
        "public_token": public_token,
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()


def get_account_info(access_token):
    url = "https://sandbox.tippay.com/auth/get"
    headers = {"Content-Type": "application/json"}
    body = {
        "client_id": TIPPAY_CLIENT_ID,
        "secret": TIPPAY_SECRET,
        "access_token": access_token,
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()


def save_to_firestore(data):
    firebase = pyrebase.initialize_app(
        json.load(open("./api-tippay-firebase-adminsdk.json")))
    db = firebase.database()
    db.collection("bank_accounts").add(data)


# Interface do usuário com Streamlit
st.title("Dashboard TipPay & Firebase")

st.sidebar.title("Navegação")
options = st.sidebar.selectbox("Selecione uma opção", [
                               "Criar Item", "Visualizar Dados", "Autenticação"])

if options == "Criar Item":
    st.header("Criar Novo Item (Conta Bancária)")
    # Integre com a API do TipPay aqui

elif options == "Visualizar Dados":
    st.header("Visualizar Dados Bancários")
    # Exiba dados armazenados no Fire

elif options == "Autenticação":
    st.header("Autenticação Firebase")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    # Layout de colunas para botões
    col1, col2 = st.columns(2)

with col1:
    if st.button("Cadastrar"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("Usuário cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao cadastrar usuário: {e}")

with col2:
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Usuário logado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao logar usuário: {e}")

# Adicionando um botão de logout no final da barra lateral
if st.sidebar.button("Logout"):
    try:
        auth.current_user = None
        st.sidebar.success("Logout realizado com sucesso!")
    except Exception as e:
        st.sidebar.error(f"Erro ao fazer logout: {e}")
