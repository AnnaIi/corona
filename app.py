from flask import Flask
from data import db_session
from flask_login import LoginManager
from forms import *
from data.users import User
from flask_login import login_user
from flask import redirect
from flask import render_template
from flask.json import jsonify
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
db_session.global_init(DB_NAME)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html',
                           message="Неправильный логин или пароль",
                           api_key=YANDEX_API_KEY)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    страница авторизации пользователя
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            address=form.address.data,
            chatname=form.chatname.data
        )
        if not user.create_address(form.address.data):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="адрес неправильный")
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/api/points', methods=['GET', ])
def points():
    session = db_session.create_session()
    users = session.query(User)
    json_result = {
        "type": "FeatureCollection",
        "features": []
    }
    for user in users:
        json_result['features'].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    user.lat,
                    user.lon
                ]
            },
            "properties": {
                "balloonContent": f'<a href="/profile?id={user.id}">{user.address}</a>',
                "hintContent": user.email
            },
            "options": {
                "preset": "islands#circleIcon",
                "iconColor": "#ff0000" if user.is_ill else "#66ff00"
            }
        })
    return jsonify(json_result)


if __name__ == '__main__':
    app.run()