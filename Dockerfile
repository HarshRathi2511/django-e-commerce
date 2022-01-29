FROM python:3

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y netcat

# Create an app user 
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash app

ENV APP_HOME=/home/app/web

# Create the staticfiles directory. This avoids permission errors. 
RUN mkdir -p $APP_HOME/staticfiles
RUN mkdir -p $APP_HOME/media

WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . $APP_HOME

RUN chown -R app:app $APP_HOME

USER app:app

#to fix the user permissions while running entrypoint.sh 
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]