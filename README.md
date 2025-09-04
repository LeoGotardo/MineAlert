# 📁 Monitor de Arquivos com Notificação por Email

Script Python que monitora uma pasta em tempo real e envia notificações por email automaticamente quando novos arquivos são criados.

## ✨ Características

- 🔍 **Monitoramento em tempo real** usando `watchdog`
- 📧 **Notificações automáticas** por email
- 🌳 **Monitoramento recursivo** (inclui subpastas)
- 🔒 **Configuração segura** via variáveis de ambiente
- ⚙️ **Suporte múltiplos provedores** (Gmail, Outlook, Yahoo)
- 🛠️ **Fácil configuração** com arquivo `.env`

## 🚀 Instalação

### Pré-requisitos
- Python 3.6+
- pip (gerenciador de pacotes Python)

### Dependências
```bash
pip install watchdog python-dotenv
```

## ⚙️ Configuração

### 1. Criar arquivo .env

Crie um arquivo `.env` na mesma pasta do script:

```bash
# Configurações obrigatórias
MONITOR_FOLDER_PATH=C:/Users/SeuUsuario/Downloads
EMAIL_USER=seuemail@gmail.com
EMAIL_PASSWORD=sua_senha_de_aplicativo
RECIPIENT_EMAIL=destinatario@gmail.com

# Configurações opcionais (padrões para Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 2. Configuração para Gmail

1. **Ative a autenticação de 2 fatores:**
   - Vá em [Conta Google](https://myaccount.google.com)
   - Segurança → Verificação em duas etapas

2. **Crie uma senha de aplicativo:**
   - Segurança → Senhas de aplicativo
   - Selecione "Outro" e digite "Monitor Arquivos"
   - Use a senha gerada no `EMAIL_PASSWORD`

### 3. Outros provedores de email

**Outlook/Hotmail:**
```bash
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

**Yahoo Mail:**
```bash
SMTP_SERVER=smtp.mail.yahoo.com  
SMTP_PORT=587
```

## 🏃‍♂️ Como usar

### Execução básica
```bash
python reconnect.py
```

### Verificação de configuração
O script automaticamente:
- Verifica se todas as dependências estão instaladas
- Mostra quais variáveis de ambiente são necessárias
- Valida se a pasta existe
- Confirma a configuração de email

### Parar o monitoramento
Pressione `Ctrl+C` para interromper

## 📋 Variáveis de Ambiente

| Variável | Obrigatória | Descrição | Exemplo |
|----------|-------------|-----------|---------|
| `MONITOR_FOLDER_PATH` | ✅ | Pasta para monitorar | `C:/Users/Leo/Downloads` |
| `EMAIL_USER` | ✅ | Email remetente | `monitor@gmail.com` |
| `EMAIL_PASSWORD` | ✅ | Senha de aplicativo | `abcd1234efgh5678` |
| `RECIPIENT_EMAIL` | ✅ | Email destinatário | `alertas@gmail.com` |
| `SMTP_SERVER` | ❌ | Servidor SMTP | `smtp.gmail.com` |
| `SMTP_PORT` | ❌ | Porta SMTP | `587` |

## 📧 Exemplo de Notificação

Quando um arquivo é criado, você receberá:

```
Assunto: Novo arquivo criado: documento.pdf

Um novo arquivo foi detectado na pasta monitorada!

Detalhes do arquivo:
• Nome: documento.pdf
• Caminho completo: C:/Users/Leo/Downloads/documento.pdf
• Data/Hora de criação: 2025-09-04 15:45:30

Este é um email automático do sistema de monitoramento de arquivos.
```

## 🛠️ Solução de Problemas

### Erro: "No module named 'watchdog'"
```bash
pip install watchdog python-dotenv
```

### Erro: Pasta não encontrada
- Verifique se o caminho em `MONITOR_FOLDER_PATH` existe
- Use barras normais `/` mesmo no Windows
- Exemplo: `C:/Users/Usuario/Downloads`

### Erro de autenticação Gmail
- Confirme que a autenticação de 2 fatores está ativada
- Use **senha de aplicativo**, não a senha da conta
- Verifique se `EMAIL_USER` e `EMAIL_PASSWORD` estão corretos

### Erro: SyntaxError com caminhos
Use barras normais `/` nos caminhos:
```bash
# ✅ Correto
MONITOR_FOLDER_PATH=C:/Users/Usuario/pasta com espaços/Downloads

# ❌ Incorreto
MONITOR_FOLDER_PATH=C:\Users\Usuario\pasta com espaços\Downloads
```

### Emails não chegam
- Verifique a pasta de spam
- Teste com um email simples primeiro
- Confirme as configurações SMTP

## 🎯 Exemplo Completo de Instalação

```bash
# 1. Instalar dependências
pip install watchdog python-dotenv

# 2. Criar arquivo .env
echo MONITOR_FOLDER_PATH=C:/Users/%USERNAME%/Downloads > .env
echo EMAIL_USER=seuemail@gmail.com >> .env
echo EMAIL_PASSWORD=sua_senha_app >> .env  
echo RECIPIENT_EMAIL=alertas@gmail.com >> .env

# 3. Executar
python reconnect.py
```

## 🔧 Personalização

### Modificar formato do email
Edite a função `sendNotification()` na classe `emailSender`:

```python
emailBody = f"""
Seu formato customizado aqui!
Arquivo: {fileName}
Caminho: {filePath}
Hora: {creationTime}
"""
```

### Desabilitar monitoramento de subpastas
Na função `startMonitoring()`, altere:
```python
self.observer.schedule(eventHandler, self.folderToWatch, recursive=False)
```

### Filtrar tipos de arquivo
Na função `on_created()`, adicione:
```python
if not fileName.endswith(('.pdf', '.docx', '.txt')):
    return  # Ignora outros tipos
```

## 🔒 Segurança

- ✅ Nunca commite o arquivo `.env` no git
- ✅ Use senhas de aplicativo específicas
- ✅ Considere um email dedicado para automações
- ✅ Mantenha permissões restritas: `chmod 600 .env` (Linux/Mac)

## 📝 Adicionando ao .gitignore

```gitignore
# Arquivos de configuração
.env
*.env

# Cache Python
__pycache__/
*.pyc
```

## 🆘 Suporte

Se encontrar problemas:
1. Verifique se todas as variáveis estão no `.env`
2. Teste a conexão de email separadamente
3. Confirme se a pasta existe e tem permissões
4. Execute com `python -v reconnect.py` para debug

---
