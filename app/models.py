from datetime import datetime
import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager
from markdown import markdown
from flask import current_app, request, url_for
import bleach
from flask_login import UserMixin, AnonymousUserMixin




class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.String(140))
    social_id = db.Column(db.String(140))
    gender = db.Column(db.String(5))
    contact_number = db.Column(db.Integer)
    education_level = db.Column(db.String(60))
    date_of_birth = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.relationship('Address', backref='Protagonist', lazy='dynamic')
    occumpation = db.relationship('Occupation', backref='Protagonist', lazy='dynamic')
    posts = db.relationship('Post', backref='Protagonist', lazy='dynamic')
    blog = db.relationship('Blog', backref = 'blog_author', lazy= 'dynamic')
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='Protagonist', lazy='dynamic')
    blog_comments = db.relationship('BlogComment', backref='blog_author', lazy='dynamic')
    links = db.relationship('Links', backref='Protagonist', lazy='dynamic')
    intrest = db.relationship('Intrest', backref='Protagonist', lazy='dynamic')
    achievement = db.relationship('Achievement', backref='Protagonist', lazy='dynamic')
    events = db.relationship('Events', backref='Protagonist', lazy='dynamic')
    travel = db.relationship('Travel', backref='Protagonist', lazy='dynamic')
    special_event = db.relationship('Special_event', backref='Protagonist', lazy='dynamic')
    media = db.relationship('Media', backref='Protagonist', lazy='dynamic')
    language = db.relationship('Language', backref='Protagonist', lazy='dynamic')
    sponsership = db.relationship('Sponsership', backref='Protagonist', lazy='dynamic')
    post_liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')
    comment_liked = db.relationship(
        'CommentLike',
        foreign_keys='CommentLike.user_id',
        backref='user', lazy='dynamic')
    blog_liked = db.relationship(
        'BlogLike',
        foreign_keys='BlogLike.user_id',
        backref='user', lazy='dynamic')
    blog_comment_liked = db.relationship(
        'BlogCommentLike',
        foreign_keys='BlogCommentLike.user_id',
        backref='user', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def like_comment(self, comment):
        if not self.has_liked_comment(comment):
            like = CommentLike(user_id=self.id, comment_id=comment.id)
            db.session.add(like)

    def unlike_comment(self, comment):
        if self.has_liked_comment(comment):
            CommentLike.query.filter_by(
                user_id=self.id,
                comment_id=comment.id).delete()

    def has_liked_comment(self, comment):
        return CommentLike.query.filter(
            CommentLike.user_id == self.id,
            CommentLike.comment_id == comment.id).count() > 0

    def like_blog(self, blog):
        if not self.has_liked_blog(blog):
            like = BlogLike(user_id=self.id, blog_id=blog.id)
            db.session.add(like)

    def unlike_blog(self, blog):
        if self.has_liked_blog(blog):
            BlogLike.query.filter_by(
                user_id=self.id,
                blog_id=blog.id).delete()

    def has_liked_blog(self, blog):
        return BlogLike.query.filter(
            BlogLike.user_id == self.id,
            BlogLike.blog_id == blog.id).count() > 0

    def like_blogcomment(self, blogcomment):
        if not self.has_liked_blogcomment(blogcomment):
            like = BlogCommentLike(user_id=self.id, blog_comment_id=blogcomment.id)
            db.session.add(like)

    def unlike_blogcomment(self, blogcomment):
        if self.has_liked_blogcomment(blogcomment):
            BlogCommentLike.query.filter_by(
                user_id=self.id,
                blog_comment_id=blogcomment.id).delete()

    def has_liked_blogcomment(self, blogcomment):
        return BlogCommentLike.query.filter(
            BlogCommentLike.user_id == self.id,
            BlogCommentLike.blog_comment_id == blogcomment.id).count() > 0




    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        self.follow(self)


    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)


    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')



    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)






    def __repr__(self):
        return f"User('{self.username}', '{self.user_id}', '{self.email}', '{self.image_file}', '{self.id}')"

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def has_liked_post(self, post):
        return False

    def has_liked_comment(self, comment):
        return False

    def has_liked_blog(self, blog):
        return False

    def has_liked_blogcomment(self, blogcomment):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    story_line = db.Column(db.String(500), nullable=False)
    story_text = db.Column(db.Text, nullable=False)
    youtube_link = db.Column(db.String(500), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')


    def __repr__(self):
        return f"Post('{self.Protagonist}', '{self.date_posted}')"



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    likes = db.relationship('CommentLike', backref='comment', lazy='dynamic')



    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    zip_code = db.column(db.text)
    country = db.Column(db.Text)

def __repr__(self):
        return f"Address('{self.Protagonist}', '{self.id}')"


class Occupation(db.Model):
    __tablename__ = 'occupation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    occupation_name = db.Column(db.Text)
    occupation_company = db.Column(db.Text)
    occupation_start_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
    occupation_end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)


def __repr__(self):
        return f"Occupation('{self.Protagonist}', '{self.occupation_company}', '{self.occupation_name}', '{self.id}' )"


class Links(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    facebook_id = db.Column(db.Text)
    twitter_id = db.Column(db.Text)
    instagram_id = db.Column(db.Text)
    snapchat_id = db.Column(db.Text)

def __repr__(self):
        return f"Links( '{self.Protagonist}' , '{self.facebook_id}', '{self.twitter_id}', '{self.instagram_id}', '{self.snapchat_id}' )"

class Intrest(db.Model):
    __tablename__ = 'intrest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    intrest_type = db.Column(db.Text)

def __repr__(self):
        return f"Intrest( '{self.Protagonist}', '{self.intrest_type}', '{self.intrest_names}' )"


class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medal_count = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

def __repr__(self):
        return f"Achievement('{self.medal}', '{self.medal_count}', '{self.Protagonist}' )"

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_name = db.Column(db.String)
    event_description = db.Column(db.String)
    event_location = db.Column(db.String)
    event_start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    event_end_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
    event_status = db.Column(db.Boolean)

def __repr__(self):
        return f"Events('{self.event_name_}', '{self.event_location}', '{self.event_status}', '{self.Protagonist}' )"

class Travel(db.Model):
    __tablename__ = 'travel'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    place = db.Column(db.String)
    start_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)

def __repr__(self):
        return f"Travel('{self.place}', '{self.Protagonist}' )"

class Special_event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    life_event = db.Column(db.String)
    life_event_start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    life_event_end_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)


def __repr__(self):
        return f"Special_event('{self.life_event}', '{self.Protagonist}')"

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    media_name = db.Column(db.String)
    media_format = db.Column(db.String)

def __repr__(self):
        return f"Media('{self.media_name}', '{self.media_name}', '{self.Protagonist}' )"

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    language = db.Column(db.String)
    language_accuracy = db.Column(db.String)

def __repr__(self):
        return f"Language('{self.language}', '{self.language_accuracy}', '{self.Protagonist}' )"

class Sponsership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sponser_type = db.Column(db.String)
    sponser_name = db.Column(db.String)
    sponsership_start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sponsership_end_date =  db.Column(db.DateTime, index=True, default=datetime.utcnow)

def __repr__(self):
        return f"Sponsership('{self.sponser_name}', '{self.sponser_type}', '{self.Protagonist}' )"



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_city = db.Column(db.String(50), nullable=False)
    blog_category = db.Column(db.String(50), nullable=False)
    blog_story_line = db.Column(db.String(500), nullable=False)
    blog_story_text = db.Column(db.Text, nullable=False)
    blog_youtube_link = db.Column(db.String(500), nullable=True)
    blog_date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    blogcomments = db.relationship('BlogComment', backref='blog', lazy='dynamic')
    likes = db.relationship('BlogLike', backref='blog', lazy='dynamic')


    def __repr__(self):
        return f"Blog('{self.blog_author}', '{self.date_posted}')"



class BlogComment(db.Model):
    __tablename__ = 'blogcomments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    likes = db.relationship('BlogCommentLike', backref='blogcomment', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(BlogComment.body, 'set', BlogComment.on_changed_body)


class PostLike(db.Model):
    __tablename__ = 'postlikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class CommentLike(db.Model):
    __tablename__ = 'commentlikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BlogLike(db.Model):
    __tablename__ = 'bloglikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BlogCommentLike(db.Model):
    __tablename__ = 'blogcommentlikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_comment_id = db.Column(db.Integer, db.ForeignKey('blogcomments.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
