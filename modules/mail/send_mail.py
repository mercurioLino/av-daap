import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

import os

#Start do server
host = "smtp.gmail.com"
port = "587"
login = os.environ['EMAIL_SENDER']
senha = os.environ['EMAIL_SENDER_SENHA']

def send_mail(type_selected, html_email):
        try:
            server = smtplib.SMTP(host, port)
            server.ehlo()
            server.starttls()
            server.login(login, senha)
        except Exception as e:
            print('Houve um erro no login do email', e)
            return
        
        corpo = html_email
        email_msg = MIMEMultipart()
        email_msg['From'] = login
        email_msg['To'] = 'vinicius.marchi98@gmail.com'
        email_msg['Subject'] = type_selected
        email_msg.attach(MIMEText(corpo, 'html'))

        try:
            #Envio do email
            server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
            #Fechando o servidor
            server.quit()
        except Exception as e:
            print(e)

# mapeia as respostas armazenadas pelo bot em algo legível para o receptor do email
def mapping_responses(original):
    if original is None:
        return 'Não Informado'
    elif original == -1:
        return 'Desconhecido'
    elif original == False:
        return 'Não'
    elif original == True:
        return 'Sim'
    else:
        return original

def configure_env_templates():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'templates')
    env = Environment(
            loader=FileSystemLoader(filename),
            autoescape=select_autoescape(['html', 'xml'])
        )
    env.globals['mapping_responses'] = mapping_responses
    return env

def send_rescue_email(objectid=None, token=None, **kwargs):
    env = configure_env_templates()
    template = env.get_template('rescue_animal.html')

    html = template.render(objectid=objectid, token=token, **kwargs)

    send_mail('Resgate de animal', html)


def send_donate_email(objectid=None, token=None, **kwargs):
    env = configure_env_templates()
    template = env.get_template('donate_animal.html')
    html = template.render(objectid=objectid, token=token, **kwargs)
    print(html)

    send_mail('Doação de animal', html)