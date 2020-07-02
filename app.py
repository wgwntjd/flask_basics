import os
from flask import Flask, render_template, request, redirect
from models import db, Fcuser
from flask_wtf.csrf import CSRFProtect 
from forms import RegisterForm

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        userid = request.form.get('userid')
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        re_passwd = request.form.get('re-passwd')

        if (userid and username and passwd and re_passwd) and passwd == re_passwd:
            fcuser = Fcuser()
            fcuser.userid = userid
            fcuser.username = username
            fcuser.passwd = passwd

            db.session.add(fcuser)
            db.session.commit()

            return redirect('/')

    return render_template('register.html', form=form)

@app.route('/')
def hello():
    return render_template('hello.html')

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'qewrqwerqwrasdfasfasfafzv'

    csrf = CSRFProtect()

    csrf.init_app(app)
    db.init_app(app)
    db.app = app
    db.create_all()
    
    app.run(host='127.0.0.1', port=5000, debug=True)