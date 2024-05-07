import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email():
    # Configurações do servidor SMTP
    servidor_smtp = '92.204.212.160'
    porta_smtp = 465  # Porta para conexões TLS

    # Informações de login
    usuario = 'support@kr-so.com'
    senha = 'WZvOFHuCNK'

    # Configurações do e-mail
    remetente = usuario
    destinatario = 'rabbittrix@hotmail.com'
    assunto = 'Teste de E-mail'
    corpo = 'Este é um e-mail de teste enviado via Python.'

    # Criando o objeto MIMEMultipart
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    # Adicionando o corpo da mensagem
    mensagem.attach(MIMEText(corpo, 'plain'))

    # Criando uma conexão com o servidor SMTP
    try:
        with smtplib.SMTP(servidor_smtp, porta_smtp) as servidor_smtp:
            servidor_smtp.starttls()  # Inicia a conexão TLS
            servidor_smtp.login(usuario, senha)
            
            # Enviando o e-mail
            servidor_smtp.sendmail(remetente, destinatario, mensagem.as_string())
            print("E-mail enviado com sucesso!")
    except Exception as e:
        print("Falha ao enviar e-mail:", e)

if __name__ == '__main__':
    enviar_email()
