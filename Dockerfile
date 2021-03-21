FROM python:3.6

RUN pip install pipenv

WORKDIR /home

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

RUN pipenv install --system --deploy

COPY . .

CMD flask run --host='0.0.0.0'
