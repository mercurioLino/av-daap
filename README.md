
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
* Facebook-sdk
* Docker 20.10.8 e Docker-compose 1.29.2
* https://sightengine.com/


# Instalação
## Rode o duckling
docker run -p 8000:8000 rasa/duckling
### Instale o Spacy
pip install spacy

python3 -m spacy download pt_core_news_lg


### Rodando as actions e o bot
rasa run actions

rasa shell


TODO

tratar momentos em que o form não pega os dados corretamente

adicionar senha no banco de dados

adicionar opção para postar ou não imagem

quando não conseguir usar o banco não deve enviar o link pra colocar o post no email