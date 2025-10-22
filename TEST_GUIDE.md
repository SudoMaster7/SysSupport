# Guia de Teste - Funcionalidade de Criar Usuários

## ✅ Checklist de Teste

### 1. Acesso à Página de Criar Usuário
- [ ] Login como Administrador TI
- [ ] Verificar se botão "Novo Usuário" está visível no menu superior direito
- [ ] Clicar no botão e confirmar que a página `/accounts/users/create/` carrega sem erros

### 2. Preenchimento do Formulário
- [ ] Formulário contém seções:
  - [ ] Dados de Login (Nome de Usuário, E-mail, Senha, Confirmar Senha)
  - [ ] Dados Pessoais (Nome, Sobrenome)
  - [ ] Dados Organizacionais (Matrícula, Unidade)
  - [ ] Perfil (Gestor ou Técnico)
- [ ] Todos os campos têm labels descritivos
- [ ] Campos obrigatórios estão marcados
- [ ] Estilo Tailwind é aplicado corretamente

### 3. Validações
- [ ] Tentar criar usuário com nome de usuário duplicado → erro exibido
- [ ] Tentar criar usuário com e-mail duplicado → erro exibido
- [ ] Tentar criar usuário com senhas diferentes → erro "As senhas não conferem"
- [ ] Tentar submeter sem preencher campo obrigatório → erro exibido
- [ ] Criar usuário com sucesso → mensagem de confirmação exibida

### 4. Criação bem-sucedida
- [ ] Criar um usuário "Gestor" com:
  - Username: `teste_gestor`
  - Email: `gestor@test.com`
  - Senha: `Teste@123456`
  - Nome: João
  - Sobrenome: Silva
  - Matrícula: MAT001
  - Unidade: (selecionar uma existente)
  - Perfil: Gestor
- [ ] Mensagem de sucesso aparecer
- [ ] Novo usuário poder fazer login
- [ ] Novo usuário estar vinculado ao grupo "Gestor"

### 5. Criação de Técnico
- [ ] Criar um usuário "Técnico" com:
  - Username: `teste_tecnico`
  - Email: `tecnico@test.com`
  - Senha: `Teste@123456`
  - Perfil: Técnico
- [ ] Verificar que está vinculado ao grupo "Técnico"

### 6. Restrições de Acesso
- [ ] Login como Gestor → botão "Novo Usuário" não deve aparecer
- [ ] Login como Técnico → botão "Novo Usuário" não deve aparecer
- [ ] Tentar acessar `/accounts/users/create/` sem ser Admin → erro de permissão

### 7. Integração com Django Admin
- [ ] Acessar `/admin/` como superusuário
- [ ] Em Usuários, verificar que os novos usuários aparecem na lista
- [ ] Clicar em um usuário criado via web e verificar que:
  - [ ] Grupo está correto
  - [ ] Perfil (inline) contém matrícula e unidade

### 8. Funcionalidades Posterior dos Usuários Criados
- [ ] **Gestor**: Pode fazer login e criar um chamado?
- [ ] **Técnico**: Pode fazer login e visualizar chamados?

## 📝 Notas Importantes

- O botão "Novo Usuário" só aparece para usuários com `is_superuser=True` ou no grupo "Administrador TI"
- A senha deve ser inserida duas vezes para confirmação
- A matrícula é opcional, mas a unidade é obrigatória
- O novo usuário é adicionado automaticamente ao grupo selecionado

## 🐛 Possíveis Problemas e Soluções

| Problema | Solução |
|----------|---------|
| Botão "Novo Usuário" não aparece | Verificar se está logado como Admin TI |
| Erro 404 ao acessar a página | Verificar se URL está correta: `/accounts/users/create/` |
| Erro de permissão | Verificar se user está no grupo "Administrador TI" |
| Usuário criado mas não recebe grupo | Executar `python manage.py create_groups` novamente |

## 🚀 Próximos Passos

Após validar a funcionalidade:
1. Teste a criação em massa (criar 5-10 usuários)
2. Teste o fluxo completo (criar usuário → fazer login → usar sistema)
3. Verifique as permissões de cada tipo de usuário
4. Teste o logout e re-login
