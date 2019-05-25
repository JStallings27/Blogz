from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzpass@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'ThisIsASecret'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    post = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'signup', 'homepage', 'index']
    if 'user' not in session and request.endpoint not in allowed_routes:
        return redirect('/login')

@app.route("/")
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route("/blog")
def homepage():
    blog_post = Blog.query.all()
    return render_template('homepage.html', blog_post=blog_post)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = user.username
            flash("Welcome back " + str(username))
            return redirect('/newpost')
        elif not user:
            flash("Username not found")
            return render_template("login.html", username=username)
        else:
            if not user.password == password:
                flash("Incorrect password")
                return render_template("login.html", username=username)
    elif 'user' in session:
        flash("You are already logged in")
        return redirect('/blog')
    else:
        return render_template("login.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        if username == "" or password == "" or verify == "":
            flash("Must complete all fields")
            return render_template("signup.html", username=username)
        elif username == existing_user:
            flash("Username is unavailable")
            return render_template("signup.html", username=username)
        elif len(username) < 3 or len(username) > 50:
            flash("Username must be between 3 - 50 characters")
            return render_template("signup.html", username=username)
        elif len(password) < 3 or len(password) > 120:
            flash("Password must be between 3 - 120 characters")
            return render_template("signup.html", username=username)
        elif verify != password:
            flash("Passwords must match")
            return render_template("signup.html", username=username)
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = new_user.username
            return redirect('/newpost')
    else:
        return render_template("signup.html")

@app.route('/select', methods=['GET'])
def select_blogs():
    select_id = request.args.get('id')
    if (select_id):
        select_post = Blog.query.get(select_id)
        return render_template('select_post.html', select_post=select_post)
    else:
        blog_post = Blog.query.all()
        return render_template('select_post.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    title_error = ''
    post_error = ''
    title = ''
    post = ''
    existing_user = User.query.filter_by(username=session['user']).first()

    if request.method == 'POST':
        title = request.form['title']
        post = request.form['post']
        owner = User.query.filter_by(username=session['user']).first()

        if title == "":
            flash("Every good blog deserves a title")
            return render_template('newpost.html', title=title, post=post)
        if post == "":
            flash("Your blog field is blank. What's wrong, cat got your tongue?")
            return render_template('newpost.html', title=title, post=post)
        else:
            new_entry = Blog(title, post, owner)
            db.session.add(new_entry)
            db.session.commit()
            post_page = "/select?id=" + str(new_entry.id)
            return redirect(post_page)
    else:
        return render_template("newpost.html")

@app.route('/logout')
def logout():
    flash("See you later")
    del session['user']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()