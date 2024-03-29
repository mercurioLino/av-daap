# Utiliza a imagem rasa oficial como base
FROM rasa/rasa:3.0.3-full

# Utiliza o root user para instalar as dependências
USER root

# Instala as dependências
RUN python -m spacy download pt_core_news_lg

COPY ./actions/requirements-actions.txt ./
RUN pip install -r requirements-actions.txt

COPY ./addons ./addons

# Seguindo as boas práticas não executo o código com user root
USER 1001