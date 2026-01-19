from ldap3 import Server, Connection, ALL, SUBTREE
from datetime import datetime
from model.usuario_ad import UsuarioAD
from service.usuario_service import importar_usuarios_ad


def buscar_usuarios_ad() -> dict:
    # === Configuração do servidor AD ===
    servidor = Server('', get_info=ALL)
    usuario = ''
    senha = ''

    # === Conexão com o Active Directory ===
    try:
        conexao = Connection(servidor, user=usuario, password=senha, auto_bind=True)
        print("✅ Conectado ao AD com sucesso!")
    except Exception as e:
        print("❌ Erro ao conectar no AD:", e)
        return {}

    # === Configurações da busca ===
    base_dns = [
        'OU=',
        'OU=',
        'OU=',
        'OU='
    ]
    filtro = '(&(objectClass=user)(objectCategory=person))'
    atributos = [
    'sAMAccountName', 'displayName', 'mail', 'pwdLastSet', 'userAccountControl',
    'msDS-UserPasswordExpiryTimeComputed', 'title', 'department', 'manager',
    'description',
    'extensionAttribute1'
    ]


    usuarios_encontrados = []

    for base_dn in base_dns:
        conexao.search(
            search_base=base_dn,
            search_filter=filtro,
            attributes=atributos,
            search_scope=SUBTREE,
        )
        usuarios_encontrados.extend(conexao.entries)

    # Filtrar duplicados pelo login
    usuarios_unicos = {}
    for entry in usuarios_encontrados:
        login = entry.sAMAccountName.value
        if login not in usuarios_unicos:
            usuarios_unicos[login] = entry

    usuarios = {}

    for entry in usuarios_unicos.values():
        login = entry.sAMAccountName.value
        nome = entry.displayName.value
        email = entry.mail.value
        matricula = entry.description.value if 'description' in entry else None  # <- matrícula
        cpf = entry.extensionAttribute1.value if 'extensionAttribute1' in entry else None

        cargo = entry.title.value if 'title' in entry else None
        departamento = entry.department.value if 'department' in entry else None
        gestor_dn = entry.manager.value if 'manager' in entry else None

        # Extrai CN do gestor (login do gestor)
        gestor_login = None
        if gestor_dn:
            partes = [p.strip() for p in gestor_dn.split(',') if p.strip().startswith('CN=')]
            if partes:
                gestor_login = partes[0].replace('CN=', '')

        # Verifica se conta está desativada
        flags = int(entry.userAccountControl.value or 0)
        conta_ativa = not (flags & 0x0002)

        # Verifica se a senha nunca expira
        senha_nunca_expira = bool(flags & 0x10000)

        # Verifica expiração da senha
        expira_em = None
        dias_restantes = None
        if not senha_nunca_expira and 'msDS-UserPasswordExpiryTimeComputed' in entry:
            raw_exp = entry['msDS-UserPasswordExpiryTimeComputed'].value
            if raw_exp:
                expira_em = datetime.fromtimestamp(int(raw_exp) / 10**7 - 11644473600)
                dias_restantes = (expira_em - datetime.now()).days

        usuario_ad = UsuarioAD(
            login,
            nome,
            email,
            cargo,
            departamento,
            gestor_login,
            conta_ativa,
            senha_nunca_expira,
            expira_em,
            dias_restantes,
            matricula,
            cpf
        )


        usuarios[login] = usuario_ad

    # Chama o service para sincronizar banco com o dicionário usuarios
    importar_usuarios_ad(usuarios)

    return {"mensagem": f"{len(usuarios)} usuários importados e sincronizados com sucesso do Active Directory"}
