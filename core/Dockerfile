FROM python:3.10.5-slim

WORKDIR /core/app/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install postgresql postgresql-contrib gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /core/app/src/entrypoint.sh
RUN chmod +x /core/app/src/entrypoint.sh

COPY . .

ENTRYPOINT ["/core/app/src/entrypoint.sh"]