"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


        
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(1000))
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'    

class Post(db.Model):
        __tablename__='posts'
        post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        title = db.Column(db.String(70), nullable=False)
        content = db.Column(db.String(2000), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        

class PostTag(db.Model):
        __tablename__ = 'posts_tag'
        pt_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
        tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
        
        
class Tag(db.Model):
        __tablename__= 'tags'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String(15), nullable=False)
       
        posts = db.relationship('Post', secondary='posts_tag',backref="tags")



def connect_db(app):
        db.app = app
        db.init_app(app)    
        

        
if __name__ == "__main__":
    from app import app
    connect_db(app)

    db.drop_all()
    db.create_all()
