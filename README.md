# Teste prático - Brisanet

Desenvolvimento de uma API RESTFull HTTP

## Observações
Como não se trata de uma API em produção, converti o Schema PostgreSQL para SQLite afim de facilitar o desenvolvimento e testes, porém deixei comentado a conexão com o PostgreSQL casso necessário...
## Requisitos

- Python 3.8.5
- Virtualenv

## Execução 

Criar o ambiente virtual

```bash
python3 -m virtualenv venv
```

Ativar o ambiente virtual (linux)

```bash
source venv/bin/activate
```

Instalar requisitos

```bash
pip install -r requirements.txt
```

Iniciar server

```bash
python3 manage.py runserver
```

## Autor
[Aleff Souza](https://www.linkedin.com/in/aleffsouza/)