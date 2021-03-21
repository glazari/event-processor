CREATE TABLE event_schemas (
  client_id     text NOT NULL,
  event_name    text NOT NULL,
  event_schema  json NOT NULL,

  PRIMARY KEY   (client_id, event_name)
)
