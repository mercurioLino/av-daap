import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#SMTP - Simple Mail Transfer Protocol
#Servidor para envio de email

def envia_email(): 
    #Start do server
    host = "smtp.gmail.com"
    port = "587"
    login = "epythonteste@gmail.com"
    senha = "Compass123456"

    server = smtplib.SMTP(host, port)
    
    server.ehlo()
    server.starttls()

    server.login(login, senha)

    #Construção do corpo do email
    ##Texto com link
    corpo = '<a href="https://www.youtube.com/watch?v=XuaoPo_6c0U">?</a>'
    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = 'danielfiliec@gmail.com'
    email_msg['Subject'] = "Descubra"
    email_msg.attach(MIMEText(corpo, 'html'))

    ##Anexo
    caminho_anexo = 'C:\\Users\\Pichau\\Documents\\GitHub\\av-daap\\tessteemail\\imagens\\dog3-600x459-0e01be20.jpg' ##Inserir aqui o caminho do arquivo
    attachment = open(caminho_anexo, 'rb')
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(attachment.read())
    encoders.encode_base64(att)
    att.add_header('Content-Disposition', f'attachment; filename=dog3-600x459-0e01be20.jpg')
    attachment.close()
    email_msg.attach(att)

    #Envio do email
    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

    #Rechando o servidor
    server.quit()
