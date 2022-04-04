# Full example

## Overview
For resolver the test I developed the endpoints:

| Endpoints                                | Methods   | Description                | Query Filter |
|------------------------------------------|-----------|----------------------------|--------------|
| /swagger/                                | GET       | Swagger json               |      ---     |
| /swagger-ui/                             | GET       | Swagger Iteractive         |      ---     |
| /api/v1/events                           | GET, POST | List and create a events   | Yes          |
| /api/v1/events/<uuid:event_uuid>         | PUT       | Update an event            | No           |
| /api/v1/selections                       | GET, POST | List and create selections | Yes          |
| /api/v1/selections/<uuid:selection_uuid> | PUT       | Update a selection.        | No           |
| /api/v1/sports                           | GET, POST | List and create a sport    | Yes          |
| /api/v1/sports/<uuid:sport_uuid>         | PUT       | Update a sport             | No           |

## Filtering

Some endpoints are enable query filter:

  - /api/v1/events 
  - /api/v1/selections 
  - /api/v1/sports

### /sports 
Fields that could be used to get events:

- id: int
- uuid: uuid
- slug: str
- active:  bool, [0, 1]
- created_at: datetime, UTC format '2022-04-04 01:11:45.904114'


Example:

**Request**
```
curl --request GET 'http://127.0.0.1:5000/api/v1/sports?active=1' \
--header 'Content-Type: application/json'
```

**Response**
```json
# 200 Success
  [
      {
          "active": true,
          "created_at": "2022-03-27T00:15:08",
          "slug": "sport-1",
          "uuid": "93a10761-e469-4adb-a0c2-9788408e1c85"
      },
      {
          "active": true,
          "created_at": "2022-03-27T00:16:40",
          "slug": "sport-2",
          "uuid": "8cc3a409-7557-42bf-96cc-82776c0dba8a"
      }
  ]
```

### /events
Fields that could be used as query filters to get events:

- id: int
- sport_id: int
- uuid: uuid
- name: str
- slug: str
- active: bool, [0, 1]
- event_type: str, values can be: pending, started, ended, cancelled.
- status: str, values can be: preplay, inplay
- scheduled_at: datetime, UTC format '2022-04-04 01:11:45.904114'
- start_at: datetime, UTC format'2022-04-04 01:11:45.904114'
- created_at: datetime, UTC format '2022-04-04 01:11:45.904114'

**Request**
```
curl --request GET 'http://127.0.0.1:5000/api/v1/events?event_type=preplay&active=1' \
--header 'Content-Type: application/json'
```

**Response**
```json
# 200 Success
[
    {
        "active": true,
        "created_at": "2022-04-01 00:26:31",
        "event_type": "EventType.preplay",
        "name": "Event First",
        "scheduled_at": "2022-03-28 00:15:08",
        "slug": "event-first",
        "start_at": null,
        "status": "EventStatus.pending",
        "uuid": "e1ec2c23-1148-48a3-a3be-2e61346323ab"
    },
    {
        "active": true,
        "created_at": "2022-04-01 00:26:33",
        "event_type": "EventType.preplay",
        "name": "Event Third",
        "scheduled_at": "2022-03-28 00:15:08",
        "slug": "event-thrid",
        "start_at": "2022-04-01 00:26:33",
        "status": "EventStatus.started",
        "uuid": "d224d7fa-ce66-4f56-bf14-ab4550ce47b9"
    }
]
```

### /selections 
Fields that could be used as query filters to get selections:

- id: int
- event_id: int
- uuid: uuid4
- price: float
- active: bool, [0, 1]
- outcome:  str, values can be: unsettled, void, lose, win.
- created_at: datetime, UTC format '2022-04-04 01:11:45.904114'


**Request**
```
curl --request GET 'http://127.0.0.1:5000/api/v1/selections?outcome=win&active=1' \
--header 'Content-Type: application/json'
```

**Response**
```json
# 200 Success
[
    {
        "active": true,
        "created_at": "2022-04-02 22:45:55",
        "uuid": "450c30b7-97d5-490c-abbd-249fa2a0a8e7"
    }
]
```
## Erros

```json
# 4xx Error Generics
{
  "message": "Filter with nonexistent field",
  "status_code": 400
}

# 422 Validation Error
{
  "message": "Field invalid",
  "status_code": 422
}

# 401 Unauthorized
{
  "msg": "Token has expired"
}
```