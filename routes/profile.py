from flask import Flask,render_template,redirect,url_for,session,Blueprint,flash,request,current_app
from models import db,Profile,Blog
from utils.resizer import save_and_resize
from models import User
import os


profile = Blueprint('profile',__name__)



@profile.route('/profilepage')
def gotopro():
    userid = session.get('user_id')
    user = User.query.get(session.get('user_id'))
    blogs = Blog.query.filter_by(user_id = userid)
    return render_template('profile.html', user=user, blogs=blogs)

@profile.route('/update_profile',methods = ['POST'])
def upload_profile():
    file = request.files['profile_pic']

    if file:
        filename = file.filename
        save_and_resize(file,current_app.config['UPLOAD_FOLDER'],filename)

        
        existing_profile = Profile.query.filter_by(user_id=session.get('user_id')).first()


        try:
            if existing_profile:
                existing_profile.profile_pic = filename
            else:
                new_profile = Profile(username = session.get('user'),profile_pic = filename,user_id = session.get('user_id'))
                db.session.add(new_profile)
            db.session.commit()
            flash("profile uploaded sucessfully🎉")
            print("profile uploaded successfully")
        except Exception as e:
            print(e)
            flash("Failed to upload image")
    
    return redirect(url_for('profile.gotopro'))

@profile.route('/user_blog',methods = ['POST','GET'])
def single_user_blog():
    blog_id = request.args.get('id')
    user = session.get('user_id')

    if not blog_id:
        return 'invalid request'
    
    try:
        blog_id = int(blog_id)
    except:
        return "Invalid blog ID"

    if not user:
        flash("Login required")
        return redirect(url_for('auth.login'))
    
    single_blog = Blog.query.get(blog_id)

    if single_blog:
        filepath = os.path.join('static/files',single_blog.filename)

        try:
             with open(filepath,'r') as f:
                 content = f.read()
        except Exception as e:
            print(e)
            content = "Error loading file"


    return render_template('user_blog_view.html',single_blog = single_blog,content = content)


    