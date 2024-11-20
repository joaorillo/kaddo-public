FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

# Install requirements
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install necessary language packages
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/*
RUN echo 'pt_BR.UTF-8 UTF-8' >> /etc/locale.gen && locale-gen
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

# Install PostgreSQL client and SQLite
RUN apt-get update && apt-get install -y postgresql-client sqlite3

COPY . .

# Start services and update static files
CMD gunicorn api.wsgi:application -c gunicorn_config.py