
# O Projeto
Um chatbot construido utilizando rasa, integrado ao facebook messager, capaz de automatizar
o processo de obtenção e estruturação de informações, enviar emails e públicar posts na página do facebook.

## Escopo
A beneficiário do projeto participava de uma ONG que ajudava animais, a qual recebia auxilio da prefeitura municipal, fornecendo um abrigo de animais. Infelizmente a ONG perdeu o apoio e, posteriormente, se desfez. Mas, para continuar ajudando os animais, a beneficiária encontrou outra forma de agir para cuidar dos animais necessitados, criando uma página no facebook para os habitantes da cidade entrarem em contato e comunicarem sobre possíveis casos com esses animais. Com isso a beneficiária poderia ajudar por si própria ou realizar publicações na página em busca de pessoas que pudessem ajudar.

## O problema resolvido pelo chabot
O auxilo aos animais provido pela beneficiária é um trabalho talmente não remunerado. Por isso ela possui um emprego formal, que ocupa parte de seu tempo, o que torna impossível que as mensagens recebidas pela página sejam lidas e respondidas no exato momento.

Devido a isso, o chatbot foi desenvolvido no intuito de facilitar essa comunicação, obter e estruturas as informações e auxiliar em tarefas manuais que são passíveis de automatização, como a criação de um post no facebook.

## Funcionalidades
O Chatbot tem por objetivo interpretar as mensagens do usuário para atender aos seguintes serviços: 
* Resgate de um animal abandonado
* Doação de um Animal
* Ajuda financeira para a página
* FAQ com dúvidas recorrentes.

Para os principais serviços, como Resgate de Animal e Doação de Animal, o Chatbot realizará perguntas para obter os dados pessoais (do usuário que entrou em contato com a página), dados do animal a ser resgatado e a localização onde o animal se encontra.

Após obter todas as informações necessárias, os dados serão estruturados e enviados por email para a beneficiária e ela tomará as medidas cabíveis ao caso.

O email possuirá um botão que, ao clicado, realizara um post na página do Facebook contendo todos os dados obtidos.

### Arquitetura do projeto
<p align="center">
  <img src="assets/arquitetura.png"/>
</p>

# Tecnologias utilizadas
* Python 3.8.10
* Rasa 3.0.3
* Spacy 3.2.1
    * Modelo <em>pt_core_news_lg</em>
* Pymongo 3.10.1
* MongoDB
* [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/)
* [Facebook-sdk](https://github.com/mobolic/facebook-sdk)
* [Duckling](https://github.com/facebook/duckling)
* Docker 20.10.8 e Docker-compose 1.29.2
* [SightEngine API](https://sightengine.com/)


# Executando o projeto
O projeto está dockerizado. Basta configuras as variaveis de ambiente e
criar os containers, como será descrito abaixo.
## Configurando variáveis de ambiente
Algumas variaveis de ambiente necessitam de alguns processos de configuração externos
ao projeto. Como, por exemplo, a integração do chatbot com o Facebook.
Para isso é necessário acessar a página do [facebook developers](https://developers.facebook.com), logar com a conta do Facebook que possui a página, criar um APP e
linkar esse APP com a página. Após esse processo serão obtidos identificadores e tokens de acesso necessários para o projeto. Detalhes podem ser encontrados na [documentação oficial](https://developers.facebook.com/docs/development/) do facebook.

Além disso, também utilizamos [SightEngine API](https://sightengine.com/), uma API que identifica nudez, sangue ou conteúdo ofensivo em imagens (algo imprecindível para não infringirmos as diretrizes do facebook ao realizar uma publícação). Esse serviço necessita de cadastro para obter da credenciais que permitem o uso da API.


A tabela abaixo as informações que devem ser descritas no arquivo ```rasa.env```
de configuração.

| Nome | Descrição |
| --------------- | --------------- |
| ```EMAIL_SENDER``` | Email do remetente. Email que irá enviar os dados capturados e estruturados pelo bot ao email receptor. Ex: email@example.com |
| ```EMAIL_SENDER_SENHA``` | Senha do email do remetente. Se utilizar a autenticação de 2 fatores é necessário definir uma "senha para aplicativos". Como mostra esse documento, para gmails. https://support.google.com/accounts/answer/185833?hl=pt-BR |
| ```EMAIL_RECEIVER``` | Email receptor. Email que receberá os dados. |
| ```DEVELOPER_APP_NAME``` | Nome do APP criado no facebook developers. |
| ```DEVELOPER_APP_SECRET``` | Secrect key. Informação obtida no facebook developers. |
| ```PAGE_ACESS_TOKEN``` | Token de acesso a página, obtido no facebook developers. |
| ```PAGE_POST_ACESS_TOKEN``` | Token de acesso a publicações na página, obtido no facebook developers. |
| ```MONGO_URI``` | URL de conexeão com o banco de dados. |
| ```ENABLE_SAFE_API``` | Valor booleano True/False que define se as imagens serão avaliadas pela API que busca nudez, sangue ou contéudo ofensivo. Quando False, as imagens passam livrimente, sem nenhuma validação, porém isso é informando no email e o botão de post automatico é removido, forçando com que o usuário precise criar o post manualmente com as informações obtidas pelo bot. Isso garante que ele não clique no botão sem avaliar as imagens. |
| ```SAFE_API_TOKEN``` | Token de acesso a API, obtida no site [SightEngine API](https://sightengine.com/) após o cadastro. |
| ```SAFE_API_USER_ID``` | Identificador obtido no site [SightEngine API](https://sightengine.com/) após o cadastro. |

/home/vinicius/Documentos/daap/av-daap/modules/facebook/images/

## Criand os containers
```
docker-compose up
```

## Executando separadamente
### Instale o Spacy
Instale o spacy e o modelo no **ambiente onde o rasa está instalado**
```
pip install spacy
python3 -m spacy download pt_core_news_lg
```
### Crie um container para o duckling
```
docker run -p 8000:8000 rasa/duckling
```

### Execute as actions
```
rasa run actions
```
### Execute e o bot
```
rasa run --credentials credentials.yml --enable-api --cors "*"
```
ou, para executar através do terminal
```
rasa shell
```
