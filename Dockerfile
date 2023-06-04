FROM python:3.11

WORKDIR /var/www

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

COPY . ./

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

RUN #alembic upgrade head
