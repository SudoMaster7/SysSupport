# ========================================
# ARQUIVO WSGI PARA PYTHONANYWHERE
# ========================================
# Cole ESTE CONTEÚDO no arquivo WSGI do PythonAnywhere
# Lembre-se de substituir:
# - SEU_USUARIO_PYTHONANYWHERE (seu username do PythonAnywhere)
# - SUA_SENHA_MYSQL (a senha que você criou no MySQL)
# ========================================

import os
import sys

# ===== CONFIGURE AQUI =====
# Substitua SEU_USUARIO_PYTHONANYWHERE pelo seu username
PYTHONANYWHERE_USER = 'SEU_USUARIO_PYTHONANYWHERE'  # <<<< MUDE AQUI
MYSQL_PASSWORD = 'SUA_SENHA_MYSQL'                   # <<<< MUDE AQUI
# ==========================

# Adicione o diretório do projeto ao path
path = f'/home/{PYTHONANYWHERE_USER}/SysSupport'
if path not in sys.path:
    sys.path.insert(0, path)

# Configure as variáveis de ambiente
os.environ['DJANGO_SETTINGS_MODULE'] = 'sys_support.settings'
os.environ['DB_PASSWORD'] = MYSQL_PASSWORD
os.environ['DB_NAME'] = f'{PYTHONANYWHERE_USER}$default'
os.environ['DB_USER'] = PYTHONANYWHERE_USER
os.environ['DB_HOST'] = f'{PYTHONANYWHERE_USER}.mysql.pythonanywhere-services.com'
os.environ['PYTHONANYWHERE_DOMAIN'] = 'True'
os.environ['SECRET_KEY'] = 'xx)5!e&+r2&dl@i^#394ylrmrbk+nzzub(_s@b!a@n*9g88_v('
os.environ['DEBUG'] = 'False'

# Configure o Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
