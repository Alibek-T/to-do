from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Task, User
from api import City, Date, Temperature, Wind


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'v0q`jD3L!h`c*:0Tat4B-}Jm?aW('
db = SQLAlchemy(app)


def login_required(route):
    def decorated_route(*args, **kwargs):
        if not session.get("username"):
            return redirect('/login')
        return route(*args, **kwargs)
    return decorated_route


@app.route('/', methods=['GET'])
def main_page():
    return render_template('start.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        users = User.query.all()

        for one in users:
            if email == one.email and password == one.password:
                return redirect("/tasks")
            else:
                return "try again"


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")
    else:
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")

        if password == confirm_password:
            user = User(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
    return redirect("/tasks") #сделал таб


@app.route('/tasks')  #метод можно убрать
def home():
    task_list = Task.query.all() #поставил фильтр
    return render_template('tasks.html', task_list=task_list)


@app.route('/tasks/add', methods=['POST'])
def add():
    title = request.form.get('name')
    new_task = Task(title=title, status=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/tasks')


@app.route('/tasks/update/<int:task_id>')
def update(task_id):
    task = Task.query.filter_by(user_id=id).get(task_id)  #filter_by(user_id=user_id).
    task.status = not task.status
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/tasks/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/tasks')
def weather_data():
    city = City
    date = Date
    temperature = Temperature
    wind = Wind
    return render_template('tasks.html', City=city, Date=date, Temperature=temperature, Wind=wind)  #значения с большой были


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5002)
