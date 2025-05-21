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
docker-compose up -d db redis
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

- API Base URL: http://localhost:8000/api/
- Documentação Swagger: http://localhost:8000/swagger/
- Documentação ReDoc: http://localhost:8000/redoc/
- Admin Interface: http://localhost:8000/admin/

## Endpoints Principais

### Autenticação
- POST `/api/token/` - Obter token JWT
- POST `/api/token/refresh/` - Renovar token JWT

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
├── jota_news/          # Configurações do projeto
├── news/               # App principal de notícias
│   ├── models.py       # Modelos de dados
│   ├── views.py        # Views da API
│   ├── serializers.py  # Serializers
│   └── tests/          # Testes
├── users/              # App de usuários
├── manage.py
├── requirements.txt
└── docker-compose.yml
```

## Funcionalidades

- CRUD completo de notícias e categorias
- Autenticação via JWT
- Permissões baseadas em roles (editor, autor, leitor)
- Conteúdo PRO para assinantes
- Agendamento de publicações
- Categorização de notícias
- Upload de imagens
- Documentação automática com Swagger/OpenAPI
