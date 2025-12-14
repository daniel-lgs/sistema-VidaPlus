# SGHSS VidaPlus – Back-end (Django + Django REST Framework)

## 1. Visão geral do projeto

Este repositório contém o **back-end** do sistema **SGHSS – Sistema de Gestão Hospitalar e de Serviços de Saúde da instituição VidaPlus**, desenvolvido como **projeto teórico** para a disciplina de Projetos (curso de Análise e Desenvolvimento de Sistemas da UNINTER).

O objetivo é demonstrar, de forma prática, como aplicar conceitos de:

- Engenharia de Software
- Boas práticas de desenvolvimento Back-end
- Arquitetura em camadas (API REST)
- Segurança e auditoria (logs, autenticação, controle de acesso)
- Front-end e testes

> Importante: este projeto se propõe a ser **um protótipo funcional de back-end**, com foco em **alguns módulos principais** (cadastro de usuários e consultas, autenticação e logs), e não em um produto final pronto para produção.

---

## 2. Funcionalidades implementadas

O back-end implementa:

### 2.1. Autenticação

- Login via **e-mail e senha**
- Geração de **Token** de autenticação (padrão Django REST Framework)
- Logout com revogação do token
- Controle de acesso por **papel** do usuário:
  - `ADMIN` – Administrador
  - `PACIENTE` – Paciente
  - `PROF` – Profissional de Saúde

### 2.2. CRUD de Pacientes

- Auto cadastro de pacientes **sem necessidade de usuário logado**
- Cadastro, atualização, listagem e exclusão de pacientes por **Administradores**
- Paciente autenticado pode:
  - Ver seu próprio cadastro
  - Atualizar seus dados
  - Excluir seu cadastro

### 2.3. CRUD de Administradores

- CRUD de administradores acessível **apenas para usuários com papel ADMIN**
- Criação de novos administradores somente por outro administrador

> O sistema inicia com um **Administrador pré-cadastrado**, criado pelo comando:
>
> - E-mail: `sistema.sghss@gmail.com`  
> - Senha: `dSf@#4340fdk`

### 2.4. CRUD de Profissionais de Saúde

- CRUD de profissionais de saúde (médicos, enfermeiros, técnicos etc.)
- Acesso restrito a **Administradores**
- Armazena dados como:
  - Nome completo
  - Especialidade
  - Registro profissional (CRM/COREN/etc.)

### 2.5. CRUD de Consultas (Presencial e Online)

- Pacientes podem:
  - Criar consultas **para si mesmos**
  - Listar suas próprias consultas
  - Cancelar suas consultas

- Administradores podem:
  - Criar consultas para qualquer paciente/profissional
  - Listar todas as consultas do sistema
  - Cancelar qualquer consulta

- Profissionais de Saúde podem:
  - Listar apenas consultas em que são o profissional responsável
  - Cancelar suas consultas com **justificativa obrigatória**

#### Telemedicina – Geração Automática de Link

Para consultas do tipo **ONLINE**, na criação da consulta o sistema gera automaticamente um link no padrão:

```text
https://meet.jit.si/abc-def-ghi

Ou seja, um link do serviço [**https://meet.jit.si**](https://meet.jit.si/) com um sufixo aleatório (como `ytr-koi-eqs`).

### 2.6. Logs de Ações (Auditoria)

Todas as ações importantes geram **logs**:

- Login / Logout
- Criação, atualização e exclusão de pacientes
- Criação, atualização e exclusão de administradores e profissionais de saúde
- Criação e cancelamento de consultas

Os logs registram:

- Usuário responsável (quando houver)
- Ação realizada
- Detalhes descritivos
- Data e hora
- IP (quando disponível)

> Apenas administradores podem consultar os logs via endpoint /api/logs/.
> 

---

## 3. Tecnologias utilizadas

- **Linguagem**: Python 3.x
- **Framework Web**: Django
- **API REST**: Django REST Framework
- **Autenticação**: Django REST Framework Token Authentication
- **Banco de dados**: SQLite (padrão, pode ser alterado para PostgreSQL/MySQL)
- **Ferramenta de testes de API**: Insomnia (pode usar também Postman ou `curl`)

---

## 4. Requisitos para executar o projeto

### 4.1. Software necessário

Antes de começar, instale:

1. **Python 3.10 ou superior**
    - Baixar no site oficial: pesquise por “Download Python” e escolha a versão para seu sistema.
    - Durante a instalação no Windows, marque a opção **“Add Python to PATH”**.
2. **Git** (opcional, mas recomendado)
    - Usado para clonar o repositório.
3. **Insomnia**
    - Ferramenta gráfica para testar endpoints HTTP.
    - Baixe no site do Insomnia (busque por “Download Insomnia REST Client”).

---

## 5. Passo a passo para rodar o servidor (ambiente local)

### 5.1. Clonar o repositório

Se o back-end estiver dentro do seu repositório `sistema-VidaPlus`:

```bash
git clone https://github.com/daniel-lgs/sistema-VidaPlus.git
cd sistema-VidaPlus

# se o backend estiver numa pasta específica, por exemplo:
cd backend

```

Se você criar um repo separado para o back-end, adapte o comando.

### 5.2. Criar e ativar um ambiente virtual (virtualenv)

No Windows (PowerShell):

```bash
python -m venv venv
venv\Scripts\activate

```

No Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate

```

Você saberá que o ambiente está ativo porque aparecerá algo como `(venv)` no início da linha do terminal.

### 5.3. Instalar as dependências

Com o ambiente virtual já ativado e dentro da pasta do projeto (onde está o `requirements.txt`):

```bash
pip install -r requirements.txt

```

### 5.4. Aplicar as migrações do banco de dados

```bash
python manage.py migrate

```

Isso vai criar as tabelas necessárias (usuários, pacientes, consultas, logs etc.) no banco `db.sqlite3`.

### 5.5. Criar o administrador inicial

O projeto possui um comando customizado para criar o **Administrador padrão** do sistema.

Execute:

```bash
python manage.py criar_admin_inicial

```

Se tudo der certo, você verá uma mensagem indicando que o administrador foi criado com:

- E-mail: `sistema.sghss@gmail.com`
- Senha: `dSf@#4340fdk`

> Essas credenciais também serão mencionadas no documento do trabalho para que o professor consiga testar.
> 

### 5.6. Executar o servidor de desenvolvimento

Por fim, rode:

```bash
python manage.py runserver

```

Por padrão, o servidor ficará disponível em:

```
http://127.0.0.1:8000/

```

Os endpoints da API estarão sob `/api/`, por exemplo:

- `http://127.0.0.1:8000/api/auth/login/`
- `http://127.0.0.1:8000/api/pacientes/`
- `http://127.0.0.1:8000/api/consultas/`
- etc.

---

## 6. Estrutura de pastas do projeto

Resumo da estrutura principal:

```
sghss/
├── manage.py                 # Arquivo de gerenciamento do Django
├── requirements.txt          # Dependências do projeto
├── sghss/                    # Pasta do projeto Django
│   ├── __init__.py
│   ├── settings.py           # Configurações (apps, banco, DRF, etc.)
│   ├── urls.py               # Rotas principais (inclui /api/)
│   └── wsgi.py
└── core/                     # App principal (lógica de negócio)
    ├── __init__.py
    ├── admin.py              # Registro de modelos no admin do Django
    ├── apps.py
    ├── models.py             # Modelos: Usuario, Paciente, Administrador, ProfissionalSaude, Consulta, LogAcao
    ├── permissions.py        # Permissões baseadas em papel (ADMIN, PACIENTE, PROF)
    ├── serializers.py        # Serializers DRF para converter modelos <-> JSON
    ├── urls.py               # Rotas da API: /pacientes, /consultas, etc.
    ├── views.py              # Lógica das views e endpoints REST
    ├── tests.py              # (Opcional) testes automatizados
    └── management/
        └── commands/
            └── criar_admin_inicial.py   # Comando para criar o admin inicial

```

---

## 7. Como testar a API no Insomnia

A seguir, um passo a passo **prático** para testar os principais endpoints.

### 7.1. Criar um ambiente no Insomnia

1. Abra o Insomnia.
2. Crie um **New Collection** (ou **New Workspace**).
3. Nas configurações do ambiente, crie uma variável, por exemplo:

```json
{
  "base_url": "http://127.0.0.1:8000/api",
  "token": ""
}

```

Depois, quando você fizer login, preencha o campo `"token"` com o valor retornado.

---

### 7.2. Login como Administrador

- **Método**: `POST`
- **URL**: `{{ base_url }}/auth/login/`

**Body (JSON):**

```json
{
  "email": "sistema.sghss@gmail.com",
  "senha": "dSf@#4340fdk"
}

```

Se estiver tudo certo, a resposta será algo como:

```json
{
  "token": "c1a2b3c4d5...",
  "usuario": {
    "id": 1,
    "email": "sistema.sghss@gmail.com",
    "papel": "ADMIN"
  }
}

```

Copie o valor de `"token"` e coloque na variável `token` do ambiente.

---

### 7.3. Enviar o token em todas as requisições autenticadas

Em cada request autenticado, adicione o header:

- **Header**: `Authorization`
- **Valor**: `Token {{ token }}`

Exemplo: `Token c1a2b3c4d5...`

---

### 7.4. Testar CRUD de Pacientes

### 7.4.1. Criar paciente (auto-cadastro, sem token)

- **Método**: `POST`
- **URL**: `{{ base_url }}/pacientes/`
- **Headers**: não precisa de `Authorization` (pode deixar vazio)

**Body (JSON):**

```json
{
  "email": "paciente1@exemplo.com",
  "senha": "SenhaSegura123",
  "nome_completo": "Paciente de Teste",
  "cpf": "123.456.789-00",
  "data_nascimento": "1990-01-01",
  "telefone": "11999999999",
  "endereco": "Rua Exemplo, 123"
}

```

Você receberá de volta os dados do paciente criado.

### 7.4.2. Listar pacientes (como ADMIN)

- **Método**: `GET`
- **URL**: `{{ base_url }}/pacientes/`
- **Headers**:
    - `Authorization: Token {{ token }}` (token do admin)

Deve retornar a lista de pacientes.

---

### 7.5. Criar um Profissional de Saúde (como ADMIN)

- **Método**: `POST`
- **URL**: `{{ base_url }}/profissionais-saude/`
- **Headers**:
    - `Authorization: Token {{ token }}` (token do admin)

**Body (JSON):**

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

### 7.6. Criar uma Consulta (como Paciente ou como Admin)

### 7.6.1. Login como Paciente

Use o endpoint `/auth/login/` com o e-mail/senha do paciente criado.

Salve o token na variável `token`.

### 7.6.2. Criar consulta online (Paciente)

- **Método**: `POST`
- **URL**: `{{ base_url }}/consultas/`
- **Headers**:
    - `Authorization: Token {{ token }}` (token do paciente)

**Body (JSON):**

```json
{
  "paciente": 1,               // será ignorado e substituído pelo paciente logado
  "profissional": 1,           // ID do profissional criado
  "tipo_atendimento": "ONLINE",
  "data_horario": "2025-12-31T14:00:00Z",
  "local": ""                  // pode ficar vazio para online
}

```

A resposta conterá algo como:

```json
{
  "id": 1,
  "paciente": 1,
  "profissional": 1,
  "administrador_criador": null,
  "tipo_atendimento": "ONLINE",
  "data_horario": "2025-12-31T14:00:00Z",
  "local": null,
  "link_teleconsulta": "https://meet.jit.si/abc-def-ghi",
  "status": "AGENDADA",
  "justificativa_cancelamento": null,
  "criado_em": "...",
  "atualizado_em": "..."
}

```

Note o campo **`link_teleconsulta`** já preenchido com um link do **meet.jit.si**.

---

### 7.7. Cancelar uma Consulta

### 7.7.1. Cancelar como Paciente

- **Método**: `POST`
- **URL**: `{{ base_url }}/consultas/1/cancelar/`
- **Headers**:
    - `Authorization: Token {{ token }}` (token do paciente dono da consulta)

**Body (JSON opcional):**

```json
{
  "justificativa": "Não poderei comparecer."
}

```

O status da consulta será atualizado para `CANCELADA_PACIENTE`.

### 7.7.2. Cancelar como Profissional de Saúde (justificativa obrigatória)

- **Método**: `POST`
- **URL**: `{{ base_url }}/consultas/1/cancelar/`
- **Headers**:
    - `Authorization: Token {{ token }}` (token do profissional)

**Body (JSON):**

```json
{
  "justificativa": "Imprevisto médico na agenda."
}

```

Se não enviar `justificativa`, o sistema retorna erro 400.

---

### 7.8. Consultar Logs (como ADMIN)

- **Método**: `GET`
- **URL**: `{{ base_url }}/logs/`
- **Headers**:
    - `Authorization: Token {{ token }}` (token do admin)

Retorna uma lista de logs com:

- Usuário
- Ação
- Detalhes
- Data e hora
- IP (se disponível)

---

## 8. Próximos passos e integração com o trabalho acadêmico

Este back-end foi pensado para:

- Ser **testável de forma independente** (sem depender do front-end)
- Ser utilizado como base para o **trabalho teórico**, onde:
    - A parte de **Implementação** descreverá **todos os endpoints** (método, URL, parâmetros, JSON, respostas, códigos HTTP).
    - A parte de **Análise de Requisitos** e **Modelagem** vai se apoiar nas funcionalidades aqui descritas.
    - A **Telemedicina** será exemplificada através das consultas online e dos links `https://meet.jit.si/...`.
    - A **Segurança e Compliance (LGPD)** será discutida com base em:
        - Autenticação por token
        - Controle de acesso por papel
        - Logs de auditoria