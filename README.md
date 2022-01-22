### Rode o duckling
docker run -p 8000:8000 rasa/duckling

### Instale o Spacy
pip install spacy

python3 -m spacy download pt_core_news_lg


### Rodando as actions e o bot
rasa run actions

rasa shell



TODO

fallback

tratar momentos em que o form não pega os dados corretamente



diagrama da arquitetura

lookup table

fazer um token do facebook no dia porque ele expira

caso em que nao conecta para enviar email

caso em que não conecta com o banco

adicionar senha no banco de dados

adicionar opção para postar ou não imagem

quando não conseguir usar o banco não deve enviar o link pra colocar o post no email



[informações parciais de endereço, quando não souber os detalhes, ele deve perguntar apenas as referências do endereço]


[o fluxo da doação ta errado, ele pede a imagem antes]

[alterar telefone porque pode ser tanto celular quando telefone e regex pega apenas telefone

Mudar o que ja ta lá    
- ^\([1-9]{2}\) [9]{0,1}[0-9]{1}[0-9]{3}\-[0-9]{4}$

Pro telefone fixo normal
 - ^\([1-9]{2}\) [0-9]{1}[0-9]{3}\-[0-9]{4}$]

[duas mensagens no inicio]