from model.usuario_ad import UsuarioAD
from db.database import get_connection, get_connection_linx
from typing import Dict
import datetime


def buscar_status_linx(login: str):
    login_linx = f"LELIS\\{login}".lower()

    conn = get_connection_linx()
    if not conn:
        return None

    cursor = conn.cursor()
    cursor.execute("""
        SELECT inativo
        FROM USERS
        WHERE LOWER(lx_system_user) = ?
    """, (login_linx,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return None

    # Retorna 0 (ativo) ou 1 (inativo)
    return 0 if row[0] == 1 else 1


def atualizar_status_linx(login: str, conta_ativa: bool):
    """Desativa usuário no Linx APENAS se conta_ativa = 0"""
    if conta_ativa:
        return False
    
    login_linx = f"LELIS\\{login}".lower()
    
    conn = get_connection_linx()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE USERS
        SET inativo = 1
        WHERE LOWER(lx_system_user) = ?
    """, (login_linx,))
    
    rows_afetadas = cursor.rowcount
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return rows_afetadas > 0


def importar_usuarios_ad(usuarios_ad: Dict[str, UsuarioAD]):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, login, nome, email, matricula, cpf, cargo,
            departamento, gestor, conta_ativa, senha_nunca_expira,
            senha_expira_em, dias_para_expirar, data_atualizacao, linx
        FROM usuarios_ad
    """)

    rows = cursor.fetchall()
    usuarios_db = {row[1]: row for row in rows}
    logins_existentes = set(usuarios_db.keys())
    logins_atuais = set(usuarios_ad.keys())
    logins_desligados = logins_existentes - logins_atuais

    contador = 0

    # Mover desligados
    for login in logins_desligados:
        dados = usuarios_db.get(login)
        if dados:
            cursor.execute(
                "DELETE FROM usuarios_desligados WHERE login = ?",
                (login,)
            )

            cursor.execute("""
                INSERT INTO usuarios_desligados (
                    login, nome, email, cargo, departamento, gestor, data_desligamento, matricula
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dados[1],  # login
                dados[2],  # nome
                dados[3],  # email
                dados[6],  # cargo
                dados[7],  # departamento
                dados[8],  # gestor
                datetime.datetime.now(),
                dados[4]   # matricula
            ))

            cursor.execute("DELETE FROM usuarios_ad WHERE login = ?", (login,))

            contador += 1
            if contador % 50 == 0:
                conn.commit()

    # Inserir / atualizar
    for login, usuario in usuarios_ad.items():
        status_linx = buscar_status_linx(login)
        row = usuarios_db.get(login)
        
        cpf_truncado = usuario.cpf[:10] if usuario.cpf and len(usuario.cpf) > 10 else usuario.cpf

        if not row:
            cursor.execute("""
                INSERT INTO usuarios_ad (
                    login, nome, email, matricula, cpf, cargo, departamento, gestor, conta_ativa,
                    senha_nunca_expira, senha_expira_em, dias_para_expirar, linx
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                usuario.login, usuario.nome, usuario.email, usuario.matricula,
                cpf_truncado, usuario.cargo, usuario.departamento, usuario.gestor,
                usuario.conta_ativa, usuario.senha_nunca_expira, usuario.senha_expira_em,
                usuario.dias_restantes, status_linx
            ))
        else:
            (
                _id, _login, nome_db, email_db, matricula_db, cpf_db,
                cargo_db, dep_db, gestor_db, ativa_db,
                senha_nunca_db, expira_em_db, dias_db,
                data_atualizacao, linx_db
            ) = row

            if (
                usuario.nome != nome_db or
                usuario.email != email_db or
                usuario.matricula != matricula_db or
                cpf_truncado != cpf_db or
                usuario.cargo != cargo_db or
                usuario.departamento != dep_db or
                usuario.gestor != gestor_db or
                usuario.conta_ativa != ativa_db or
                usuario.senha_nunca_expira != senha_nunca_db or
                usuario.senha_expira_em != expira_em_db or
                usuario.dias_restantes != dias_db or
                status_linx != linx_db
            ):
                # Desativa no Linx se conta inativa no AD mas ativa no Linx
                if (usuario.conta_ativa == 0 or usuario.conta_ativa == False) and (status_linx == 1 or status_linx == True):
                    desativou = atualizar_status_linx(login, usuario.conta_ativa)
                    if desativou:
                        status_linx = 0

                cursor.execute("""
                    UPDATE usuarios_ad SET
                        nome = ?, email = ?, matricula = ?, cpf = ?, cargo = ?, departamento = ?, gestor = ?,
                        conta_ativa = ?, senha_nunca_expira = ?, senha_expira_em = ?, dias_para_expirar = ?,
                        linx = ?, data_atualizacao = GETDATE()
                    WHERE login = ?
                """, (
                    usuario.nome, usuario.email, usuario.matricula, cpf_truncado,
                    usuario.cargo, usuario.departamento, usuario.gestor,
                    usuario.conta_ativa, usuario.senha_nunca_expira, usuario.senha_expira_em,
                    usuario.dias_restantes, status_linx, usuario.login
                ))

        contador += 1
        if contador % 50 == 0:
            conn.commit()

    conn.commit()
    cursor.close()
    conn.close()
