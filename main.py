from flask import Flask, url_for, request, render_template, redirect
from markupsafe import escape 
from flask_sqlalchemy import SQLAlchemy
from typing import List
from flask_login import login_required


from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


# config
db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///e.db"

db.init_app(app)


#models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    __mapper_args__ = {'polymorphic_on': user_type}

    def __repr__(self):
        return "<User(username='%s', email='%s')>" % (
            self.username,
            self.email,
        )
    
#inheritance
class Customer(User):
    __tablename__ = 'customer'
    __mapper_args__ = { 
        'polymorphic_identity' : 'customer',
    }
    id = db.Column(db.String(32), db.ForeignKey('user.id'), primary_key=True)
    

class Driver(User):
    __tablename__ = 'driver'
    __mapper_args__ = { 
        'polymorphic_identity' : 'driver',
    }
    id = db.Column(db.String(32), db.ForeignKey('user.id'), primary_key=True)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kcal = db.Column(db.Integer)
    name = db.Column(db.String(32), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))


with app.app_context():
    db.create_all()

#logic
@app.route('/')
@app.route('/<name>')
def index(name=None):
    user = db.session.execute(db.select(User)).scalars()

    return render_template('index.html', name=user)

@app.get('/login')
def login_get():    
    return render_template('login.html')


@app.post('/login')
def login_post():
    
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()

    username=request.form['username']
    email=request.form["email"]
    
    user = Customer(
           user_type= 'customer',
           username=username,
           email=email,
      )
    db.session.add(user)
    db.session.commit()
    return render_template("index.html", name=user.username)
    

@app.get('/dashboard/<username>')
@app.get('/dashboard')
def dashboard_get():
    return render_template('dashboard.html', result=None)

@app.get('/order')
def order():
    return render_template('order.html', result=None)


@app.get('/payment')
def payment():
    return render_template('payment.html', result=None)

@app.get('/subscribe')
def subscribe():
    return render_template('subscribe.html', result=None)



@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login_get'))
    print(url_for('login_get', next='/'))
    print(url_for('profile', username='John Doe'))
    url_for('static', filename='style.css')
