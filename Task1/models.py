import json
import sqlite3
from sqlite3 import Error

# class Todos:
#     def __init__(self):
#         try:
#             with open("todos.json", "r") as f:
#                 self.todos = json.load(f)
#         except FileNotFoundError:
#             self.todos=[]
#
#     def all(self):
#         return self.todos
#
#     def get(self, id):
#         return self.todos[id]
#
#     def create(self, data):
#         data.pop('csrf_token')
#         self.todos.append(data)
#
#     def save_all(self):
#         with open("todos.json", "w") as f:
#             json.dump(self.todos, f)
#
#     def update(self, id, data):
#         data.pop('csrf_token')
#         self.todos[id] = data
#         self.save_all()

class TodosSQL:
    def __init__(self):
        pass

    def db_connect(self):
        conn = None
        try:
            conn = sqlite3.connect("database.db")
            print(f"Connected to database, sqlite version: {sqlite3.version}")
            return conn
        except Error as e:
            print(e)

        return conn

    def execute_sql(self, conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def all(self, conn):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM todos")
        rows = cur.fetchall()

        return rows

    def get(self, conn, **query):
        cur = conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
           qs.append(f"{k}=?")
           values += (v,)
        q = " AND ".join(qs)
        cur.execute(f"SELECT * FROM todos WHERE {q}", values)
        rows = cur.fetchall()
        return rows

    def create(self, conn, data):
        data.pop('csrf_token')
        sql = '''INSERT INTO todos(title, description, done) VALUES(?, ?, ?)'''
        cur = conn.cursor()
        vals = (data['title'], data['description'], data['done'])
        cur.execute(sql, vals)
        conn.commit()
        return cur.lastrowid

    def update(self, conn, id, data):
        data.pop('csrf_token')
        parameters = [f"{k} = ?" for k in data]
        parameters = ", ".join(parameters)
        values = tuple(v for v in data.values())
        values += (id, )

        sql = f''' UPDATE todos
                 SET {parameters}
                 WHERE id = ?'''

        print(sql)
        try:
           cur = conn.cursor()
           cur.execute(sql, values)
           conn.commit()
           print("OK")
        except sqlite3.OperationalError as e:
           print(e)


# todos = Todos()
todos_sql = TodosSQL()
