# Guia de Deploy - SysSupport

## ⚠️ IMPORTANTE: Limitações do Vercel para Django

O Vercel é otimizado para aplicações serverless e tem algumas limitações importantes para projetos Django:

### 1. **Banco de Dados SQLite não persiste**
- O Vercel usa sistema de arquivos efêmero
- O banco SQLite será perdido a cada deploy
- **Solução**: Use banco de dados externo (PostgreSQL, MySQL)

### 2. **Arquivos de mídia não persistem**
- Uploads (assinaturas, memorandos) serão perdidos
- **Solução**: Use serviço de armazenamento em nuvem

### 3. **Recomendações de serviços gratuitos**

#### Banco de Dados (escolha um):
- **Supabase** (https://supabase.com/) - PostgreSQL gratuito
- **Railway** (https://railway.app/) - PostgreSQL/MySQL gratuito
- **PlanetScale** (https://planetscale.com/) - MySQL gratuito
- **ElephantSQL** (https://www.elephantsql.com/) - PostgreSQL gratuito

#### Armazenamento de Mídia (escolha um):
- **Cloudinary** (https://cloudinary.com/) - Gratuito até 25 GB
- **AWS S3** (https://aws.amazon.com/s3/) - 5 GB gratuito (12 meses)
- **Vercel Blob** (https://vercel.com/docs/storage/vercel-blob) - Pago
- **Supabase Storage** (https://supabase.com/) - 1 GB gratuito

## 📋 Passo a Passo Completo

### Passo 1: Configure um Banco de Dados Externo

#### Exemplo com Supabase (PostgreSQL):

1. Crie conta em https://supabase.com/
2. Crie um novo projeto
3. Copie a string de conexão do banco (Settings > Database > Connection String)
4. Instale o driver PostgreSQL:
   ```bash
   pip install psycopg2-binary
   ```
5. Adicione ao `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```

### Passo 2: Configure Armazenamento de Mídia

#### Exemplo com Cloudinary:

1. Crie conta em https://cloudinary.com/
2. Copie suas credenciais (Cloud Name, API Key, API Secret)
3. Instale o pacote:
   ```bash
   pip install cloudinary django-cloudinary-storage
   ```
4. Adicione ao `requirements.txt`:
   ```
   cloudinary==1.41.0
   django-cloudinary-storage==0.3.0
   ```

### Passo 3: Atualize settings.py

Adicione ao final do `sys_support/settings.py`:

```python
import os
import dj_database_url

# Database para produção
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }

# Cloudinary para mídia
if os.environ.get('CLOUDINARY_URL'):
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    
    INSTALLED_APPS += ['cloudinary_storage', 'cloudinary']
    
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
    
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

Adicione ao `requirements.txt`:
```
dj-database-url==2.2.0
```

### Passo 4: Inicialize o Repositório Git

```bash
git init
git add .
git commit -m "Preparando para deploy no Vercel"
```

### Passo 5: Faça Push para GitHub

```bash
# Crie um repositório no GitHub primeiro
git remote add origin https://github.com/seu-usuario/seu-repositorio.git
git branch -M main
git push -u origin main
```

### Passo 6: Configure o Projeto no Vercel

1. Acesse https://vercel.com/
2. Clique em "Add New" > "Project"
3. Importe seu repositório do GitHub
4. Configure as variáveis de ambiente:
   - `SECRET_KEY`: Gere uma nova chave (https://djecrety.ir/)
   - `DEBUG`: `False`
   - `DATABASE_URL`: String de conexão do banco (ex: Supabase)
   - `CLOUDINARY_CLOUD_NAME`: Nome da nuvem Cloudinary
   - `CLOUDINARY_API_KEY`: API Key do Cloudinary
   - `CLOUDINARY_API_SECRET`: API Secret do Cloudinary

### Passo 7: Deploy

1. Clique em "Deploy"
2. Aguarde o build terminar
3. Acesse o domínio fornecido (seu-projeto.vercel.app)

### Passo 8: Crie um Superusuário (Importante!)

Como não temos acesso SSH no Vercel, você precisa criar um comando customizado:

1. Crie um endpoint temporário para criar superusuário OU
2. Use o Django Admin após fazer o primeiro deploy e criar manualmente via interface

## 🔧 Comandos de Management Necessários

Após o primeiro deploy, você precisará executar:

```python
# Estes comandos são executados automaticamente pelo build_files.sh:
python manage.py migrate
python manage.py create_groups
python manage.py update_unidades
```

## 🚨 Troubleshooting

### Erro: "DisallowedHost"
- Adicione seu domínio Vercel ao `ALLOWED_HOSTS` em `settings.py`

### Erro: "Static files not found"
- Certifique-se de que `WhiteNoise` está instalado
- Execute `python manage.py collectstatic`

### Erro: "Database connection failed"
- Verifique se a variável `DATABASE_URL` está configurada corretamente
- Teste a conexão localmente primeiro

### Uploads não funcionam
- Verifique se o Cloudinary está configurado corretamente
- Teste as credenciais localmente

## 📝 Alternativas ao Vercel

Se você encontrar dificuldades com o Vercel, considere estas alternativas:

1. **Railway.app** - Muito mais simples para Django, suporta PostgreSQL nativo
2. **Render.com** - Suporte completo para Django, PostgreSQL incluído
3. **PythonAnywhere** - Especializado em Python/Django
4. **Heroku** - Clássico para Django (planos pagos)
5. **DigitalOcean App Platform** - Bom suporte para Django

## ✅ Checklist Final

- [ ] Banco de dados externo configurado
- [ ] Armazenamento de mídia configurado
- [ ] `requirements.txt` atualizado
- [ ] `settings.py` com configurações de produção
- [ ] Variáveis de ambiente configuradas no Vercel
- [ ] Repositório no GitHub
- [ ] Deploy realizado
- [ ] Superusuário criado
- [ ] Grupos e unidades criados
- [ ] Teste de upload de arquivos
- [ ] Teste de criação de chamados

## 📚 Recursos Úteis

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Cloudinary Django Integration](https://cloudinary.com/documentation/django_integration)
