# Reddit Folha Bot Poster
Crie uma virtualenv:
> $ mkvirtualenv folha

Instale as dependências:
> $ pip install -r requirements.pip

Instale as dependências (Ubuntu 15.10):
> sudo apt-get install build-essential libncursesw5-dev libgdbm-dev libc6-dev && \
                                                       zlib1g-dev libsqlite3-dev tk-dev && \
                                                       libssl-dev openssl && \
                                                       python3-dev && \
                                                       libxml2-dev && \
                                                       libxslt1-dev libffi-dev


Configure um arquivo com as variáveis de ambiente necessárias:

> $ echo 'export REDDIT_USERNAME=<my_username>' >> .env

> $ echo 'export REDDIT_PASSWORD=<my_secret_key>' >> .env

> $ echo 'export IMGUR_API_CLIENT=<my_imgur_client>' >> .env

> $ echo 'export IMGUR_API_SECRET=<my_imgur_secret>' >> .env

Execute agora:
> source .env && ./main.py
