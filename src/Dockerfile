FROM python:3.7.4

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

COPY ./app /app

RUN groupadd -r app_user && \
    useradd --no-log-init --create-home -r -g app_user app_user

USER app_user
