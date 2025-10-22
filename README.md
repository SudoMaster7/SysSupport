# SysSupport

SysSupport é uma aplicação web construída com Django para gerenciar o ciclo de vida de chamados de suporte de TI entre Gestores de Unidade, técnicos e a equipe administrativa de TI. O projeto inclui interface web responsiva (Tailwind CSS via CDN), API REST protegida com JWT, formulários com assinatura digital e controles de acessibilidade.

## Funcionalidades principais

- **Autenticação e perfis**: usa `django.contrib.auth` com perfis (`Profile`) associados a unidades. Grupos padrão (`Gestor`, `Administrador TI`, `Tecnico`) são criados automaticamente após as migrações.
- **Gestão de usuários**: 
  - Administradores TI podem criar novos usuários (Gestores e Técnicos) diretamente pela interface web.
  - Novo botão "Novo Usuário" no menu superior (com ícone de usuário +).
  - Formulário com validação de email e nome de usuário únicos.
  - Atribuição automática de grupos e associação a unidades organizacionais.
- **Gestão de chamados**:
  - Gestores criam chamados vinculados à sua unidade e acompanham apenas os próprios registros.
  - Administradores TI visualizam todos os chamados, atualizam status, atribuem técnicos e registram notas.
  - Técnicos visualizam chamados atribuídos e podem atualizar o status para "Em Andamento" ou "Resolvida".
  - Finalização com avaliação (1–5), observação opcional, identificação do cliente final e captura de assinatura em canvas.
- **Uploads e mídia**: memorandos e assinaturas são armazenados em `MEDIA_ROOT` (`media/`).
- **Painel web**: listagem com filtro por status/prioridade/unidade, detalhes do chamado e formulários (criação, atualização, finalização) com validação server-side.
- **API REST**: endpoints baseados em Django REST Framework com autenticação via JWT (`/api/auth/login/`) e permissões por grupo.
- **Acessibilidade**: botão flutuante para alternar tema claro/escuro e ajustar tamanho da fonte com persistência via `localStorage`.

## Deploy no Vercel

### Pré-requisitos
- Conta no [Vercel](https://vercel.com/)
- [Vercel CLI](https://vercel.com/docs/cli) instalado (opcional)
- Git instalado

### Passos para Deploy

1. **Inicialize o repositório Git (se ainda não tiver)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Faça push para GitHub/GitLab/Bitbucket**
   ```bash
   git remote add origin <seu-repositorio>
   git push -u origin main
   ```

3. **Configure variáveis de ambiente no Vercel**
   - Acesse [vercel.com](https://vercel.com/)
   - Importe seu repositório
   - Vá em **Settings > Environment Variables**
   - Adicione:
     - `SECRET_KEY`: gere uma nova chave secreta segura
     - `DEBUG`: defina como `False` para produção
     - Outras variáveis necessárias

4. **Deploy automático**
   - O Vercel detectará automaticamente o projeto Django
   - O build será executado usando `build_files.sh`
   - A aplicação estará disponível em `seu-projeto.vercel.app`

### Deploy via CLI (alternativo)

```bash
# Instale o Vercel CLI
npm i -g vercel

# Faça login
vercel login

# Deploy
vercel

# Deploy para produção
vercel --prod
```

### Notas importantes sobre Vercel

⚠️ **ATENÇÃO**: O Vercel tem limitações para aplicações Django:

1. **Banco de dados**: SQLite não persiste entre deploys. Use:
   - PostgreSQL (Vercel Postgres, Supabase, Railway, etc.)
   - MySQL/MariaDB hospedado externamente

2. **Arquivos de mídia**: O sistema de arquivos é efêmero. Configure:
   - Cloudinary
   - AWS S3
   - Vercel Blob Storage
   - Outro serviço de armazenamento em nuvem

3. **Sessões**: Configure para usar banco de dados ou cache Redis

### Configuração recomendada para produção

Adicione ao `settings.py` (já configurado):
- WhiteNoise para arquivos estáticos
- Variáveis de ambiente para configurações sensíveis
- ALLOWED_HOSTS configurado para `.vercel.app`

## Estrutura de pastas (resumo)

```
accounts/        # Perfil de usuários e integrações com admin
chamados/        # Domínio de chamados, API, formulários e testes
sys_support/     # Configurações do projeto Django
templates/       # Templates base, auth e páginas de chamados
static/js/       # Scripts de acessibilidade e assinatura
media/           # Diretório padrão para uploads (assinaturas, memorandos)
vercel.json      # Configuração de deploy para Vercel
build_files.sh   # Script de build para Vercel
```

## Pré-requisitos

- Python 3.13 (virtualenv configurado em `.venv/`)
- Pip

## Configuração Local

1. **Instale as dependências**

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

2. **Aplique as migrações**

   ```powershell
   .\.venv\Scripts\python.exe manage.py migrate
   ```

3. **Crie grupos e unidades**

   ```powershell
   .\.venv\Scripts\python.exe manage.py create_groups
   .\.venv\Scripts\python.exe manage.py update_unidades
   ```

4. **Crie um superusuário**

   ```powershell
   .\.venv\Scripts\python.exe manage.py createsuperuser
   ```

5. **Execute o servidor de desenvolvimento**

   ```powershell
   .\.venv\Scripts\python.exe manage.py runserver
   ```

A aplicação estará disponível em `http://127.0.0.1:8000/`.

## Criando Novos Usuários

### Via Interface Web (Recomendado)
1. Faça login como **Administrador TI**
2. Clique no botão **"Novo Usuário"** (ícone de usuário com +) no canto superior direito da página
3. Preencha o formulário com as seguintes informações:
   - **Dados de Login**: Nome de usuário, e-mail e senha (com confirmação)
   - **Dados Pessoais**: Nome e sobrenome
   - **Dados Organizacionais**: Matrícula (opcional) e Unidade
   - **Perfil (Grupo)**: Selecione "Gestor" ou "Técnico"
4. Clique em "Criar Usuário"
5. A página confirmará a criação e voltará ao formulário para criar mais usuários se necessário

### Via Django Admin
1. Acesse `/admin/` com credenciais de superusuário
2. Em **Autenticação e Autorização > Usuários**, clique em **Adicionar usuário**
3. Configure nome de usuário e senha
4. Na página de edição, configure grupos (Gestor, Técnico, ou Administrador TI)
5. No inline **Profiles**, configure matrícula e unidade

### Validações e Restrições
- Nomes de usuário devem ser únicos
- E-mails devem ser únicos
- Senhas devem ser diferentes
- Matrícula é opcional, mas unidade é obrigatória
- Apenas Administradores TI podem criar novos usuários

## API REST

Use autenticação JWT (SimpleJWT):

- `POST /api/auth/login/` – obtém `access` e `refresh` tokens
- `POST /api/auth/refresh/` – renova o token de acesso

Endpoints principais:

- `POST /api/chamados/` (Gestor) – cria chamado
- `GET /api/chamados/` – lista chamados (filtrados por permissões)
- `GET /api/chamados/{id}/` – detalha chamado
- `PATCH /api/chamados/{id}/atualizar/` (Admin TI) – atualiza status, notas e designações
- `POST /api/chamados/{id}/finalizar/` (Gestor solicitante) – encerra chamado com avaliação e assinatura
- `GET/POST /api/unidades/` (Admin TI) – gerencia unidades
- `GET/POST /api/users/` (Admin TI) – gerencia usuários e grupos

## Testes

O projeto inclui testes unitários focados no fluxo de chamados (criação, atualização e finalização). Execute-os com:

```powershell
.\.venv\Scripts\python.exe manage.py test chamados.tests
```

## Notas adicionais

- Os grupos `Gestor`, `Administrador TI` e `Tecnico` são criados automaticamente ao aplicar migrações (`post_migrate`).
- Para capturar assinaturas na web, a página de finalização usa `signature_pad` (CDN) e envia os dados em base64; o backend converte e salva como imagem.
- Ajuste `ALLOWED_HOSTS` no `settings.py` para o ambiente de produção apropriado.
- Caso utilize deploy em produção, configure armazenamento seguro para arquivos, HTTPS e proteção de uploads (antivírus, limitação de tamanho, etc.).
```}```}