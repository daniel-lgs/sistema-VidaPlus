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
