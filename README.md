# 🌈 HealthCare — API de Agendamentos

API RESTful para gerenciamento de profissionais de saúde e agendamento de consultas com foco social: inclusão e apoio à comunidade LGBTQIAPN+.

> 🚀 Produção: https://healthcare-appointments-api.onrender.com/api/docs

---

## ✨ Visão Geral

Esta API foi desenvolvida como solução para o processo seletivo da Lacrei Saúde. Objetivos principais:

- Fornecer endpoints robustos para cadastro de profissionais de saúde e gerenciamento de consultas médicas;
- Garantir segurança, rastreabilidade e observabilidade (logs, testes e pipeline CI/CD);
- Facilitar deploy via containers e integração com provedores de pagamento (ex.: integração conceitual com Asaas para split de pagamentos).

---

## 🛠️ Tecnologias e Ecossistema

- **Python 3.13**
- **Django 6.0**
- **Django REST Framework (DRF)**
- **Poetry** (gerenciador de dependências)
- **PostgreSQL**
- **Docker & Docker Compose**
- **Ruff** (lint / formatter)
- **GitHub Actions** (CI/CD)

---

## 🏗️ Arquitetura & Justificativas Técnicas

- **Django ORM & Segurança**: o uso do Django ORM evita SQL Injection porque utiliza queries parametrizadas nativamente. Além disso, os `serializers` do DRF centralizam validações de entrada e regras de negócio.

- **CORS & Autenticação**: `django-cors-headers` limita origens permitidas, protegendo endpoints contra acessos indevidos. As views usam permissões globais do DRF (e.g., `IsAuthenticated`/roles) para controle de acesso por recurso.

- **Poetry**: adotado para garantir determinismo nas dependências via `poetry.lock`, reprodutibilidade de ambientes e facilidade de publicação/CI.

- **Logs de Acesso e Erros**: design de logging distinto por ambiente:
  - Desenvolvimento (DEBUG=True): `RotatingFileHandler` salva logs localmente com limite de 5MB por arquivo, preservando histórico e evitando crescimento indefinido.
  - Produção (DEBUG=False): `StreamHandler` envia logs para `stdout` (prática recomendada em containers), permitindo coleta por orquestradores/serviços de logging.

---

## ⚙️ Setup do Ambiente Local

### Pré-requisitos

- Docker e Docker Compose instalados (recomendado).
- Para execução nativa: Python 3.13 e Poetry instalados.

### Método A — Docker (recomendado)

O `docker compose` sobe a API e o PostgreSQL. O `entrypoint` já executa migrations automaticamente.

```bash
# Construir e iniciar containers em background
docker compose up -d --build

# Ver logs
docker compose logs -f
```

Após subir: API local em `http://localhost:8000/api` e documentação Swagger em `http://localhost:8000/api/docs`.

### Método B — Execução nativa (Poetry)

```bash
# Instalar dependências
poetry install

# Ativar shell (opcional)
poetry shell

# Rodar migrations
python manage.py migrate

# Iniciar servidor de desenvolvimento
python manage.py runserver
```

Docs locais: `http://localhost:8000/api/docs`.

---

## ✅ Suite de Testes e Qualidade

- Rodar testes automatizados (APITestCase):

```bash
python manage.py test
```

- Rodar linter/formatador (Ruff):

```bash
ruff check .
```

Inclua novos testes para qualquer bugfix ou feature que altere regras de negócio.

---

## ⚙️ Esteira de CI/CD & Fluxo de Deploy

O pipeline no GitHub Actions foi pensado em duas frentes:

1. **Esteira de Qualidade (`test-and-lint`)**
   - Executa `ruff` e a suíte de testes (`python manage.py test`).
   - Bloqueia merges se falhas forem detectadas.

2. **Esteira de Infraestrutura (`build-and-deploy-aws`)**
   - Implementada para demonstrar integração com AWS utilizando Amazon ECR e ECS/App Runner.
   - O deploy produtivo deste desafio foi realizado em Render para evitar custos adicionais de infraestrutura.
   - A ativação do deploy na AWS requer apenas a configuração das credenciais da conta e a habilitação das etapas de push e atualização do serviço já definidas no workflow.

> Nota: o deploy público ativo está disponível em Render e a URL da API e docs é fornecida no topo do README.

---

## 🔁 Proposta de Rollback Funcional

Mitigar riscos em produção com duas estratégias complementares:

1. **Rollback via Imagem Docker**
   - Mantemos imagens Docker tagueadas por SHA (commit). No painel do provedor é possível reverter para a tag estável anterior em segundos, retornando o tráfego à versão conhecida.

2. **Rollback via Git Revert**
   - Fluxo: `git revert <hash>` → push para `main` → GitHub Actions valida e redeploya. Útil quando é necessário documentar o revert no histórico de commits.

Ambas estratégias garantem reprodutibilidade e testes automáticos antes do novo deploy.

---

## 💳 Proposta de Integração com Asaas (Split de Pagamentos)

Arquitetura conceitual para pagamentos com split (fluxo simplificado):

- Serviço de pagamentos externo (Asaas) para criar subcontas e cobranças;
- Nossa API registra `walletId` do profissional para roteamento de receita;
- Webhooks processam eventos de pagamento para atualizar o estado da consulta.

Fluxo proposto:

1. **Onboarding (criar subconta do profissional)**

- Endpoint (exemplo): `POST /api/v1/payments/accounts/`
- Ação: cria subconta no Asaas (`POST /v3/accounts`) e salva `walletId` no perfil do profissional.

2. **Cobrança com Split**

Exemplo de payload JSON para cobrar R$ 200,00 via PIX com split 90% para o profissional e 10% para a plataforma:

```json
{
  "amount": 200.00,
  "currency": "BRL",
  "method": "PIX",
  "split": [
    {"walletId": "WALLET_PROFISSIONAL_123", "percentage": 90},
    {"walletId": "WALLET_PLATAFORMA_456", "percentage": 10}
  ],
  "metadata": {
    "appointment_id": "APPT_abc123",
    "description": "Consulta médica - pagamento via API"
  }
}
```

- Endpoint (exemplo): `POST /api/v1/payments/charge/` → repassa payload ao gateway (Asaas) que processa split.

3. **Sincronização por Webhook**

- Endpoint de escuta: `POST /api/v1/payments/webhook/`
- Quando o gateway envia `PAYMENT_RECEIVED`, a API valida a assinatura (se aplicável) e atualiza o status da consulta para `Confirmada` de forma assíncrona.

```json
{
  "event": "PAYMENT_RECEIVED",
  "data": {
    "appointment_id": "APPT_abc123",
    "amount": 200.00,
    "gateway_reference": "XYZ789"
  }
}
```

---

## 📦 Endpoints Principais

A API responde sob o prefixo `/api/` e utiliza barras finais (`/`). A listagem completa de esquemas e testes interativos está disponível na página do Swagger em `/api/docs/`.

### 🔐 Autenticação (JWT)
*   `POST /api/token/` — Obtém o par de tokens (Access e Refresh Token) enviando as credenciais do usuário.
*   `POST /api/token/refresh/` — Renova o Access Token utilizando o Refresh Token.

### 🏥 Profissionais de Saúde
*   `GET /api/profissionais/` — Listagem de todos os profissionais cadastrados.
*   `POST /api/profissionais/` — Cadastro de um novo profissional (Nome social, Profissão, Endereço, Contato).
*   `GET /api/profissionais/{id}/` — Detalhes de um profissional específico.
*   `PUT/PATCH /api/profissionais/{id}/` — Atualização dos dados do profissional.
*   `DELETE /api/profissionais/{id}/` — Remoção do cadastro de um profissional.

### 📅 Consultas Médicas
*   `GET /api/consultas/` — Listagem de todas as consultas agendadas.
*   `POST /api/consultas/` — Agendamento de uma nova consulta vinculada a um profissional (Data, Profissional via FK).
*   `GET /api/consultas/profissional/{id}/` — **(Requisito do Desafio)** Busca e filtragem de consultas utilizando o ID do profissional de saúde.

*Nota: Todos os retornos da API são estritamente entregues em formato JSON.*

---

## 🤝 Contribuição

- Fork → branch de feature → PR com descrição clara e testes.
- Siga o padrão de commits semânticos e escreva testes para novas regras de negócio.

Sugestões de labels: `feature`, `bug`, `chore`.

---

## 🛣️ Roadmap (curto prazo)

- Implementar integração completa com Asaas (sandbox);
- Dashboard básico para profissionais;
- Monitoramento com Prometheus/Grafana e alertas;
- Testes end-to-end com Playwright/HTTP.

---