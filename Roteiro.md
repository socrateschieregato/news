# Roteiro de Apresentação - Jota News API

## 1. Visão Geral do Sistema
- API REST para gerenciamento de notícias
  - Desenvolvida com Django REST Framework
  - Segue padrões RESTful
  - Documentação automática com Swagger/OpenAPI
- Sistema de assinaturas com diferentes planos
  - Planos básicos e premium
  - Acesso diferenciado por vertical
  - Sistema de preços flexível
- Categorização por verticais
  - Organização hierárquica: Vertical > Categoria > Notícia
  - Verticais: Poder, Tributos, Saúde, Energia, Trabalhista
  - Categorias específicas por vertical
- Conteúdo PRO e público
  - Controle granular de acesso
  - Paywall inteligente
  - Preview de conteúdo PRO
- Autenticação via JWT
  - Tokens de acesso e refresh
  - Segurança reforçada
  - Sessões persistentes

## 2. Demonstração das Funcionalidades

### 2.1 Autenticação
1. Obter Token JWT
```bash
POST /api/token/
{
    "username": "socrates",
    "password": "sua_senha"
}
```
Resposta:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- O access_token é usado para autenticar requisições
- O refresh_token permite obter um novo access_token
- Tokens expiram após 5 minutos (access) e 24 horas (refresh)
- Explicar a estrutura do JWT (header, payload, signature)

2. Renovar Token
```bash
POST /api/token/refresh/
{
    "refresh": "seu_refresh_token"
}
```
- O refresh_token é usado para obter um novo access_token
- Não requer autenticação
- Mantém o usuário logado sem precisar de senha
- Explicar o fluxo de renovação automática

### 2.2 Gerenciamento de Planos
1. Criar um Plano
```bash
POST /api/plans/
{
    "name": "Plano Premium",
    "description": "Acesso completo a todas as verticais",
    "price": 99.90,
    "features": ["Acesso PRO", "Todas as verticais"],
    "verticais": [1, 2, 3]
}
```
- Planos definem o acesso do usuário
- Cada plano tem um preço específico
- Features listam os benefícios
- Verticais definem quais áreas o usuário pode acessar
- Explicar a relação com o sistema de pagamentos

2. Listar Planos
```bash
GET /api/plans/
```
Resposta:
```json
[
    {
        "id": 1,
        "name": "Plano Básico",
        "description": "Acesso a notícias públicas",
        "price": 0.00,
        "features": ["Notícias públicas"],
        "verticais": []
    },
    {
        "id": 2,
        "name": "Plano Premium",
        "description": "Acesso completo",
        "price": 99.90,
        "features": ["Acesso PRO", "Todas as verticais"],
        "verticais": [1, 2, 3]
    }
]
```
- Mostrar diferentes níveis de acesso
- Explicar a estrutura de preços
- Demonstrar como os planos afetam o acesso

### 2.3 Gerenciamento de Verticais
1. Criar uma Vertical
```bash
POST /api/verticais/
{
    "name": "Poder",
    "description": "Notícias sobre política e poder"
}
```
- Verticais são áreas temáticas
- Cada vertical tem suas próprias categorias
- Verticais podem ser PRO ou públicas
- Explicar a hierarquia de conteúdo

2. Listar Verticais
```bash
GET /api/verticais/
```
Resposta:
```json
[
    {
        "id": 1,
        "name": "Poder",
        "description": "Notícias sobre política e poder",
        "slug": "poder"
    },
    {
        "id": 2,
        "name": "Tributos",
        "description": "Notícias sobre impostos e tributos",
        "slug": "tributos"
    }
]
```
- Mostrar a organização do conteúdo
- Explicar como as verticais se relacionam com planos
- Demonstrar a navegação por vertical

### 2.4 Gerenciamento de Categorias
1. Criar uma Categoria
```bash
POST /api/categories/
{
    "name": "Política",
    "vertical": "PODER",
    "description": "Notícias sobre política"
}
```
- Categorias são subdivisões das verticais
- Cada categoria pertence a uma vertical
- Categorias ajudam na organização do conteúdo
- Explicar a estrutura hierárquica

2. Listar Categorias
```bash
GET /api/categories/
```
Resposta:
```json
[
    {
        "id": 1,
        "name": "Política",
        "slug": "politica",
        "vertical": "PODER",
        "description": "Notícias sobre política"
    },
    {
        "id": 2,
        "name": "Economia",
        "slug": "economia",
        "vertical": "TRIBUTOS",
        "description": "Notícias sobre economia"
    }
]
```
- Mostrar categorias por vertical
- Explicar como as categorias organizam o conteúdo
- Demonstrar a navegação por categoria

### 2.5 Gerenciamento de Notícias
1. Criar uma Notícia
```bash
POST /api/news/
FormData:
- title: "Título da Notícia"
- subtitle: "Subtítulo da Notícia"
- content: "Conteúdo da notícia..."
- image: [arquivo]
- category_id: 1
- access_type: "PUBLIC"
- is_pro: false
```
- Upload de imagens com validação
- Controle de acesso (PRO/Público)
- Relacionamentos com categoria e vertical
- Explicar o processo de publicação

2. Listar Notícias
```bash
GET /api/news/
```
Resposta:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/news/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Título da Notícia",
            "subtitle": "Subtítulo",
            "content": "Conteúdo...",
            "image": "http://localhost:8000/media/news_images/imagem.jpg",
            "author": "socrates",
            "category": {
                "id": 1,
                "name": "Política"
            },
            "access_type": "PUBLIC",
            "is_pro": false,
            "publish_date": "2024-03-20T10:00:00Z"
        }
    ]
}
```
- Paginação automática
- Filtros por categoria e vertical
- Ordenação por data
- Explicar a estrutura de resposta

3. Detalhes da Notícia
```bash
GET /api/news/1/
```
- Mostrar todos os campos
- Explicar relacionamentos
- Demonstrar controle de acesso:
  - Verificação do plano do usuário
  - Validação de assinatura ativa
  - Controle por vertical
  - Verificação de conteúdo PRO
  - Bloqueio de acesso não autorizado
  - Redirecionamento para upgrade
- Explicar o sistema de preview:
  - Exibição parcial do conteúdo PRO
  - Limite de caracteres visíveis
  - Chamada para ação (CTA)
  - Destaque de benefícios do plano
  - Opção de upgrade imediato
  - Persistência do conteúdo após assinatura

### 2.6 Gerenciamento de Usuários
1. Criar um Usuário
```bash
POST /api/users/
```

Exemplos para cada tipo de usuário:

a) Usuário Básico:
```json
{
    "username": "usuario_basico",
    "email": "basico@email.com",
    "password": "senha123",
    "plan": 1,  // ID do plano básico
    "is_active": true
}
```

b) Usuário Premium:
```json
{
    "username": "usuario_premium",
    "email": "premium@email.com",
    "password": "senha123",
    "plan": 2,  // ID do plano premium
    "is_active": true
}
```

c) Usuário Personalizado:
```json
{
    "username": "usuario_personalizado",
    "email": "personalizado@email.com",
    "password": "senha123",
    "plan": 3,  // ID do plano personalizado
    "is_active": true,
    "verticais": [1, 2]  // IDs das verticais permitidas
}
```

d) Editor:
```json
{
    "username": "editor",
    "email": "editor@email.com",
    "password": "senha123",
    "plan": 2,  // Plano premium
    "is_active": true,
    "role": "EDITOR"
}
```

e) Moderador:
```json
{
    "username": "moderador",
    "email": "moderador@email.com",
    "password": "senha123",
    "plan": 2,  // Plano premium
    "is_active": true,
    "role": "MODERATOR"
}
```

f) Administrador:
```json
{
    "username": "admin",
    "email": "admin@email.com",
    "password": "senha123",
    "plan": 2,  // Plano premium
    "is_active": true,
    "role": "ADMIN"
}
```

Resposta para todos os tipos:
```json
{
    "id": 1,
    "username": "nome_usuario",
    "email": "email@exemplo.com",
    "plan": {
        "id": 1,
        "name": "Nome do Plano"
    },
    "role": "ROLE_NAME",
    "is_active": true,
    "date_joined": "2024-03-20T10:00:00Z"
}
```

Observações importantes:
- Todos os usuários requerem email único
- Senha deve ter no mínimo 8 caracteres
- Planos devem existir no sistema
- Roles são atribuídas automaticamente baseado no plano
- Usuários inativos não podem acessar o sistema
- Verticais devem existir para usuários personalizados

2. Listar Usuários
```bash
GET /api/users/
```
Resposta:
```json
[
    {
        "id": 1,
        "username": "socrates",
        "email": "socrates@email.com",
        "plan": {
            "id": 2,
            "name": "Plano Premium"
        },
        "is_active": true,
        "date_joined": "2024-03-20T10:00:00Z"
    }
]
```
- Mostrar diferentes tipos de usuários:
  - Usuário Básico: Acesso apenas a conteúdo público
  - Usuário Premium: Acesso completo ao conteúdo PRO
  - Usuário Personalizado: Acesso a verticais específicas
  - Administrador: Acesso total ao sistema
  - Editor: Gerenciamento de conteúdo
  - Moderador: Moderação de comentários
- Explicar permissões e roles:
  - Roles:
    - ADMIN: Acesso total ao sistema
    - EDITOR: Gerenciamento de conteúdo
    - MODERATOR: Moderação de conteúdo
    - USER: Acesso básico
  - Permissões:
    - create_news: Criar notícias
    - edit_news: Editar notícias
    - delete_news: Excluir notícias
    - moderate_comments: Moderar comentários
    - manage_users: Gerenciar usuários
    - access_pro: Acesso a conteúdo PRO
  - Hierarquia de permissões:
    - Herança de permissões por role
    - Permissões específicas por usuário
    - Combinação de roles e permissões
  - Controle de acesso:
    - Verificação em nível de API
    - Validação em nível de modelo
    - Middleware de autenticação
    - Decoradores de permissão

## 3. Funcionalidades Especiais

### 3.1 Sistema de Assinaturas
- Planos afetam o acesso:
  - Básico: Apenas conteúdo público
  - Premium: Acesso a conteúdo PRO
  - Personalizado: Acesso a verticais específicas
- Conteúdo PRO vs. público:
  - Preview de conteúdo PRO
  - Paywall inteligente
  - Upgrade de plano
- Sistema de preços:
  - Preços por plano
  - Períodos de assinatura
  - Promoções e descontos

### 3.2 Upload de Imagens
- Processo de upload:
  - Validação de tipo e tamanho
  - Otimização automática
  - Geração de thumbnails
- Armazenamento:
  - Sistema de arquivos
  - CDN para distribuição
  - Backup automático
- URLs de acesso:
  - URLs públicas
  - Controle de acesso
  - Cache de imagens

### 3.3 Filtros e Busca
- Filtros por vertical:
  - Seleção múltipla
  - Ordenação
  - Paginação
- Busca por categoria:
  - Busca por texto
  - Filtros avançados
  - Resultados relevantes
- Paginação:
  - Controle de página
  - Tamanho de página
  - Navegação intuitiva

## 4. Documentação da API
- Swagger UI (/swagger/):
  - Interface interativa
  - Teste de endpoints
  - Exemplos de requisições
- ReDoc (/redoc/):
  - Documentação detalhada
  - Esquemas de dados
  - Exemplos de uso
- Uso da documentação:
  - Autenticação
  - Parâmetros
  - Respostas

## 5. Segurança
- Autenticação JWT:
  - Tokens seguros
  - Expiração
  - Renovação
- Permissões:
  - Roles e grupos
  - Controle de acesso
  - Validação de dados
- Proteção de rotas:
  - Middleware de autenticação
  - Rate limiting
  - CORS

## 6. Integração com Frontend
- Consumo da API:
  - Autenticação
  - Requisições
  - Tratamento de erros
- Exemplos de integração:
  - React
  - Vue.js
  - Angular
- Fluxo de autenticação:
  - Login
  - Refresh token
  - Logout

## 7. Próximos Passos
- Melhorias planejadas:
  - Cache de conteúdo
  - Sistema de comentários
  - Notificações
- Novas funcionalidades:
  - Newsletter
  - Compartilhamento
  - Analytics
- Roadmap do projeto:
  - Fase 1: Performance
  - Fase 2: Novas features
  - Fase 3: Escalabilidade 