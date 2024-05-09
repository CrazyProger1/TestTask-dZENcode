FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/comment-system

COPY ./requirements/deploy.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/comment-system

EXPOSE 8000

CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
