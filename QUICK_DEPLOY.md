# 🚀 GUIA RÁPIDO DE DEPLOY NO VERCEL

## ✅ Preparação Completa

Todos os arquivos necessários foram criados:
- ✅ `vercel.json` - Configuração do Vercel
- ✅ `build_files.sh` - Script de build
- ✅ `.gitignore` - Arquivos a ignorar no Git
- ✅ `.vercelignore` - Arquivos a ignorar no Vercel
- ✅ `requirements.txt` - Dependências atualizadas (whitenoise, gunicorn)
- ✅ `settings.py` - Configurado para produção
- ✅ `wsgi.py` - Compatível com Vercel
- ✅ `README.md` - Documentação completa
- ✅ `DEPLOY.md` - Guia detalhado de deploy

## 🔑 SECRET KEY GERADA

```
xx)5!e&+r2&dl@i^#394ylrmrbk+nzzub(_s@b!a@n*9g88_v(
```

**IMPORTANTE:** Guarde esta chave em segredo e use-a no Vercel!

## ⚠️ ATENÇÃO: Limitações do Vercel

O Vercel NÃO é ideal para Django por causa de:
1. **SQLite não persiste** - Banco de dados é perdido a cada deploy
2. **Arquivos de mídia não persistem** - Uploads são perdidos
3. **Cold starts** - Primeira requisição pode ser lenta

### 🎯 Recomendação: Use Railway.app ao invés do Vercel

**Railway** é MUITO mais simples para Django:
- ✅ PostgreSQL incluído gratuitamente
- ✅ Arquivos persistem
- ✅ Deploy mais simples
- ✅ Melhor para aplicações com banco de dados

## 📋 Passos para Deploy no Vercel (se ainda quiser usar)

### 1. Configure Banco de Dados Externo (OBRIGATÓRIO)
   
Escolha um (recomendado: **Supabase**):
- Supabase (PostgreSQL) - https://supabase.com/
- Railway (PostgreSQL/MySQL) - https://railway.app/
- ElephantSQL (PostgreSQL) - https://www.elephantsql.com/

**Exemplo Supabase:**
1. Crie conta em https://supabase.com/
2. Crie um projeto
3. Copie a string de conexão (URI format)
4. Exemplo: `postgresql://user:pass@host:port/database`

### 2. Configure Armazenamento de Mídia (OBRIGATÓRIO)

Escolha um (recomendado: **Cloudinary**):
- Cloudinary - https://cloudinary.com/ (25GB grátis)
- AWS S3 - https://aws.amazon.com/s3/
- Supabase Storage - https://supabase.com/

**Exemplo Cloudinary:**
1. Crie conta em https://cloudinary.com/
2. Copie: Cloud Name, API Key, API Secret
3. Será usado nas variáveis de ambiente

### 3. Instale Dependências Adicionais

```bash
.\.venv\Scripts\python.exe -m pip install psycopg2-binary cloudinary django-cloudinary-storage dj-database-url
```

Atualize `requirements.txt`:
```bash
.\.venv\Scripts\python.exe -m pip freeze > requirements.txt
```

### 4. Atualize settings.py

Adicione ao final do arquivo `sys_support/settings.py`:

```python
import dj_database_url

# Database para produção
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }

# Cloudinary para mídia
if os.environ.get('CLOUDINARY_URL'):
    INSTALLED_APPS += ['cloudinary_storage', 'cloudinary']
    
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
    
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

### 5. Inicialize Git e Faça Push

```bash
git init
git add .
git commit -m "Preparando para deploy"

# Crie um repositório no GitHub e depois:
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
git branch -M main
git push -u origin main
```

### 6. Configure no Vercel

1. Acesse https://vercel.com/
2. Faça login com GitHub
3. Clique em "Add New" > "Project"
4. Importe seu repositório
5. Configure variáveis de ambiente:
   - `SECRET_KEY`: `xx)5!e&+r2&dl@i^#394ylrmrbk+nzzub(_s@b!a@n*9g88_v(`
   - `DEBUG`: `False`
   - `DATABASE_URL`: (sua string do Supabase/Railway)
   - `CLOUDINARY_CLOUD_NAME`: (do Cloudinary)
   - `CLOUDINARY_API_KEY`: (do Cloudinary)
   - `CLOUDINARY_API_SECRET`: (do Cloudinary)

6. Clique em "Deploy"

### 7. Após Deploy

Acesse: `https://seu-projeto.vercel.app/`

## 🎯 ALTERNATIVA RECOMENDADA: Railway.app

Se você quer algo mais simples, use Railway:

```bash
# Instale Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy (cria projeto e banco automaticamente!)
railway up
```

Railway é MUITO mais fácil porque:
- PostgreSQL já vem configurado
- Não precisa configurar armazenamento externo
- Deploy mais rápido
- Melhor para Django

## 📚 Próximos Passos

1. [ ] Criar conta no Supabase (banco) ou Railway (tudo-em-um)
2. [ ] Criar conta no Cloudinary (mídia) se usar Vercel
3. [ ] Atualizar settings.py com configurações de produção
4. [ ] Fazer commit e push para GitHub
5. [ ] Fazer deploy no Vercel/Railway
6. [ ] Testar a aplicação online
7. [ ] Criar superusuário na produção

## 🆘 Precisa de Ajuda?

Consulte:
- `DEPLOY.md` - Guia detalhado completo
- `README.md` - Documentação do projeto
- https://docs.djangoproject.com/en/5.2/howto/deployment/

## ✨ Dica Final

Para um deploy mais simples e rápido, recomendo **fortemente** usar Railway.app ao invés do Vercel. O Railway é feito para aplicações com banco de dados e você não vai ter dor de cabeça com persistência de dados!
