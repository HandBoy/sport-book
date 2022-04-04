DROP TABLE IF EXISTS sport;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS selection;
PRAGMA foreign_keys = ON;

CREATE TABLE sport (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT,
	slug TEXT NOT NULL,
	active INTEGER DEFAULT 0,	
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE event (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sport_id INTEGER NOT NULL,
  uuid TEXT,
  name TEXT NOT NULL,
	slug TEXT NOT NULL,
	active INTEGER DEFAULT 0,	
	event_type TEXT NOT NULL,
	status TEXT NOT NULL,
	scheduled_at TIMESTAMP NOT NULL,
	start_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sport_id) REFERENCES sport (id)
);

CREATE TABLE selection (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER NOT NULL,
  uuid TEXT,
	price REAL NOT NULL,
	active INTEGER DEFAULT 0,	
	outcome TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (event_id) REFERENCES event (id)
);

INSERT INTO sport (id, uuid, slug, active, created_at) 
VALUES (1, '93a10761-e469-4adb-a0c2-9788408e1c85', 'sport-1', 1, '2022-03-27 00:15:08'),
(2, '8cc3a409-7557-42bf-96cc-82776c0dba8a', 'sport-2', 1, '2022-03-27 00:16:40');

INSERT INTO event
(id, sport_id, uuid, name, slug, active, event_type, status, scheduled_at, start_at, created_at)
VALUES (1, 1, 'e1ec2c23-1148-48a3-a3be-2e61346323ab', 'Event First', 'event-first', 1, 'preplay', 'pending', '2022-03-28 00:15:08', NULL, '2022-04-01 00:26:31'),
(2, 1, 'c39fbe78-f4c2-49db-adaf-7b433f79ebe4', 'Event Second', 'event-second', 0, 'inplay', 'cancelled', '2022-03-28 00:15:08', NULL, '2022-04-01 00:26:32'),
(3, 2, 'd224d7fa-ce66-4f56-bf14-ab4550ce47b9', 'Event Third', 'event-thrid', 1, 'preplay', 'started', '2022-03-28 00:15:08', '2022-04-01 00:26:33', '2022-04-01 00:26:33'),
(4, 2, 'b4c35e82-a127-4651-9f04-202d3f232cc5', 'Event Fourth', 'event-fourth', 0, 'inplay', 'ended', '2022-03-28 00:15:08', NULL, '2022-04-01 00:26:34');


INSERT INTO selection (id, event_id, uuid, price, active, outcome, created_at)
VALUES
(1, 1, '3797c122-1a9b-40ab-8bd1-4830e7d4d3f7', 100.0, 1, 'unsettled', '2022-04-02 22:45:55'),
(2, 1, '450c30b7-97d5-490c-abbd-249fa2a0a8e7', 100.50, 1, 'win', '2022-04-02 22:45:55'),
(3, 1, '38b423a1-16f6-4f73-87bb-443a1cd03861', 70.75, 1, 'lose', '2022-04-02 22:45:55'),
(4, 1, '7521897a-666c-4f08-ac5d-eb2f04af2310', 100.0, 1, 'void', '2022-04-02 22:45:55');
