from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    post = db.Column(db.Text)

    def __init__(self, title, post):
        self.title = title
        self.post = post

def filled_form(x):
    if x:
        return True
    else:
        return False


@app.route('/blog', methods=['GET'])
def all_blogs():
    select_id = request.args.get('id')
    if (select_id):
        select_post = Post.query.get(select_id)
        return render_template('select_post.html', select_post=select_post)
    else:
        blog_post = Post.query.all()
        return render_template('homepage.html', blog_post=blog_post)

@app.route('/newpost', methods=['POST', 'GET'])
def index():

    title_error = ''
    post_error = ''
    title = ''
    post = ''

    if request.method == 'POST':
        title = request.form['title']
        post = request.form['post']

    if not filled_form(title) and not filled_form(post):
        title_error = 'This field cannot be blank'
        post_error = 'This field cannot be blank'
        return render_template('newpost.html', title_error=title_error, post_error=post_error, title=title, post=post)

    elif not filled_form(title):
        title_error = 'This field cannot be blank'
        return render_template('newpost.html', title_error=title_error, title=title, post=post)
    
    elif not filled_form(post):
        post_error = 'This field cannot be blank'
        return render_template('newpost.html', post_error=post_error, title=title, post=post)

    else:
        new_entry = Post(title, post)
        db.session.add(new_entry)
        db.session.commit()
        post_page = "/blog?id=" + str(new_entry.id)
        return redirect(post_page)

if __name__ == '__main__':
    app.run()