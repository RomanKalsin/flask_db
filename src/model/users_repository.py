import psycopg2
from psycopg2.extras import RealDictCursor


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users;")
            return cur.fetchall()
    
    def find(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s;", (id,))
            return cur.fetchone()

    def get_by_term(self, search_term=""):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                    SELECT * FROM users
                    WHERE name ILIKE %s OR email ILIKE %s;
                """,
                (f"%{search_term}%", f"%{search_term}%"),
            )
            return cur.fetchall()

    def save(self, user):
        if 'id' in user and user['id']:
            self._update(user)
        else:
            self._create(user)

    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE id = %s;",
                (id,)
            )
        self.conn.commit()

    def _update(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET name = %s, email = %s WHERE id = %s;",
                (user['name'], user['email'], user['id']),
            )
        self.conn.commit()

    def _create(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
                (user['name'], user['email']),
            )
            user['id'] = cur.fetchone()[0]
        self.conn.commit()
