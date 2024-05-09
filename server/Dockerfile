FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/comment-system

COPY . /usr/src/comment-system

RUN pip install -r ./requirements/deploy.txt

EXPOSE 8000

CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
