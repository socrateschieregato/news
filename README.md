# Jota News API

API REST para gerenciamento de notícias com funcionalidades de CRUD, agendamento, categorização e níveis de acesso baseados em planos de assinatura.

## Requisitos

- Python 3.11+
- PostgreSQL
- Redis
- Docker e Docker Compose (opcional)

## Configuração do Ambiente

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd jota_news
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
POSTGRES_DB=jota_news
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
REDIS_URL=redis://localhost:6379/0
```

### 5. Inicie os serviços com Docker Compose
```bash
docker-compose up -d
```

### 6. Execute as migrações
```bash
python manage.py migrate
```

### 7. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

## Rodando o Projeto

### Iniciar o servidor Django
```bash
python manage.py runserver
```

### Iniciar o Celery (em outro terminal)
```bash
celery -A jota_news worker -l info
```

## Acessando a API

- Documentação Swagger: http://localhost:8000/swagger/
- Documentação ReDoc: http://localhost:8000/redoc/
- Admin Interface: http://localhost:8000/admin/

## Endpoints da API

### Autenticação
- POST `/api/token/` - Obter token JWT
- POST `/api/token/refresh/` - Renovar token JWT

### Usuários
- GET `/api/users/` - Listar usuários
- POST `/api/users/` - Criar usuário
- GET `/api/users/{id}/` - Detalhes do usuário
- PUT `/api/users/{id}/` - Atualizar usuário
- DELETE `/api/users/{id}/` - Deletar usuário

### Planos
- GET `/api/plans/` - Listar planos
- POST `/api/plans/` - Criar plano
- GET `/api/plans/{id}/` - Detalhes do plano
- PUT `/api/plans/{id}/` - Atualizar plano
- DELETE `/api/plans/{id}/` - Deletar plano

### Verticais
- GET `/api/verticais/` - Listar verticais
- POST `/api/verticais/` - Criar vertical
- GET `/api/verticais/{id}/` - Detalhes da vertical
- PUT `/api/verticais/{id}/` - Atualizar vertical
- DELETE `/api/verticais/{id}/` - Deletar vertical

### Notícias
- GET `/api/news/` - Listar notícias
- POST `/api/news/` - Criar notícia
- GET `/api/news/{id}/` - Detalhes da notícia
- PUT `/api/news/{id}/` - Atualizar notícia
- DELETE `/api/news/{id}/` - Deletar notícia

### Categorias
- GET `/api/categories/` - Listar categorias
- POST `/api/categories/` - Criar categoria
- GET `/api/categories/{id}/` - Detalhes da categoria
- PUT `/api/categories/{id}/` - Atualizar categoria
- DELETE `/api/categories/{id}/` - Deletar categoria

## Modelos de Dados

### Usuário
- Campos: id, username, email, password, plan, is_active, date_joined
- Relacionamentos: plan (ForeignKey para Plan)

### Plano
- Campos: id, name, description, price, features, verticais
- Relacionamentos: verticais (ManyToMany para Vertical)

### Vertical
- Campos: id, name, description, slug
- Relacionamentos: news (ForeignKey reversa de News)

### Notícia
- Campos: id, title, subtitle, content, image, author, category, vertical, access_type, status, publish_date, created_at, updated_at
- Relacionamentos: author (ForeignKey para User), category (ForeignKey para Category), vertical (ForeignKey para Vertical)

### Categoria
- Campos: id, name, slug, vertical, description, created_at, updated_at
- Relacionamentos: vertical (CharField com choices)

## Testes

Para rodar os testes:
```bash
pytest
```

Para rodar os testes com cobertura:
```bash
pytest --cov
```

## Estrutura do Projeto

```
jota_news/
├── .github/            # Configurações do GitHub (CI/CD, workflows)
├── jota_news/          # Configurações do projeto Django
│   ├── __init__.py
│   ├── settings.py     # Configurações do projeto
│   ├── urls.py         # URLs principais
│   ├── asgi.py         # Configuração ASGI
│   └── wsgi.py         # Configuração WSGI
├── news/               # App de notícias
│   ├── __init__.py
│   ├── admin.py        # Configuração do admin
│   ├── apps.py         # Configuração do app
│   ├── models.py       # Modelos de dados
│   ├── serializers.py  # Serializers da API
│   ├── tests/          # Testes do app
│   ├── urls.py         # URLs do app
│   └── views.py        # Views da API
├── users/              # App de usuários
│   ├── __init__.py
│   ├── admin.py        # Configuração do admin
│   ├── apps.py         # Configuração do app
│   ├── models.py       # Modelos de dados
│   ├── serializers.py  # Serializers da API
│   ├── tests/          # Testes do app
│   ├── urls.py         # URLs do app
│   └── views.py        # Views da API
├── staticfiles/        # Arquivos estáticos coletados
├── media/             # Arquivos de mídia (uploads)
├── venv/              # Ambiente virtual Python
├── .env               # Variáveis de ambiente
├── .gitignore         # Configuração do Git
├── docker-compose.yml # Configuração do Docker Compose
├── Dockerfile         # Configuração do Docker
├── manage.py          # Script de gerenciamento Django
├── pytest.ini         # Configuração do Pytest
├── requirements.txt   # Dependências do projeto
└── README.md          # Documentação do projeto
```

## Funcionalidades

- CRUD completo de notícias, categorias, usuários, planos e verticais
- Autenticação via JWT
- Permissões baseadas em roles (editor, autor, leitor)
- Conteúdo PRO para assinantes
- Agendamento de publicações
- Categorização de notícias por vertical
- Upload de imagens
- Documentação automática com Swagger/OpenAPI
- Sistema de planos de assinatura
- Gerenciamento de verticais de conteúdo
