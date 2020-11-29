import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)

    return conn

# def create_connection_in_memory():
#     conn = None
#     try:
#         conn = sqlite3.connect(":memory:")
#         print(f"Connected, sqlite version {sqlite3.version}")
#     except Error as e:
#         if conn:
#             conn.close()

def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def add_projekt(conn, projekt):
    sql = '''INSERT INTO projects(nazwa, start_date, end_date) VALUES(?, ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, projekt)
    conn.commit()
    return cur.lastrowid

def add_zadanie(conn, zadanie):
    sql = '''INSERT INTO tasks(projekt_id, nazwa, opis, status, start_date, end_date)
                VALUES(?, ?, ?, ?, ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, zadanie)
    conn.commit()
    return cur.lastrowid

if __name__ == "__main__":

    create_projects_sql = """
    -- projects table
    CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        nazwa text NOT NULL,
        start_date text,
        end_date text
    );
    """

    create_tasks_sql = """
    -- zadanie table
    CREATE TABLE IF NOT EXISTS tasks (
        id integer PRIMARY KEY,
        projekt_id integer NOT NULL,
        nazwa VARCHAR(250) NOT NULL,
        opis TEXT,
        status VARCHAR(15) NOT NULL,
        start_date text NOT NULL,
        end_date text NOT NULL,
        FOREIGN KEY (projekt_id) REFERENCES projects (id)
    );
    """

    db_file = "database.db"
    conn = create_connection(db_file)

    projekt = ("Projekt excel to yaml", "2020-09-01 00:00:00", "2020-12-30 00:00:00")

    if conn is not None:
        execute_sql(conn, create_projects_sql)
        execute_sql(conn, create_tasks_sql)
        pr_id = add_projekt(conn, projekt)

        zadanie = (
            pr_id,
            "Create class",
            "Test",
            "in progress",
            "2020-11-01",
            "2020-12-31"
        )

        zadanie_id = add_zadanie(conn, zadanie)

        print(pr_id, zadanie_id)

        conn.commit()
        conn.close()
