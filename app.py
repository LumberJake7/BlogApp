"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
import random 
from random import sample


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        users_data = [
            {'first_name': 'John', 'last_name': 'Doe', 'image_url': 'https://static7.depositphotos.com/1298242/789/i/950/depositphotos_7894119-stock-photo-smiling-hispanic-man-headshot.jpg'},
            {'first_name': 'Jane', 'last_name': 'Smith', 'image_url': 'https://img.freepik.com/premium-photo/portrait-woman-glasses-standing-folded-her-hands_2221-5133.jpg'},
            {'first_name': 'Alice', 'last_name': 'Johnson', 'image_url': 'https://img.freepik.com/free-photo/portrait-expressive-young-woman_1258-48167.jpg?size=626&ext=jpg&ga=GA1.1.1546980028.1703116800&semt=ais'},
            {'first_name': 'Bob', 'last_name': 'Brown', 'image_url': 'https://as2.ftcdn.net/v2/jpg/02/19/63/31/1000_F_219633151_BW6TD8D1EA9OqZu4JgdmeJGg4JBaiAHj.jpg'},
            {'first_name': 'Eve', 'last_name': 'Williams', 'image_url': 'https://img.freepik.com/free-photo/close-up-shot-pretty-woman-with-perfect-teeth-dark-clean-skin-having-rest-indoors-smiling-happily-after-received-good-positive-news_273609-1248.jpg?w=1380&t=st=1703196770~exp=1703197370~hmac=5b86927297974fee5307ceee5dc23ced1bd219f403f6f8cd8274cb15e0c26f47'}
        ]

        # Create users
        users = [User(**user_data) for user_data in users_data]
        db.session.add_all(users)
        db.session.commit()

        # Create posts
        posts_data = [
            {'title': 'Post 1', 'content': 'Content of post 1'},
            {'title': 'Post 2', 'content': 'Content of post 2'},
            {'title': 'Post 3', 'content': 'Content of post 3'},
            {'title': 'Post 4', 'content': 'Content of post 4'},
            {'title': 'Post 5', 'content': 'Content of post 5'}
        ]

        posts = []
        for i, post_data in enumerate(posts_data):
            new_post = Post(title=post_data['title'], content=post_data['content'], user_id=users[i % len(users)].id)
            db.session.add(new_post)
            posts.append(new_post)

        db.session.commit()

        # Create tags
        tags_data = [
            {'name': 'Tag 1'},
            {'name': 'Tag 2'},
            {'name': 'Tag 3'}
        ]

        tags = [Tag(**tag_data) for tag_data in tags_data]
        db.session.add_all(tags)
        db.session.commit()

        # Assign random tags to posts
        for post in posts:
            post_tags = sample(tags, 2)  # Assigning 2 random tags per post
            post.tags.extend(post_tags)

        db.session.commit()

    app.run(debug=True)

@app.route('/')
def homepage():
    return redirect(url_for('list_users'))


"""User Routes"""

@app.route('/users')
def list_users():
      
      users = User.query.order_by(User.last_name, User.first_name).all()
      posts_with_user_names = db.session.query(Post, User).join(User).all()
      return render_template('home.html', users=users, posts_with_user_names=posts_with_user_names)


@app.route('/users/new', methods=['GET'])
def add_user_form():    
    return render_template('add_user.html',)


@app.route('/users/new', methods=['POST'])
def add_user():
    first_name = request.form['fname']
    last_name = request.form['lname']
    image_url = request.form['pimage']
    
    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('user_profile.html', user=user, user_posts=user_posts)


@app.route('/user/<int:user_id>/edit', methods=['GET'])
def user_profile_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form['pimage']

    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    if user:
        full_name = user.full_name()
    return render_template('posts/new.html', user=user, full_name=full_name,tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_new_post(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user_id=user.id,
                    tags=tags)
    
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f"/user/{user_id}")



"""route for posts"""


@app.route('/posts', methods=['GET'])
def list_posts():
    posts = Post.query.all()
    tags = Tag.query.all()
    return render_template('/posts/posts.html', posts=posts, tags=tags)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def posts_delete(post_id):
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/user/{post.user_id}')


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/show.html', post=post, post_id=post_id, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""
    tags = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    
    return render_template('posts/edit.html', post=post, post_id=post_id,tags=tags)



@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/user/{post.user_id}")



"""Routes for tags"""

@app.route('/tags', methods=['GET'])
def list_tags():
    tags = Tag.query.all()
    return render_template('tags/tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_link(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tag_info.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag_submit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    
    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/new')
def new_tag():
    return render_template('/tags/new.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    new_tag = Tag(name=request.form['name'])
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    db.session.delete(tag)
    db.session.commit()

    return redirect(f'/tags')
