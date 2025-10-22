# 🚀 Deploy no PythonAnywhere - Guia Completo

## Por que PythonAnywhere?
- ✅ 100% GRATUITO (sem cartão)
- ✅ Especializado em Python/Django
- ✅ MySQL incluído
- ✅ Não precisa configurar nada de banco externo
- ✅ Mais fácil de usar

## 📋 Passo a Passo Completo

### 1. Crie uma Conta Gratuita

1. Acesse: https://www.pythonanywhere.com/
2. Clique em "Pricing & signup"
3. Escolha o plano **"Beginner"** (Free)
4. Preencha o formulário (não precisa cartão)
5. Confirme seu email

### 2. Prepare o Projeto Localmente

#### 2.1. Atualize o settings.py

Adicione ao final de `sys_support/settings.py`:

```python
# PythonAnywhere Configuration
ALLOWED_HOSTS += ['.pythonanywhere.com']

# Database para PythonAnywhere (MySQL)
if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'seu_usuario$default'),
            'USER': os.environ.get('DB_USER', 'seu_usuario'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST', 'seu_usuario.mysql.pythonanywhere-services.com'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }
```

#### 2.2. Instale o driver MySQL

```bash
.\.venv\Scripts\python.exe -m pip install mysqlclient
```

#### 2.3. Atualize o requirements.txt

```bash
.\.venv\Scripts\python.exe -m pip freeze > requirements.txt
```

#### 2.4. Faça commit e push para GitHub

```bash
git add .
git commit -m "Preparando para PythonAnywhere"
git push
```

### 3. Configure no PythonAnywhere

#### 3.1. Abra um Console Bash

1. Faça login em PythonAnywhere
2. Clique na aba **"Consoles"**
3. Clique em **"Bash"** para abrir um terminal

#### 3.2. Clone seu repositório

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

#### 3.3. Crie um Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 seu-projeto-env
workon seu-projeto-env
```

#### 3.4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados

#### 4.1. Crie o banco MySQL

1. Vá na aba **"Databases"**
2. Na seção **"MySQL"**, defina uma senha
3. Clique em **"Initialize MySQL"**
4. Anote:
   - **Nome do banco**: `seu_usuario$default`
   - **Host**: `seu_usuario.mysql.pythonanywhere-services.com`
   - **Senha**: a que você definiu

#### 4.2. Execute as migrações

No console Bash:

```bash
cd ~/SEU-REPOSITORIO
workon seu-projeto-env

# Configure variáveis de ambiente
export DB_PASSWORD='sua_senha_mysql'
export DB_NAME='seu_usuario$default'
export DB_USER='seu_usuario'
export DB_HOST='seu_usuario.mysql.pythonanywhere-services.com'
export PYTHONANYWHERE_DOMAIN='True'
export SECRET_KEY='xx)5!e&+r2&dl@i^#394ylrmrbk+nzzub(_s@b!a@n*9g88_v('

# Execute as migrações
python manage.py migrate

# Crie grupos e unidades
python manage.py create_groups
python manage.py update_unidades

# Colete arquivos estáticos
python manage.py collectstatic --noinput

# Crie um superusuário
python manage.py createsuperuser
```

### 5. Configure o Web App

#### 5.1. Adicione um Web App

1. Clique na aba **"Web"**
2. Clique em **"Add a new web app"**
3. Escolha **"Manual configuration"**
4. Escolha **Python 3.10**

#### 5.2. Configure o WSGI

1. Na página do Web App, clique no link do arquivo WSGI
2. **Delete todo o conteúdo** do arquivo
3. Cole o seguinte código:

```python
import os
import sys

# Adicione o diretório do projeto ao path
path = '/home/seu_usuario/SEU-REPOSITORIO'
if path not in sys.path:
    sys.path.append(path)

# Configure as variáveis de ambiente
os.environ['DJANGO_SETTINGS_MODULE'] = 'sys_support.settings'
os.environ['DB_PASSWORD'] = 'sua_senha_mysql'
os.environ['DB_NAME'] = 'seu_usuario$default'
os.environ['DB_USER'] = 'seu_usuario'
os.environ['DB_HOST'] = 'seu_usuario.mysql.pythonanywhere-services.com'
os.environ['PYTHONANYWHERE_DOMAIN'] = 'True'
os.environ['SECRET_KEY'] = 'xx)5!e&+r2&dl@i^#394ylrmrbk+nzzub(_s@b!a@n*9g88_v('

# Configure o Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Salve (Ctrl+S ou botão Save)

#### 5.3. Configure o Virtual Environment

Na página do Web App:
1. Na seção **"Virtualenv"**, clique em **"Enter path to a virtualenv"**
2. Digite: `/home/seu_usuario/.virtualenvs/seu-projeto-env`
3. Marque o check ✓

#### 5.4. Configure Arquivos Estáticos

Na página do Web App, na seção **"Static files"**:

1. Adicione:
   - **URL**: `/static/`
   - **Directory**: `/home/seu_usuario/SEU-REPOSITORIO/staticfiles`

2. Adicione:
   - **URL**: `/media/`
   - **Directory**: `/home/seu_usuario/SEU-REPOSITORIO/media`

### 6. Recarregue o Web App

1. Role até o topo da página do Web App
2. Clique no grande botão verde **"Reload seu_usuario.pythonanywhere.com"**
3. Aguarde alguns segundos

### 7. Teste sua Aplicação

Acesse: `https://seu_usuario.pythonanywhere.com/`

## 🎉 Pronto! Seu projeto está no ar!

## 🔧 Comandos Úteis

### Atualizar o código (após fazer push no GitHub)

```bash
cd ~/SEU-REPOSITORIO
git pull
workon seu-projeto-env
python manage.py migrate
python manage.py collectstatic --noinput
```

Depois, clique em **"Reload"** no Web App.

### Ver logs de erro

1. Vá na aba **"Web"**
2. Role até **"Log files"**
3. Clique em **"Error log"** ou **"Server log"**

### Acessar o console Python

```bash
workon seu-projeto-env
cd ~/SEU-REPOSITORIO
python manage.py shell
```

## 🆘 Problemas Comuns

### Erro 500
- Verifique os logs (Error log e Server log)
- Certifique-se de que o WSGI está configurado corretamente
- Verifique se o virtualenv está ativado

### Banco de dados não conecta
- Verifique as variáveis de ambiente no arquivo WSGI
- Certifique-se de que a senha do MySQL está correta
- Teste a conexão no console MySQL

### Arquivos estáticos não carregam
- Execute `python manage.py collectstatic`
- Verifique os caminhos na configuração de Static files
- Clique em Reload

### ImportError ou ModuleNotFoundError
- Certifique-se de que instalou todas as dependências
- Verifique se o virtualenv está configurado corretamente
- Execute `pip install -r requirements.txt` novamente

## 📊 Limitações do Plano Gratuito

- ⏱️ 100 segundos de CPU por dia (suficiente para projetos pequenos)
- 💾 512MB de espaço em disco
- 🗄️ 1 app web
- 👤 Sem domínio personalizado (só .pythonanywhere.com)
- 🔄 App não hiberna (sempre disponível!)

## 🎓 Dicas

1. **Use o console Bash** para tudo (é mais fácil)
2. **Sempre faça git pull** antes de fazer alterações
3. **Sempre clique em Reload** após mudanças
4. **Verifique os logs** se algo der errado
5. **Backup do banco** periodicamente

## 📚 Recursos

- [Documentação PythonAnywhere](https://help.pythonanywhere.com/)
- [Tutorial Django no PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [FAQ](https://help.pythonanywhere.com/pages/FAQ/)

## ✅ Checklist Final

- [ ] Conta criada no PythonAnywhere
- [ ] Repositório no GitHub
- [ ] settings.py atualizado
- [ ] mysqlclient instalado
- [ ] requirements.txt atualizado
- [ ] Repositório clonado
- [ ] Virtual environment criado
- [ ] Dependências instaladas
- [ ] Banco MySQL configurado
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Arquivos estáticos coletados
- [ ] WSGI configurado
- [ ] Virtual environment configurado no Web App
- [ ] Static files configurados
- [ ] Web App recarregado
- [ ] Aplicação testada

🎊 **Parabéns! Seu projeto Django está online e gratuito!**
