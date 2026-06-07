from flask import Flask,request,render_template,redirect,flash,url_for,session,Blueprint
from models import db , User ,Blog
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash,generate_password_hash
from forms import Signupform,Loginform


auth = Blueprint('auth',__name__)

@auth.route('/signup',methods = ['POST','GET'])
def signup():
    form = Signupform()

    if form.validate_on_submit():
        name = form.username.data
        passkey = form.password.data

        hashed_password = generate_password_hash(passkey)

        user_object = User(username = name,password = hashed_password)

        try:
            db.session.add(user_object)
            db.session.commit()
            flash("Signed up sucessfully,Welcome to Blong 🤝 ")
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash("Failed to signup,try again ☹️")
    return render_template('Signup.html',form = form)
        
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Loginform()

    if form.validate_on_submit():
        Username = form.username.data
        Password = form.password.data

        user = User.query.filter_by(username = Username).first()

        if user and check_password_hash(user.password, Password):
            session['user'] = user.username
            session['user_id'] = user.id 
            flash("Login successful 👍 ")
            return redirect(url_for('blog.view_blog'))
        
    return render_template('login.html',form = form)

@auth.route('/logout', methods = ['Post','Get'])
def logout():
    session.clear()
    flash("logged out sucessfully")
    return redirect(url_for('auth.login'))

