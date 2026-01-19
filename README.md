# 👥 usuarios_ad – Módulo de Integração com Active Directory

Este projeto é um **módulo base** responsável pela **integração, consulta e sincronização de usuários do Active Directory**.

Ele foi desenvolvido para centralizar toda a lógica de comunicação com o AD, servindo como **dependência obrigatória** para outros sistemas e automações.

---

## 🔗 Projetos que dependem deste módulo

Este repositório é utilizado diretamente pelo projeto:

👉 https://github.com/WiBaP/inventario_equipamentos.git  

Esse módulo fornece as rotinas de:
- Importação de usuários do AD  
- Atualização de dados (nome, e-mail, gestor, status, etc.)  
- Identificação de usuários desligados  
- Padronização do acesso ao Active Directory  

---

## 🎯 Objetivo do projeto

- Centralizar a comunicação com o Active Directory  
- Evitar duplicação de código entre sistemas  
- Padronizar integrações com AD  
- Servir como base para automações corporativas  

---

## 🚀 Funcionalidades

- Consulta de usuários no Active Directory  
- Sincronização com banco de dados  
- Atualização controlada de informações  
- Identificação de contas inexistentes/desligadas  
- Suporte a automações administrativas  

---

## 🛠 Tecnologias utilizadas

- Python  
- LDAP / Active Directory  
- PyODBC  
- SQL Server  
- dotenv  

---

## ⚙️ Instalação

```bash
git clone https://github.com/WiBaP/usuarios_ad.git
cd usuarios_ad
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

▶️ Execução (exemplo)
uvicorn main:app --reload

Acesse:
http://localhost:8000

📌 Observações importantes
Este módulo não é um sistema final e sim uma camada de integração

Deve ser utilizado como dependência por outros projetos

Credenciais e strings de conexão devem ser definidas via variáveis de ambiente

Nunca versionar senhas ou dados sensíveis

🔮 Próximos passos
Padronizar interface de serviços

Criar logs estruturados

Implementar testes automatizados

Empacotar o módulo para reutilização

