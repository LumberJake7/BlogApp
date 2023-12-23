# add_sample_data.py

from flask import Flask
from models import db, connect_db, User, Post, Tag, PostTag
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Establish the database connection
connect_db(app)

# Initialize app context
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create 5 users
        users_data = [
            {'first_name': 'John', 'last_name': 'Doe', 'image_url': 'https://static7.depositphotos.com/1298242/789/i/950/depositphotos_7894119-stock-photo-smiling-hispanic-man-headshot.jpg'},
            {'first_name': 'Jane', 'last_name': 'Smith', 'image_url': 'https://img.freepik.com/premium-photo/portrait-woman-glasses-standing-folded-her-hands_2221-5133.jpg'},
            {'first_name': 'Alice', 'last_name': 'Johnson', 'image_url': 'https://img.freepik.com/free-photo/portrait-expressive-young-woman_1258-48167.jpg?size=626&ext=jpg&ga=GA1.1.1546980028.1703116800&semt=ais'},
            {'first_name': 'Bob', 'last_name': 'Brown', 'image_url': 'https://as2.ftcdn.net/v2/jpg/02/19/63/31/1000_F_219633151_BW6TD8D1EA9OqZu4JgdmeJGg4JBaiAHj.jpg'},
            {'first_name': 'Eve', 'last_name': 'Williams', 'image_url': 'https://img.freepik.com/free-photo/close-up-shot-pretty-woman-with-perfect-teeth-dark-clean-skin-having-rest-indoors-smiling-happily-after-received-good-positive-news_273609-1248.jpg?w=1380&t=st=1703196770~exp=1703197370~hmac=5b86927297974fee5307ceee5dc23ced1bd219f403f6f8cd8274cb15e0c26f47'}
        ]
        users = []
        for user_data in users_data:
            new_user = User(**user_data)
            db.session.add(new_user)
            users.append(new_user)

        # Create 5 unique posts, each by a different user
        posts_data = [
            {'title': 'Post 1', 'content': 'Content of post 1'},
            {'title': 'Post 2', 'content': 'Content of post 2'},
            {'title': 'Post 3', 'content': 'Content of post 3'},
            {'title': 'Post 4', 'content': 'Content of post 4'},
            {'title': 'Post 5', 'content': 'Content of post 5'}
        ]
        posts = []
        for i, post_data in enumerate(posts_data):
            new_post = Post(title=post_data['title'], content=post_data['content'], user_id=users[i].id)
            db.session.add(new_post)
            posts.append(new_post)

        tags_data = [
            {'name': 'Tag 1'},
            {'name': 'Tag 2'},
            {'name': 'Tag 3'}
        ]
        tags = []
        for tag_data in tags_data:
            new_tag = Tag(**tag_data)
            db.session.add(new_tag)
            tags.append(new_tag)

        for post in posts:
            post_tags = random.sample(tags, 3) 
            post.tags.extend(post_tags)

        db.session.commit()

    app.run(debug=True)
