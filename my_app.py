import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, session, redirect, url_for
from flask import request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from flask_mail import Mail, Message
from threading import Thread




migrate = Migrate(app,db)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    
    msg = Message(app.config['MAIL_SENDER'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
    

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField("Submit")

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User', backref = 'role')

    def __repr__(self):
        return f'<Role {self.name}>'
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique = True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    

    def __repr__(self):
        return f'<User {self.username}>'

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User,Role=Role)


@app.route('/', methods=['GET', 'POST'])
def index():    
    
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known']= False
            if app.config['ADMIN']:
                print("Sending Email")
                send_email(
                    app.config['ADMIN'], 
                    'New User', 
                    'mail/new_user', 
                    user=user)
                print('Email sent!')
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', 
        form=form, name=session.get('name'),
        known = session.get('known', False)
    )

@app.route('/user/<name>')
def user(name):

    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def intenal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    
    app.run(debug=True)