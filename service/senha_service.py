from db.database import get_connection
from service.email_service import enviar_email
from datetime import date

def notificar_senhas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, dias_para_expirar, ultima_notificacao_senha
        FROM usuarios_ad
        WHERE email IS NOT NULL
          AND (
                dias_para_expirar BETWEEN 1 AND 5
                OR dias_para_expirar <= 0
          )
    """)

    usuarios = cursor.fetchall()
    enviados = 0

    hoje = date.today()

    for u in usuarios:
        user_id, nome, email, dias, ultima = u

        # já notificou hoje? pula
        if ultima == hoje:
            continue

        if dias > 0:
            assunto = f"⚠️ Sua senha expira em {dias} dia(s)"
            html = f"""
                <h2>Olá {nome}</h2>
                <p>Sua senha expira em <b>{dias} dia(s)</b>.</p>
                <p>Troque sua senha antes do vencimento para evitar bloqueio.</p>
                <p><b>Para trocar segue o procedimento em anexo:</b><br>
                </p>
            """
        else:
            assunto = "❌ Sua senha expirou"
            html = f"""
                <h2>Olá {nome}</h2>
                <p><b>Sua senha expirou.</b></p>
                <p>Você precisa trocar sua senha imediatamente.</p>
                <p><b>Para trocar segue o procedimento em anexo:</b><br>
                </p>
            """

        if enviar_email(
                        email,
                        assunto,
                        html,
                        anexo_path=r"C:\Users\willian.pinho\Desktop\inventario_2\procedimento\procedimento_de_alteração_de_senha.pdf"
                    ):
                    
            cursor.execute("""
                UPDATE usuarios_ad
                SET ultima_notificacao_senha = GETDATE()
                WHERE id = ?
            """, (user_id,))
            enviados += 1

    conn.commit()
    cursor.close()
    conn.close()

    return enviados

def notificar_usuario(login: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, dias_para_expirar, ultima_notificacao_senha
        FROM usuarios_ad
        WHERE login = ?
    """, (login,))

    u = cursor.fetchone()
    if not u:
        return False

    user_id, nome, email, dias, ultima = u

    assunto = "Teste de notificação de senha"
    html = f"<h2>Olá {nome}</h2><p>Este é um email de teste. falta {dias} para expirar</p>"

    enviar_email(
        email,
        assunto,
        html,
        anexo_path="procedimento/procedimento_de_alteração_de_senha.pdf"
    )

    cursor.close()
    conn.close()
    return True

