import logging
import json

from psycopg2.pool import ThreadedConnectionPool

from core.types import SchemaStorage


class PostgresSchemaStorage(SchemaStorage):
    def __init__(self, host, port, user, password):
        min_conns, max_conns = 1, 20
        self.pool = ThreadedConnectionPool(
            min_conns, max_conns,
            host=host, port=port,
            user=user, password=password,
            database="postgres",
        )

    def register_event(self, event_name, client, event_schema):
        insert_query = f"""
         INSERT INTO event_schemas
           (client_id, event_name, event_schema)
         VALUES
           ('{client}', '{event_name}', '{json.dumps(event_schema)}')
        """
        try:
            conn = self.pool.getconn()
            cur = conn.cursor()
            cur.execute(insert_query)
            conn.commit()
            success = True
        except Exception as e:
            logging.error(e)
            success = False
        finally:
            self.pool.putconn(conn)
        return success


    def get_event(self, event_name, client):
        select_query = f"""
         SELECT event_schema
         FROM event_schemas
         WHERE client_id = '{client}'
           AND event_name = '{event_name}'
        """
        try:
            conn = self.pool.getconn()
            cur = conn.cursor()
            cur.execute(select_query)
            row = cur.fetchone()
            schema = row[0]
        except Exception as e:
            logging.error(e)
            schema = None
        finally:
            self.pool.putconn(conn)
        return schema

    def list_events(self):
        select_query = """
         SELECT client_id, event_name, event_schema
         FROM event_schemas
        """
        try:
            conn = self.pool.getconn()
            cur = conn.cursor()
            cur.execute(select_query)
            rows = cur.fetchall()
        except Exception as e:
            logging.error(e)
            rows = []
        finally:
            self.pool.putconn(conn)

        for row in rows:
            client, event_name, schema = row
            yield (client, event_name, schema)



if __name__ == "__main__":
    storage = PostgresSchemaStorage("localhost", "5432", "admin", "admin")
    succ = storage.register_event("new_event", "client1", {"type":"object"})
    print("success", succ)

    schema = storage.get_event("new_event", "client1")
    print("schema", schema)

    events = storage.list_events()
    print(list(events))
