# 🛠️ SysSupport

![Django](https://img.shields.io/badge/Django-5.2.7-green?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

SysSupport é um **sistema completo de gerenciamento de chamados de TI** construído com Django. Oferece controle total do ciclo de vida dos chamados entre Gestores, Técnicos e Administradores TI, com interface moderna e responsiva, API REST protegida com JWT, assinatura digital e recursos avançados de acessibilidade.

## ✨ Destaques

- 🎨 **Interface moderna** com Tailwind CSS e responsividade total (mobile-first)
- 🔐 **Autenticação robusta** com controle de permissões por grupos
- 📱 **API REST completa** com autenticação JWT
- ♿ **Acessibilidade** (tema claro/escuro, ajuste de fonte)
- ✍️ **Assinatura digital** em canvas HTML5
- 📊 **Dashboard** com filtros avançados e métricas
- 🚀 **Pronto para produção** (PythonAnywhere, Vercel, Railway)

## 🎯 Funcionalidades Principais

### 👥 Gestão de Usuários
- **Criação simplificada** de usuários (Gestores e Técnicos) por Administradores TI
- **Botão "Novo Usuário"** acessível no menu superior
- **Validação automática** de email e username únicos
- **Atribuição inteligente** de grupos e unidades organizacionais
- Perfis personalizados com matrícula e unidade

### 📋 Gestão de Chamados
- **Gestores**: Criam e acompanham chamados da sua unidade
- **Técnicos**: Visualizam chamados atribuídos e atualizam status (Em Andamento → Resolvida)
- **Administradores TI**: Controle total (visualização global, atribuição de técnicos, atualização de notas)
- **Finalização completa**: Avaliação por estrelas (1-5), observações, identificação do cliente final e assinatura digital

### 🔍 Filtros e Busca
- Filtro por **Status** (Aberta, Em Andamento, Resolvida, Fechada)
- Filtro por **Prioridade** (Baixa, Média, Alta, Crítica)
- Filtro por **Unidade Organizacional**
- Tempo de espera calculado automaticamente

### 📁 Uploads e Mídia
- Upload de **memorandos** (documentos)
- Captura de **assinatura digital** em canvas HTML5
- Armazenamento seguro em `/media/`

### 🎨 Interface e UX
- **Design moderno** com Tailwind CSS
- **Totalmente responsivo** (mobile, tablet, desktop)
- **Tema claro/escuro** com persistência
- **Ajuste de fonte** (pequena, normal, grande)
- **Ícones Font Awesome** para melhor visualização

### 🔌 API REST
- **Autenticação JWT** (access/refresh tokens)
- **Endpoints RESTful** completos para todas as operações
- **Permissões granulares** por grupo de usuário
- **Documentação** com Django REST Framework

## 🌐 Deploy em Produção

O SysSupport está pronto para deploy em diversas plataformas.

### 🐍 PythonAnywhere (Recomendado - Gratuito)

#### Passo a Passo Completo

1. **Crie uma conta em [PythonAnywhere](https://www.pythonanywhere.com/)** (plano gratuito)

2. **Abra um Bash Console** e clone o repositório:
   ```bash
   git clone https://github.com/SudoMaster7/SysSupport.git
   cd SysSupport
   ```

3. **Crie um ambiente virtual**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 atendimentos-env
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados MySQL** (na aba **Databases**):
   - Crie um banco chamado `default`
   - Anote: host, username, password

5. **Configure variáveis de ambiente** no console:
   ```bash
   export SECRET_KEY="sua-chave-secreta"
   export DEBUG="False"
   export DB_NAME="seu_usuario$default"
   export DB_USER="seu_usuario"
   export DB_PASSWORD="sua_senha_mysql"
   export DB_HOST="seu_usuario.mysql.pythonanywhere-services.com"
   export PYTHONANYWHERE_DOMAIN="seu_usuario.pythonanywhere.com"
   ```

6. **Execute migrações e comandos**:
   ```bash
   python manage.py migrate
   python manage.py create_groups
   python manage.py update_unidades
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

7. **Configure o WSGI** (aba **Web**):
   - Edite o arquivo WSGI e use o conteúdo de `wsgi_pythonanywhere.py`
   - Ajuste os caminhos para seu usuário

8. **Configure arquivos de mídia** (aba **Web > Static files**):
   - URL: `/media/`
   - Directory: `/home/seu_usuario/SysSupport/media/`

9. **Recarregue a aplicação** (botão **Reload**)

10. **Acesse**: `seu_usuario.pythonanywhere.com` 🎉

> 📚 **Guia detalhado**: Consulte `PASSO_A_PASSO_PYTHONANYWHERE.md`

---

### ▲ Vercel (Limitações para Django)

⚠️ **Atenção**: Vercel tem limitações importantes:
- ❌ SQLite não persiste (use PostgreSQL externo)
- ❌ Sistema de arquivos efêmero (use Cloudinary/S3 para mídia)
- ⚠️ Cold starts podem ser lentos

#### Deploy Rápido

```bash
# Instale Vercel CLI
npm i -g vercel

# Faça login
vercel login

# Deploy
vercel --prod
```

#### Variáveis de Ambiente (Vercel Dashboard)

- `SECRET_KEY`: Chave secreta Django
- `DEBUG`: `False`
- `DATABASE_URL`: URL do PostgreSQL externo

> 📚 **Guia completo**: Consulte `DEPLOY.md` e `QUICK_DEPLOY.md`

---

### 🚂 Outras Opções

| Plataforma | Gratuito | Banco de Dados | Mídia | Dificuldade |
|------------|----------|----------------|-------|-------------|
| **PythonAnywhere** | ✅ Sim | MySQL incluído | ✅ Suportado | ⭐ Fácil |
| **Railway** | 💳 $5 crédito | PostgreSQL | ✅ Suportado | ⭐⭐ Médio |
| **Render** | ✅ Sim | PostgreSQL | ⚠️ Configurar | ⭐⭐ Médio |
| **Heroku** | 💰 Pago | PostgreSQL | ⚠️ S3/Cloudinary | ⭐⭐⭐ Difícil |
| **VPS (DigitalOcean, etc)** | 💰 Pago | Qualquer | ✅ Suportado | ⭐⭐⭐⭐ Muito difícil |

## 📁 Estrutura do Projeto

```
📦 SysSupport/
├── 📂 accounts/              # Gestão de usuários, perfis e autenticação
│   ├── forms.py              # Formulários de criação/edição de usuários
│   ├── views.py              # Views de perfil e gestão
│   ├── mixins.py             # Permissões customizadas
│   └── management/commands/  # Comandos personalizados
├── 📂 chamados/              # Core: chamados de TI
│   ├── models.py             # Modelos (Chamado, Unidade)
│   ├── forms.py              # Formulários de chamados
│   ├── views.py              # Views web
│   ├── api_views.py          # API REST
│   ├── serializers.py        # Serialização DRF
│   └── tests.py              # Testes unitários
├── 📂 sys_support/           # Configurações do Django
│   ├── settings.py           # Configurações principais
│   ├── urls.py               # Roteamento principal
│   └── wsgi.py               # WSGI para produção
├── 📂 templates/             # Templates HTML
│   ├── base.html             # Template base (menu, footer, acessibilidade)
│   ├── chamados/             # Templates de chamados
│   ├── accounts/             # Templates de usuários
│   └── registration/         # Login
├── 📂 static/                # Arquivos estáticos
│   └── js/
│       ├── accessibility.js  # Tema e fonte
│       └── signature.js      # Captura de assinatura
├── 📂 media/                 # Uploads (memorandos, assinaturas)
├── 📄 requirements.txt       # Dependências Python
├── 📄 manage.py              # CLI do Django
├── 📄 vercel.json            # Config para Vercel
└── 📄 README.md              # Este arquivo
```

## 🚀 Instalação e Configuração Local

### Pré-requisitos
- Python 3.10+ (recomendado: 3.13)
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/SudoMaster7/SysSupport.git
   cd SysSupport
   ```

2. **Crie e ative o ambiente virtual**
   ```powershell
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   
   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente** (opcional para desenvolvimento)
   ```bash
   # Crie um arquivo .env na raiz do projeto
   SECRET_KEY=sua-chave-secreta-aqui
   DEBUG=True
   ```

5. **Execute as migrações**
   ```bash
   python manage.py migrate
   ```

6. **Crie grupos e unidades organizacionais**
   ```bash
   python manage.py create_groups
   python manage.py update_unidades
   ```

7. **Crie um superusuário (Administrador TI)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Inicie o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```

9. **Acesse a aplicação**
   - 🌐 Interface Web: `http://127.0.0.1:8000/`
   - 🔧 Admin Django: `http://127.0.0.1:8000/admin/`
   - 🔌 API: `http://127.0.0.1:8000/api/`

## 👤 Criando Novos Usuários

### 🖥️ Via Interface Web (Recomendado)

1. **Faça login** como **Administrador TI**
2. Clique no botão **"Novo Usuário"** (ícone 👤➕) no menu superior
3. **Preencha o formulário**:
   - 🔑 **Login**: Nome de usuário, e-mail e senha (com confirmação)
   - 👤 **Dados Pessoais**: Nome e sobrenome
   - 🏢 **Organização**: Matrícula (opcional) e Unidade
   - 🔖 **Perfil**: Selecione "Gestor" ou "Técnico"
4. Clique em **"Criar Usuário"**
5. ✅ Confirmação e retorno ao formulário para novos cadastros

### ⚙️ Via Django Admin

1. Acesse `/admin/` com credenciais de superusuário
2. Em **Autenticação > Usuários**, clique em **Adicionar**
3. Configure **username** e **senha**
4. Atribua **grupos** (Gestor, Técnico ou Administrador TI)
5. Configure **perfil** (matrícula e unidade) no inline

### ✔️ Validações Automáticas

- ✅ Nomes de usuário **únicos**
- ✅ E-mails **únicos**
- ✅ Senhas **diferentes** (confirmação obrigatória)
- ✅ Matrícula opcional, **unidade obrigatória**
- 🔒 Apenas **Administradores TI** podem criar usuários

## 🔌 API REST

A API utiliza **Django REST Framework** com autenticação **JWT (JSON Web Tokens)**.

### 🔐 Autenticação

```bash
# Obter tokens (access + refresh)
POST /api/auth/login/
{
  "username": "seu_usuario",
  "password": "sua_senha"
}

# Resposta
{
  "access": "eyJ0eXAiOiJKV1QiLC...",
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}

# Renovar token de acesso
POST /api/auth/refresh/
{
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

### 📡 Endpoints Principais

| Método | Endpoint | Permissão | Descrição |
|--------|----------|-----------|-----------|
| `GET` | `/api/chamados/` | Todos | Lista chamados (filtrado por permissões) |
| `POST` | `/api/chamados/` | Gestor | Cria novo chamado |
| `GET` | `/api/chamados/{id}/` | Relacionados | Detalhes do chamado |
| `PATCH` | `/api/chamados/{id}/atualizar/` | Admin TI | Atualiza status, notas e técnicos |
| `POST` | `/api/chamados/{id}/finalizar/` | Gestor solicitante | Finaliza com avaliação |
| `GET` | `/api/unidades/` | Admin TI | Lista unidades |
| `POST` | `/api/unidades/` | Admin TI | Cria unidade |
| `GET` | `/api/users/` | Admin TI | Lista usuários |
| `POST` | `/api/users/` | Admin TI | Cria usuário |

### 💡 Exemplo de Uso

```bash
# 1. Fazer login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "senha123"}'

# 2. Listar chamados (usando o token)
curl -X GET http://localhost:8000/api/chamados/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLC..."

# 3. Criar chamado
curl -X POST http://localhost:8000/api/chamados/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLC..." \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Computador não liga",
    "descricao": "Máquina da sala 10 não está funcionando",
    "prioridade": "Alta",
    "unidade": 1
  }'
```

## 🧪 Testes

O projeto inclui **testes unitários completos** para o fluxo de chamados.

### Executar Todos os Testes

```bash
python manage.py test chamados.tests
```

### Executar com Verbosidade

```bash
python manage.py test chamados.tests -v 2
```

### Cobertura de Testes

- ✅ Criação de chamados
- ✅ Atualização de status por técnicos
- ✅ Finalização com avaliação
- ✅ Permissões por grupo de usuário
- ✅ Validações de formulários
- ✅ API REST (endpoints protegidos)

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.7** - Framework web Python
- **Django REST Framework 3.16.1** - API REST
- **djangorestframework-simplejwt 5.4.0** - Autenticação JWT
- **Pillow 11.1.0** - Processamento de imagens
- **mysqlclient 2.2.7** - Conector MySQL

### Frontend
- **Tailwind CSS 3.4** (via CDN) - Framework CSS
- **Font Awesome 6.6.0** - Ícones
- **Lightbox2** - Visualização de imagens
- **Signature Pad** - Captura de assinatura

### Deploy
- **WhiteNoise 6.11.0** - Servir arquivos estáticos
- **Gunicorn 23.0.0** - Servidor WSGI

## 📝 Notas Adicionais

- ✅ Grupos (`Gestor`, `Administrador TI`, `Técnico`) são criados automaticamente via `post_migrate` signal
- ✅ 62+ unidades organizacionais pré-cadastradas via comando `update_unidades`
- ✅ Assinaturas são capturadas em canvas HTML5 e salvas como PNG via base64
- ✅ Tema escuro e ajuste de fonte persistem via `localStorage`
- ⚠️ Em produção, configure:
  - HTTPS obrigatório
  - Armazenamento seguro para uploads
  - Backup regular do banco de dados
  - Limitação de tamanho de uploads
  - Verificação antivírus para arquivos

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os passos:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Leonardo Brito**
- GitHub: [@SudoMaster7](https://github.com/SudoMaster7)
- Projeto: [SysSupport](https://github.com/SudoMaster7/SysSupport)

---

<div align="center">

**Feito com ❤️ usando Django**

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐

</div>
```}```}