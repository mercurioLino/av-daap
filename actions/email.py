import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_mail(type_selected, html_email):
        #Start do server
        host = "smtp.gmail.com"
        port = "587"
        login = ""
        senha = ""

        server = smtplib.SMTP(host, port)
        
        server.ehlo()
        server.starttls()

        server.login(login, senha)

        #Construção do corpo do email
        ##Texto com link
        corpo = html_email
        print(corpo)
        email_msg = MIMEMultipart()
        email_msg['From'] = login
        email_msg['To'] = ''
        email_msg['Subject'] = type_selected
        email_msg.attach(MIMEText(corpo, 'html'))

        ##Anexo
        # caminho_anexo = '' ##Inserir aqui o caminho do arquivo
        # attachment = open(caminho_anexo, 'rb')
        # att = MIMEBase('application', 'octet-stream')
        # att.set_payload(attachment.read())
        # encoders.encode_base64(att)
        # att.add_header('Content-Disposition', f'attachment; filename=') #Inserir no filename o nome do arquivo
        # attachment.close()
        # email_msg.attach(att)

        #Envio do email
        server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

        #Fechando o servidor
        server.quit()

# mapeia as respostas armazenadas pelo bot em algo legível para o receptor do email
def mapping_responses(original):
    if original is None:
        return 'Não Informado'
    elif original == False:
        return 'Não'
    elif original == True:
        return 'Sim'
    else:
        return original

def send_rescue_email(age, name, phone, email, animal_type, animal_attributes, animal_health,
                    animal_urgency, medical_attention, private_property, maus_tratos,
                    address_district, address_street, address_number, address_landmark):
        
        htlm_email = f'''
        <!DOCTYPE html>
        <html>
        <head>
        <style>

        .colored {{
        color: red;
        }}

        table {{
        table-layout: fixed; 
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }}

        td, th {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        }}

        </style>
        </head>
        <body>

        <h2>Solicitação de <span class='colored'>RESGATE<span></h2>

        <h3>Dados do usuário</h3>

        <table>
        <tr>
            <td>Idade</td>
            <td>{mapping_responses(age)}</td>
        </tr>
        <tr>
            <td>Nome</td>
            <td>{mapping_responses(name)}</td>
        </tr>
        <tr>
            <td>Telefone</td>
            <td>{mapping_responses(phone)}</td>
        </tr>
        <tr>
            <td>Email</td>
            <td>{mapping_responses(email)}</td>
        </tr>
        </table>

        <h3>Dados do Animal</h3>

        <table>
        <tr>
            <td>Tipo do animal</td>
            <td>{mapping_responses(animal_type)}</td>
        </tr>
        <tr>
            <td>Características do animal</td>
            <td>{mapping_responses(animal_attributes)}</td>
        </tr>
        <tr>
            <td>Saude do animal</td>
            <td>{mapping_responses(animal_health)}</td>
        </tr>
        <tr>
            <td>Necessidade de urgência</td>
            <td>{mapping_responses(animal_urgency)}</td>
        </tr>
        <tr>
            <td>Necessidade de atenção médica</td>
            <td>{mapping_responses(medical_attention)}</td>
        </tr>
        <tr>
            <td>Propriedade privada</td>
            <td>{mapping_responses(private_property)}</td>
        </tr>
        <tr>
            <td>Maus tratos</td>
            <td>{mapping_responses(maus_tratos)}</td>
        </tr>
        </table>

        <h3>Endereço onde o animal se encontra</h3>

        <table>
        <tr>
            <td>Bairro</td>
            <td>{mapping_responses(address_district)}</td>
        </tr>
        <tr>
            <td>Rua</td>
            <td>{mapping_responses(address_street)}</td>
        </tr>
        <tr>
            <td>Numero</td>
            <td>{mapping_responses(address_number)}</td>
        </tr>
        <tr>
            <td>Referencia</td>
            <td>{mapping_responses(address_landmark)}</td>
        </tr>
        </table>
        </body>
        </html>
        '''

        send_mail('Resgate de animal', htlm_email)

def send_donate_email(age, name, phone, email, animal_type, animal_attributes, animal_quantity,
                    is_vacinado, is_castrado, address_district, address_street, address_number, address_landmark):
        
        htlm_email = f'''
        <!DOCTYPE html>
        <html>
        <head>
        <style>

        .colored {{
        color: red;
        }}

        table {{
        table-layout: fixed; 
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }}

        td, th {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        }}

        </style>
        </head>
        <body>

        <h2>Solicitação de <span class='colored'>RESGATE<span></h2>

        <h3>Dados do usuário</h3>

        <table>
        <tr>
            <td>Idade</td>
            <td>{mapping_responses(age)}</td>
        </tr>
        <tr>
            <td>Nome</td>
            <td>{mapping_responses(name)}</td>
        </tr>
        <tr>
            <td>Telefone</td>
            <td>{mapping_responses(phone)}</td>
        </tr>
        <tr>
            <td>Email</td>
            <td>{mapping_responses(email)}</td>
        </tr>
        </table>

        <h3>Dados do Animal a ser adotado</h3>

        <table>
        <tr>
            <td>Tipo do animal</td>
            <td>{mapping_responses(animal_type)}</td>
        </tr>
        <tr>
            <td>Características do animal</td>
            <td>{mapping_responses(animal_attributes)}</td>
        </tr>
        <tr>
            <td>Quantidade de animais</td>
            <td>{mapping_responses(animal_quantity)}</td>
        </tr>
        <tr>
            <td>Animail vacinado</td>
            <td>{mapping_responses(is_vacinado)}</td>
        </tr>
        <tr>
            <td>Necessidade castrado</td>
            <td>{mapping_responses(is_castrado)}</td>
        </tr>
        </table>

        <h3>Endereço onde o animal se encontra</h3>

        <table>
        <tr>
            <td>Bairro</td>
            <td>{mapping_responses(address_district)}</td>
        </tr>
        <tr>
            <td>Rua</td>
            <td>{mapping_responses(address_street)}</td>
        </tr>
        <tr>
            <td>Numero</td>
            <td>{mapping_responses(address_number)}</td>
        </tr>
        <tr>
            <td>Referencia</td>
            <td>{mapping_responses(address_landmark)}</td>
        </tr>
        </table>
        </body>
        </html>
        '''

        send_mail('Doação de animal', htlm_email)