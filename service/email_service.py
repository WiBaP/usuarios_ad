import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL = ""
SENHA = ""

def enviar_email(destinatario, assunto, mensagem_html, anexo_path=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = destinatario
        msg["Subject"] = assunto

        msg.attach(MIMEText(mensagem_html, "html"))

        if anexo_path:
            caminho = Path(anexo_path)
            with open(caminho, "rb") as f:
                anexo = MIMEApplication(f.read(), _subtype="pdf")
                anexo.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=caminho.name
                )
                msg.attach(anexo)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, SENHA)
            server.send_message(msg)

        return True

    except Exception as e:
        print("Erro ao enviar email:", e)
        return False
