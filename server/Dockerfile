FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/comment-system

COPY . /usr/src/comment-system

RUN pip install -r ./requirements/production.txt

EXPOSE 8000

RUN chmod +x /usr/src/comment-system/entrypoint.sh

ENTRYPOINT ["/usr/src/comment-system/entrypoint.sh"]
