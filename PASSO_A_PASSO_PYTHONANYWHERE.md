# 🚀 DEPLOY NO PYTHONANYWHERE - SIGA ESTES PASSOS

## ✅ PREPARAÇÃO LOCAL CONCLUÍDA!

O projeto já está pronto para deploy. Agora siga estes passos:

---

## 📝 PASSO 1: Criar Conta no PythonAnywhere

1. Acesse: **https://www.pythonanywhere.com/**
2. Clique em **"Pricing & signup"**
3. Escolha o plano **"Beginner"** (FREE - $0/month)
4. Preencha:
   - Username (anote esse nome! Será usado em várias etapas)
   - Email
   - Senha
5. Confirme seu email
6. Faça login

✅ **ANOTAÇÃO IMPORTANTE:**
```
Meu username PythonAnywhere: ___________________
```

---

## 📝 PASSO 2: Subir o Código para o GitHub

Você precisa criar um repositório no GitHub primeiro.

### 2.1. No GitHub (https://github.com):

1. Faça login
2. Clique no **"+"** no canto superior direito
3. Clique em **"New repository"**
4. Preencha:
   - Repository name: `atendimentos` (ou outro nome)
   - Description: `Sistema de Chamados Django`
   - Deixe como **Public**
   - **NÃO** marque "Initialize with README"
5. Clique em **"Create repository"**

✅ **ANOTAÇÃO:**
```
URL do meu repositório: ___________________
```

### 2.2. No seu computador (PowerShell):

Execute estes comandos um por vez:

```powershell
# Configure seu nome e email (substitua pelos seus dados)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Conecte ao GitHub (substitua pela URL do seu repositório)
git remote add origin https://github.com/SEU-USUARIO/atendimentos.git

# Renomeie a branch para main
git branch -M main

# Faça push
git push -u origin main
```

**Quando pedir credenciais:**
- Username: seu usuário do GitHub
- Password: use um **Personal Access Token** (não a senha!)
  - Gere em: https://github.com/settings/tokens
  - Clique em "Generate new token (classic)"
  - Marque "repo"
  - Copie o token e use como senha

---

## 📝 PASSO 3: Configurar MySQL no PythonAnywhere

1. No PythonAnywhere, clique na aba **"Databases"**
2. Na seção **"MySQL"**:
   - Digite uma senha forte
   - Clique em **"Initialize MySQL"**
3. Aguarde alguns segundos

✅ **ANOTAÇÕES IMPORTANTES:**
```
Senha do MySQL: terilo0825
Nome do banco: leonardobritoo$default
Host: leonardobritoo.mysql.pythonanywhere-services.com
User: leonardobritoo
```

---

## 📝 PASSO 4: Clonar o Projeto no PythonAnywhere

### 4.1. Abrir Console Bash

1. No PythonAnywhere, clique na aba **"Consoles"**
2. Clique em **"Bash"** (abrirá um terminal)

### 4.2. Clonar e Configurar

**Cole estes comandos no console Bash** (um por vez):

```bash
# Clone seu repositório (substitua pela sua URL)
git clone https://github.com/SEU-USUARIO/atendimentos.git
cd atendimentos

# Crie o virtual environment
mkvirtualenv --python=/usr/bin/python3.10 atendimentos-env

# Ative o ambiente (sempre use este comando quando entrar no console)
workon atendimentos-env

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente (SUBSTITUA OS VALORES!)
export DB_PASSWORD='terilo0825'
export DB_NAME='leonardobritoo$default'
export DB_USER='leonardobritoo'
export DB_HOST='leonardobritoo.mysql.pythonanywhere-services.com'
export PYTHONANYWHERE_DOMAIN='True'
export SECRET_KEY='xx)5!e&+r2&dl@i^#394ylrmrbk+nzzub(_s@b!a@n*9g88_v('
export DEBUG='False'

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

**No último comando, preencha:**
- Username: (escolha um)
- Email: (seu email)
- Password: Terilo0825

---

## 📝 PASSO 5: Configurar o Web App

### 5.1. Criar Web App

1. Clique na aba **"Web"**
2. Clique em **"Add a new web app"**
3. Na tela "Your web app's domain name", clique **"Next"**
4. Escolha **"Manual configuration"**
5. Escolha **"Python 3.10"**
6. Clique **"Next"**

### 5.2. Configurar o Virtual Environment

Na página do Web App:
1. Role até a seção **"Virtualenv"**
2. Clique em **"Enter path to a virtualenv"**
3. Digite: `/home/seu_usuario/.virtualenvs/atendimentos-env`
   (Substitua `seu_usuario` pelo seu username PythonAnywhere)
4. Clique no ✓

### 5.3. Configurar Arquivos Estáticos

Na seção **"Static files"**:

**Adicione dois mapeamentos:**

1. Primeiro mapeamento:
   - URL: `/static/`
   - Directory: `/home/seu_usuario/atendimentos/staticfiles`
   - (Substitua `seu_usuario`)

2. Segundo mapeamento:
   - URL: `/media/`
   - Directory: `/home/seu_usuario/atendimentos/media`
   - (Substitua `seu_usuario`)

### 5.4. Configurar o WSGI

1. Na seção **"Code"**, clique no link do arquivo WSGI:
   - Exemplo: `/var/www/seu_usuario_pythonanywhere_com_wsgi.py`
2. **DELETE TODO O CONTEÚDO** do arquivo
3. Cole este código (SUBSTITUA `seu_usuario` em TODOS os lugares):

```python
import os
import sys

# Adicione o diretório do projeto ao path
path = '/home/seu_usuario/atendimentos'
if path not in sys.path:
    sys.path.append(path)

# Configure as variáveis de ambiente (SUBSTITUA OS VALORES!)
os.environ['DJANGO_SETTINGS_MODULE'] = 'sys_support.settings'
os.environ['DB_PASSWORD'] = 'sua_senha_mysql'
os.environ['DB_NAME'] = 'seu_usuario$default'
os.environ['DB_USER'] = 'seu_usuario'
os.environ['DB_HOST'] = 'seu_usuario.mysql.pythonanywhere-services.com'
os.environ['PYTHONANYWHERE_DOMAIN'] = 'True'
os.environ['SECRET_KEY'] = 'xx)5!e&+r2&dl@i^#394ylrmrbk+nzzub(_s@b!a@n*9g88_v('
os.environ['DEBUG'] = 'False'

# Configure o Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Clique em **"Save"** (Ctrl+S)

---

## 📝 PASSO 6: Lançar o Site!

1. Role até o topo da página do Web App
2. Clique no grande botão verde **"Reload seu_usuario.pythonanywhere.com"**
3. Aguarde 5-10 segundos
4. Clique no link: **seu_usuario.pythonanywhere.com**

## 🎉 SEU SITE ESTÁ NO AR!

Acesse: `https://seu_usuario.pythonanywhere.com/`

---

## 🆘 SE DER ERRO

### Ver os logs:

1. Na aba **"Web"**, role até **"Log files"**
2. Clique em:
   - **"Error log"** - erros do Django
   - **"Server log"** - erros do servidor

### Problemas comuns:

**Erro 500 (Internal Server Error):**
1. Verifique o Error log
2. Certifique-se de que todas as variáveis no WSGI estão corretas
3. Verifique se o caminho do virtualenv está correto

**"DisallowedHost":**
1. Isso não deve acontecer pois já está configurado
2. Se acontecer, adicione seu domínio no `ALLOWED_HOSTS` do settings.py

**Banco não conecta:**
1. Verifique a senha do MySQL no WSGI
2. Certifique-se de que o banco foi inicializado
3. Verifique se o nome do banco está correto: `seu_usuario$default`

**Static files não carregam:**
1. Execute novamente: `python manage.py collectstatic`
2. Verifique os caminhos na configuração de Static files
3. Clique em Reload

---

## 🔄 ATUALIZAR O SITE (após mudanças no código)

No console Bash:

```bash
cd ~/atendimentos
workon atendimentos-env

# Baixe as atualizações do GitHub
git pull

# Execute migrações (se houver)
python manage.py migrate

# Colete arquivos estáticos
python manage.py collectstatic --noinput
```

Depois, vá na aba **"Web"** e clique em **"Reload"**.

---

## 📊 INFORMAÇÕES ÚTEIS

**Suas URLs:**
- Site: `https://seu_usuario.pythonanywhere.com/`
- Admin: `https://seu_usuario.pythonanywhere.com/admin/`
- API: `https://seu_usuario.pythonanywhere.com/api/`

**Limites do plano gratuito:**
- 100 segundos de CPU por dia (suficiente!)
- 512MB de espaço em disco
- 1 app web
- Domínio .pythonanywhere.com

---

## ✅ CHECKLIST FINAL

- [x] Conta criada no PythonAnywhere
- [x] Repositório criado no GitHub
- [x] Código enviado para o GitHub
- [x] MySQL configurado no PythonAnywhere
- [x] Projeto clonado no Bash
- [x] Virtual environment criado
- [x] Dependências instaladas
- [x] Migrações executadas
- [x] Superusuário criado
- [x] Web App criado
- [x] Virtual environment configurado no Web App
- [x] Static files configurados
- [x] WSGI configurado e salvo
- [x] Site recarregado
- [ ] ✨ **SITE NO AR!**

---

🎊 **Parabéns! Você conseguiu hospedar seu Django gratuitamente!**

Se precisar de ajuda, me chame! 😊
