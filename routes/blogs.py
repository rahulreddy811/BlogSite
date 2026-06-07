import uuid
from flask import Flask,request,render_template,redirect,flash,url_for,session,Blueprint
from models import db , Blog
from werkzeug.utils import secure_filename
from forms import BlogForm
import os

blog = Blueprint('blog',__name__)

@blog.route('/create',methods = ['GET','POST'])
def create_blog():
    form = BlogForm()

    if form.validate_on_submit():
        if not session.get('user_id'):
            flash("Login required")
            return redirect(url_for('auth.login'))
        blogtext = form.blogText.data
        filename = form.filename.data
        Title = form.title.data

        secured_filename = secure_filename(filename)

        unique_filename = f"{secured_filename}_{uuid.uuid4().hex}.txt"

        filepath = os.path.join('static/files',unique_filename)

        try:
            with open(filepath,'w') as f:
                f.write(blogtext)
            blog = Blog(filename = unique_filename,title = Title,username = session.get('user'),user_id = session.get('user_id') )
            db.session.add(blog)
            db.session.commit()
            flash("Blog Created sucessfully 🎉")   
            return redirect(url_for('blog.view_blog'))         
        except Exception as e:
            db.session.rollback()
            if os.path.exists(filepath):
                os.remove(filepath)
            print(e)
            flash("Error creating blog😭")

    return render_template('create.html',form = form)

@blog.route('/view',methods = ['GET','POST'])
def view_blog():
    blogs = Blog.query.all()
    print("BLOGS:", blogs)
    return render_template('mainpage.html',blogs=blogs)

@blog.route('/view_single',methods = ['POST','GET'])
def view_single():

    blog_id = request.args.get('id')

    if not session.get('user'):
        flash("Login required")
        return redirect(url_for('auth.login'))
    
    blog = Blog.query.get(blog_id)

    if not blog:
        return "Blog not found"

    if blog:
        filepath = os.path.join('static/files',blog.filename)
        
        try:
            with open(filepath,'r') as f:
                content = f.read()
        except Exception as e:
            print(e)
            content = "error loding the file"

    return render_template('view.html', blog=blog, content=content) 

        