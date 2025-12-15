# 🏥 Sistema de Gestão Hospitalar e de Serviços de Saúde – VidaPlus (SGHSS)

Este repositório contém o **back-end completo** de um **Sistema de Gestão Hospitalar e de Serviços de Saúde (SGHSS)** desenvolvido como **trabalho acadêmico** da disciplina **Projetos**, com foco em **Back-end** e **Engenharia de Software**.

O sistema foi projetado para simular um **cenário real de alta criticidade na área da saúde**, contemplando segurança, controle de acesso, auditoria (logs) e telemedicina.

---

## 📚 Contexto acadêmico

Este projeto foi desenvolvido com **abordagem teórica-prática**, ou seja:

* O **back-end foi implementado de forma funcional e testável**
* O **front-end (HTML/CSS)** existe apenas como protótipo visual
* **Não há integração direta entre front-end e back-end**
* Todas as funcionalidades do back-end podem ser testadas **via API REST**, utilizando ferramentas como o **Insomnia**

O objetivo é demonstrar:

* Modelagem correta
* Arquitetura
* Boas práticas
* Segurança
* Organização
* Documentação profissional

---

## 🎯 Objetivos do sistema

O SGHSS VidaPlus tem como objetivo centralizar:

* Cadastro e atendimento de pacientes
* Gestão de profissionais de saúde
* Gestão administrativa
* Agendamento de consultas presenciais e online
* Telemedicina (link automático de videochamada)
* Controle de acesso por perfil
* Registro completo de logs (auditoria)
* Conformidade conceitual com a LGPD

---

## 👥 Perfis de usuário

O sistema trabalha com **três perfis distintos**, cada um com permissões específicas:

### 👨‍💼 Administrador (ADMIN)

* Cria administradores
* Cria profissionais de saúde
* Visualiza todos os pacientes
* Cria, visualiza e cancela qualquer consulta
* Visualiza todos os logs do sistema

### 🧑‍⚕️ Profissional de Saúde (PROF)

* Visualiza **apenas suas consultas**
* Cancela suas consultas (justificativa obrigatória)
* Não cria consultas
* Não cria usuários

### 🧑‍🦱 Paciente (PACIENTE)

* Pode se auto-cadastrar (sem login prévio)
* Visualiza e edita seu próprio cadastro
* Cria, visualiza e cancela suas próprias consultas
* Acessa link de teleconsulta

---

## 🛠️ Tecnologias utilizadas

### Back-end

* **Python**
* **Django**
* **Django REST Framework**
* **Token Authentication**
* **SQLite** (banco relacional SQL)

### Ferramentas

* **Git / GitHub**
* **Insomnia** (testes de API)
* **Virtualenv (venv)**

---

## 📁 Estrutura do projeto

```text
sghss/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── sghss/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── core/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── permissions.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── migrations/
    │   └── __init__.py
    └── management/
        └── commands/
            └── criar_admin_inicial.py
```

---

## ⚙️ Pré-requisitos

Antes de começar, você precisa ter instalado:

* **Python 3.12 ou superior**
* **Git**
* **Insomnia** (ou Postman)

Links úteis:

* Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Insomnia: [https://insomnia.rest/](https://insomnia.rest/)

---

## 🚀 Como executar o projeto (passo a passo)

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/daniel-lgs/sistema-VidaPlus.git
cd sistema-VidaPlus/sghss
```

---

### 2️⃣ Crie e ative o ambiente virtual (venv)

```bash
python -m venv venv
```

#### Windows (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

> Caso o PowerShell bloqueie scripts, execute uma vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Crie o banco de dados e as tabelas

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Crie o administrador inicial (obrigatório)

```bash
python manage.py criar_admin_inicial
```

Esse comando cria automaticamente o **ADMIN padrão do sistema**:

* **E-mail:** `sistema.sghss@gmail.com`
* **Senha:** `dSf@#4340fdk`

---

### 6️⃣ Inicie o servidor

```bash
python manage.py runserver
```

O sistema estará disponível em:

```
http://127.0.0.1:8000
```

---

## 🔐 Autenticação (muito importante)

O sistema utiliza **Token Authentication**.

### Login

**POST** `/api/auth/login/`

```json
{
  "email": "sistema.sghss@gmail.com",
  "senha": "dSf@#4340fdk"
}
```

A resposta conterá um **token**.

---

### ⚠️ Header obrigatório em TODAS as requisições protegidas

```http
Authorization: Token SEU_TOKEN_AQUI
```

❗ A palavra **Token** é obrigatória
❗ Cada requisição precisa do header (abas do Insomnia não compartilham)

---

## 🧪 Testando no Insomnia (roteiro básico)

### Criar paciente (sem autenticação)

**POST** `/api/pacientes/`

```json
{
  "email": "paciente1@exemplo.com",
  "senha": "SenhaPaciente123",
  "nome_completo": "Paciente de Teste",
  "cpf": "123.456.789-00",
  "data_nascimento": "1990-01-01",
  "telefone": "11999999999",
  "endereco": "Rua Exemplo, 123"
}
```

---

### Criar profissional de saúde (ADMIN)

**POST** `/api/profissionais-saude/`
Header: `Authorization: Token ...`

```json
{
  "email": "medico1@exemplo.com",
  "senha": "SenhaMedico123",
  "nome_completo": "Dr. João da Silva",
  "especialidade": "Cardiologia",
  "registro_profissional": "CRM-12345"
}
```

---

### Criar consulta online

**POST** `/api/consultas/`

```json
{
  "paciente": 1,
  "profissional": 1,
  "tipo_atendimento": "ONLINE",
  "data_horario": "2026-01-10T14:00:00Z",
  "local": ""
}
```

➡️ O sistema gera automaticamente um link Jitsi:

```
https://meet.jit.si/abc-def-ghi
```

---

### Cancelar consulta

**POST** `/api/consultas/1/cancelar/`

Profissional:

```json
{
  "justificativa": "Imprevisto na agenda."
}
```

---

### Visualizar logs (somente ADMIN)

**GET** `/api/logs/`

---

## 🧾 Logs e auditoria

✔️ Todas as ações relevantes são registradas:

* Login
* Logout
* Criação/edição/exclusão de usuários
* Criação e cancelamento de consultas

✔️ Logs incluem:

* Usuário
* Ação
* Data/hora
* IP

✔️ Apenas administradores podem consultar logs

---

## 🔒 Segurança e LGPD (nível acadêmico)

* Senhas criptografadas
* Controle de acesso por perfil
* Restrição de dados por sessão
* Auditoria completa
* Separação clara de responsabilidades

---

## ⚠️ Aviso importante

Este projeto:

* **Não é para produção**
* Utiliza servidor de desenvolvimento do Django
* Foi desenvolvido **exclusivamente para fins acadêmicos**
