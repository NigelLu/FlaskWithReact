from flask import Flask, render_template, request, redirect, url_for
from forms import Todo
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = 'password'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tmp/test.db'
db = SQLAlchemy(app)

class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(240))

    def __str__(self):
        return f'{self.content}, {self.id}'

@app.route("/", methods=["GET"])
def index():
    todos = TodoModel.query.all()
    return render_template("home.html", name="Home", todos=todos)

@app.route("/<string:name>")
def hello_world(name, methods=["GET"]):
    return render_template("home.html", name=name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("---------------------")
        print(request.form['first_name']+" "+request.form['last_name']+" logged in!")
        print("---------------------")
    return render_template("login.html", method=request.method)

@app.route("/todo", methods=['GET', 'POST'])
def todo():
    todo_form = Todo()
    if todo_form.validate_on_submit():
        print("---------------------")
        print(todo_form.content.data)
        print("---------------------")
        temp_todo = TodoModel(content=todo_form.content.data)
        db.session.add(temp_todo)
        db.session.commit()
        return redirect('/')
    return render_template('todo.html', form=todo_form)

if __name__ == '__main__':
    app.run(debug=True)
