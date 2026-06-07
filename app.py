from flask import Flask,render_template
from models import db,Blog
from routes.auth import auth
from routes.blogs import blog
from routes.profile import profile
from PIL import Image
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'abc123'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)
with app.app_context():
    db.create_all()
    print("database created")
    
app.register_blueprint(auth)
app.register_blueprint(blog)
app.register_blueprint(profile)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/debug')
def debug():
    blogs = Blog.query.all()
    return str(blogs)

from sqlalchemy import text

@app.route('/raw')
def raw():
    result = db.session.execute(text("SELECT * FROM blog"))
    return str(list(result))


if __name__ ==  "__main__":
    print("Server is starting")
    app.run(debug=False,port=8000)