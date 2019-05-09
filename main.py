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


@app.route('/blogs', methods=['GET'])
def all_blogs():
    blog_post = Post.query.all()

    return render_template('homepage.html', blog_post=blog_post)



@app.route('/add_blog', methods=['POST', 'GET'])
def index():

    new_blog = ''

    if request.method == 'POST':
        title = request.form['title']
        post = request.form['post']
        new_entry = Post(title, post)
        db.session.add(new_entry)
        db.session.commit()
        
    return render_template('/add_blog.html', new_blog=new_blog)

@app.route('/delete-post', methods=['POST'])
def delete_post():

    post_id = int(request.form['post-id'])
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()