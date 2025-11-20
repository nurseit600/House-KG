FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /hous_app

COPY requirements.txt/hous_app/
RUN pip install -r requirements.txt && \
    pip install --upgrade pip

COPY . /hous_app/
