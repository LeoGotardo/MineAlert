import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()

class fileCreationHandler(FileSystemEventHandler):
    def __init__(self, emailSender):
        self.emailSender = emailSender
    
    def on_created(self, event):
        if not event.is_directory:
            fileName = os.path.basename(event.src_path)
            filePath = event.src_path
            creationTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"Arquivo criado: {fileName} em {filePath}")
            self.emailSender.sendNotification(fileName, filePath, creationTime)

class emailSender:
    def __init__(self, smtpServer, smtpPort, emailUser, emailPassword, recipientEmail):
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.emailUser = emailUser
        self.emailPassword = emailPassword
        self.recipientEmail = recipientEmail
    
    def sendNotification(self, fileName, filePath, creationTime):
        try:
            # Criar mensagem de email
            message = MIMEMultipart()
            message["From"] = self.emailUser
            message["To"] = self.recipientEmail
            message["Subject"] = f"Novo arquivo criado: {fileName}"
            
            # Corpo do email
            emailBody = f"""
            Um novo arquivo foi detectado na pasta monitorada!
            
            Detalhes do arquivo:
            • Nome: {fileName}
            • Caminho completo: {filePath}
            • Data/Hora de criação: {creationTime}
            
            Este é um email automático do sistema de monitoramento de arquivos.
            """
            
            message.attach(MIMEText(emailBody, "plain", "utf-8"))
            
            # Conectar ao servidor SMTP e enviar email
            with smtplib.SMTP(self.smtpServer, self.smtpPort) as server:
                server.starttls()  # Habilitar criptografia
                server.login(self.emailUser, self.emailPassword)
                server.send_message(message)
            
            print(f"Email enviado com sucesso para {self.recipientEmail}")
            
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")

class fileMonitor:
    def __init__(self, folderToWatch, emailConfig):
        self.folderToWatch = folderToWatch
        self.emailSender = emailSender(**emailConfig)
        self.observer = Observer()
    
    def startMonitoring(self):
        if not os.path.exists(self.folderToWatch):
            print(f"Erro: A pasta '{self.folderToWatch}' não existe!")
            return
        
        eventHandler = fileCreationHandler(self.emailSender)
        self.observer.schedule(eventHandler, self.folderToWatch, recursive=True)
        self.observer.start()
        
        print(f"Monitoramento iniciado para a pasta: {self.folderToWatch}")
        print("Pressione Ctrl+C para parar o monitoramento")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("\nMonitoramento interrompido pelo usuário")
        
        self.observer.join()

def main():
    # Configurações - MODIFIQUE ESTAS INFORMAÇÕES
    folderToWatch = os.getenv("MONITOR_FOLDER_PATH")
    
    emailConfig = {
        "smtpServer": os.getenv("SMTP_SERVER", "smtp.gmail.com"),   # Servidor SMTP (Gmail)
        "smtpPort": int(os.getenv("SMTP_PORT", 587)),               # Porta SMTP
        "emailUser": os.getenv("EMAIL_USER"),                       # Seu email
        "emailPassword": os.getenv("EMAIL_PASSWORD"),               # Senha de aplicativo do Gmail
        "recipientEmail": os.getenv("RECIPIENT_EMAIL")              # Email de destino
    }
    
    # Criar e iniciar monitor
    monitor = fileMonitor(folderToWatch, emailConfig)
    monitor.startMonitoring()

if __name__ == "__main__":
    # Verificar se as dependências estão instaladas
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Erro: A biblioteca 'watchdog' não está instalada.")
        print("Instale com: pip install watchdog")
        exit(1)
    
    print("=== Monitor de Arquivos com Notificação por Email ===")
    print("Variáveis de ambiente necessárias:")
    print("• MONITOR_FOLDER_PATH - Caminho da pasta a monitorar")
    print("• EMAIL_USER - Seu email de origem")
    print("• EMAIL_PASSWORD - Senha de aplicativo do email")
    print("• RECIPIENT_EMAIL - Email de destino das notificações")
    print("• SMTP_SERVER (opcional) - Servidor SMTP (padrão: smtp.gmail.com)")
    print("• SMTP_PORT (opcional) - Porta SMTP (padrão: 587)")
    print()
    
    main()
