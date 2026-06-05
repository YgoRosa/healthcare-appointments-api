# 🌈 HealthCare — API de Agendamentos

API RESTful para gerenciamento de profissionais de saúde e agendamento de consultas com foco social: inclusão e apoio à comunidade LGBTQIAPN+.

> 🚀 API em Produção: https://healthcare-appointments-api.onrender.com/api
>
> 📖 Documentação Swagger: https://healthcare-appointments-api.onrender.com/api/docs

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
  - Desenvolvimento (DEBUG=True): `RotatingFileHandler` salva logs localmente em logs/app.log com limite de 5MB por arquivo, preservando histórico e evitando crescimento indefinido.
  - Produção (DEBUG=False): `StreamHandler` envia logs para `stdout` (prática recomendada em containers), permitindo coleta por orquestradores/serviços de logging.

---

## ⚙️ Setup do Ambiente Local

### Pré-requisitos

- Docker e Docker Compose instalados (com suporte a BuildKit).
- Para execução nativa: Python 3.13 e Poetry (v2.0+) instalados.

### Método A — Docker (recomendado)

O `docker compose` sobe a API e o PostgreSQL. O `entrypoint` já executa migrations automaticamente.

```bash
# Construir e iniciar containers em background
docker compose up -d --build

# Ver logs em tempo real
docker compose logs -f
```

Após subir: API local em `http://localhost:8000/api` e documentação Swagger em `http://localhost:8000/api/docs`.

### Método B — Execução nativa (Poetry)

```bash
# Instalar dependências
poetry install

# Executar migrações do banco local
poetry run python manage.py migrate

# Iniciar servidor de desenvolvimento
poetry run python manage.py runserver
```

Docs locais: `http://localhost:8000/api/docs`.

## 🧪 Como Testar a API
A API utiliza autenticação JWT para proteger os endpoints de gerenciamento de profissionais e consultas.

Para facilitar a avaliação do projeto, um usuário de homologação é criado automaticamente durante o deploy da aplicação em produção.

### Credenciais de Teste

```
> As credenciais abaixo existem apenas para fins de avaliação técnica.
Username: admin
Password: admin123
```

### Passo 1 — Obter um Access Token
Acesse a documentação interativa:

```
https://healthcare-appointments-api.onrender.com/api/docs/
```
Localize o endpoint:

```
POST /api/token/
```
Clique em **Try it out** e envie o seguinte JSON:

```
{
  "username": "admin",
  "password": "admin123"
}
```
A resposta será semelhante a:

```
{
  "refresh": "eyJ...",
  "access": "eyJ..."
}
```
Copie o valor retornado no campo `access`.

---

### Passo 2 — Autorizar as Requisições
Na parte superior da página do Swagger, clique em **Authorize**.

Cole o token obtido no passo anterior no campo de autenticação.

Caso o Swagger solicite o formato completo, utilize:

```
Bearer SEU_ACCESS_TOKEN
```
Clique em **Authorize** e depois em **Close**.

---

### Passo 3 — Executar os Endpoints
Após a autenticação, todos os endpoints protegidos poderão ser testados diretamente pela interface Swagger.

Exemplos:

```
GET /api/profissionais/
POST /api/profissionais/
GET /api/consultas/
POST /api/consultas/
GET /api/consultas/profissional/{id}/
```

---

### Ambiente Local
Caso esteja executando a aplicação localmente via Docker, você pode criar um superusuário próprio com:

```
docker compose exec web python manage.py createsuperuser
```
Após a criação, utilize as credenciais cadastradas no endpoint `/api/token/` para gerar seus tokens JWT.

> Observação: o usuário `admin` foi criado exclusivamente para facilitar a avaliação técnica do projeto. Em ambientes reais de produção, credenciais padrão não devem ser utilizadas.

---

## ✅ Suite de Testes e Qualidade

- Rodar testes automatizados (APITestCase):

```bash
poetry run python manage.py test
```

- Rodar linter/formatador (Ruff):

```bash
ruff check .
```

Inclua novos testes para qualquer bugfix ou feature que altere regras de negócio.

---

## ⚙️ Esteira de CI/CD & Fluxo de Deploy

O pipeline GitHub Actions é responsável por garantir a qualidade da aplicação antes de qualquer atualização.

### Esteira de Qualidade (`test-and-lint`)

- Executa análise estática de código com `ruff`;
- Executa a suíte de testes automatizados (`poetry run python manage.py test`);
- Bloqueia alterações caso falhas sejam identificadas.

### Deploy

O deploy produtivo da aplicação foi realizado utilizando a plataforma Render, onde a API está disponível publicamente para testes e validação.

Como estudo complementar de infraestrutura, foi documentado e estruturado o fluxo necessário para adaptação do projeto à AWS (Amazon ECR e ECS/App Runner), permitindo futura migração para um ambiente dedicado sem alterações significativas na arquitetura da aplicação.

> Nota: o deploy público ativo está disponível em Render e a URL da API e da documentação Swagger está disponível no topo deste README.

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

### Desafios Encontrados

- Configuração do ambiente Docker com PostgreSQL
- Integração do JWT com Swagger
- Automação de migrations durante o deploy

---

## 🛣️ Roadmap (curto prazo)

- Implementar integração completa com Asaas (sandbox);
- Dashboard básico para profissionais;
- Monitoramento com Prometheus/Grafana e alertas;
- Testes end-to-end com Playwright/HTTP.

---