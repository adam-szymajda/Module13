from flask import Flask, request, url_for, render_template, redirect

from forms import TodoForm
from models import todos_sql

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/todos/", methods = ["GET", "POST"])
def todos_list():
    form = TodoForm()
    errors = ""

    create_todo_list_sql = """
    -- todos table
    CREATE TABLE IF NOT EXISTS todos (
        id integer PRIMARY KEY,
        title VARCHAR(150),
        description text NOT NULL,
        done text
    );
    """
    conn = todos_sql.db_connect()
    todos_sql.execute_sql(conn, create_todo_list_sql)

    if request.method == "POST":
        if form.validate_on_submit():
            # todos.create(form.data)
            todos_sql.create(conn, form.data)
            # todos.save_all()
        return redirect(url_for("todos_list"))

    print(todos_sql.all(conn))

    return render_template("todos.html", form=form, todos=todos_sql.all(conn), errors=errors)

@app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    conn = todos_sql.db_connect()

    # todo = todos.get(todo_id - 1)
    todo_sql =todos_sql.get(conn, id=todo_id)
    todo = {
            'title': todo_sql[0][1],
            'description': todo_sql[0][2],
            'done': todo_sql[0][3],
    }
    form = TodoForm(data=todo)
    if request.method == "POST":
        print(form.data)
        if form.validate_on_submit():
            todos_sql.update(conn, todo_id, form.data)
        return redirect(url_for("todos_list"))

    return render_template("todo.html", form=form, todo_id=todo_id)

if __name__ == "__main__":
    app.run(debug=True)
