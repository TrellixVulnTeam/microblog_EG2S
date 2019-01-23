from flask import (render_template, url_for, flash, request,
                   redirect, request, abort, current_app, make_response)
from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries
from app import db
from app.posts import bp
from app.models import Post, User, Comment, PostLike, CommentLike
from app.posts.forms import PostForm, CommentForm


@bp.route("/post/<int:id>", methods=['GET', 'POST'])
@login_required
def new_post(id):
    form = PostForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        post = Post(city=form.city.data,
                    category=form.category.data,
                    story_line=form.story_line.data,
                    story_text=form.story_text.data,
                    youtube_link=form.youtube_link.data,
                    Protagonist= user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('posts/create_post.html', title='New Post',
                           form=form, legend='New Post')


@bp.route("/postn/<int:post_id>",  methods=['GET', 'POST'])
def postn(post_id):
    post = Post.query.get_or_404(post_id)
    comment=Comment
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          Protagonist=current_user._get_current_object() )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.', 'success')
        return redirect(url_for('posts.postn', post_id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items

    return render_template('posts/post.html', story_line=post.story_line, posts=[post],post=post, form=form,
                              comments=comments, pagination=pagination, comment=comment)


@bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.city = form.city.data
        post.category = form.category.data
        post.story_line = form.story_line.data
        post.story_text = form.story_text.data
        post.youtube_link = form.youtube_link.data
        db.session.commit()
        flash(' post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.city.data = post.city
        form.category.data = post.category
        form.story_line.data = post.story_line
        form.story_text.data = post.story_text
        form.youtube_link.data = post.youtube_link
    return render_template('posts/create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required

def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('  post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@bp.route('/postlike/<int:post_id>/<action>')
@login_required
def postlike_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(url_for('posts.postn', post_id=post.id, page=-1))

@bp.route('/postcommentlike/<int:comment_id>/<action>')
@login_required
def postcommentlike_action(comment_id, action):
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    if action == 'like':
        current_user.like_comment(comment)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_comment(comment)
        db.session.commit()
    return redirect(url_for('main.home'))
