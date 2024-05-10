# Comment-System

## Quickstart

```shell
git clone https://github.com/CrazyProger1/TestTask-dZENcode
```

```shell
cd ./TestTask-dZENcode/server/
```

```shell
docker-compose -f compose.dev.yaml up
```

## API

See [swagger docs](http://localhost:8000/docs/swagger/)

## Websockets

Supported events:

- comments.create - create comment
- comments.read - get paginated comment list
- comments.replies.read - get paginated list of comment-replies

```json
{
  "type": "comments.create",
  "data": {
    "text": "comment text",  // required
    "reply_to": null  // comment id
  }
}
```

```json
{
  "type": "comments.read",
  "data": {
    "order_by": [
      "-created_at" // by default, order by creation date
    ],
    "filters": {
      "user": 0,  // filter by user id
      "created_at": "",  // filter by creation date
      "has_attachment": false  // filter by attachments
    },
    "limit": 25,  // by default, pagination limit
    "offset": 0  // by default, pagination offset
  }
}
```

```json
{
  "type": "comments.replies.read",
  "data": {
    "order_by": [
      "-created_at" // by default, order by creation date
    ],
    "filters": {
      "reply_to": 0,  // filter by parent comment id
      "user": 0,  // filter by user id
      "created_at": "",  // filter by creation date
      "has_attachment": false  // filter by attachments,
      
    },
    "limit": 25,  // by default, pagination limit
    "offset": 0  // by default, pagination offset
  }
}
```

## Database

ERD:

<p align="center">
    <img src="docs/database/database_v1.png" alt="ERD">
</p>

