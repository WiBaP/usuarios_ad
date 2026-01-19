class UsuarioAD:
    def __init__(self, login, nome, email, cargo, departamento, gestor, conta_ativa, senha_nunca_expira, senha_expira_em, dias_restantes, matricula, cpf ):
        self.login = login
        self.nome = nome
        self.email = email
        self.cargo = cargo
        self.departamento = departamento
        self.gestor = gestor
        self.conta_ativa = conta_ativa
        self.senha_nunca_expira = senha_nunca_expira
        self.senha_expira_em = senha_expira_em
        self.dias_restantes  = dias_restantes
        self.matricula  = matricula
        self.cpf = cpf