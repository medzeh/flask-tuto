from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email, Length

app=Flask(__name__)
bootstrap =  Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'anyMos14string'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,  primary_key=True)
    lastname = db.Column(db.String(15))
    firstname = db.Column(db.String(15))
    email = db.Column(db.String(15), unique=False)

    def __repr__(self):
        return 'User ' + str(self.id)

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    firstname = StringField('First Name', validators=[InputRequired(), Length(min=3, max=10)])
    lastname = StringField('Last Name', validators=[InputRequired(), Length(min=3, max=10)])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(firstname=form.firstname.data, email=form.email.data, lastname=form.lastname.data)
        db.session.add(new_user)
        db.session.commit()
        flash("New user has been created!")
        return redirect(url_for('index'))
    users= User.query.all()
    return render_template('index.html', form=form, users=users)




