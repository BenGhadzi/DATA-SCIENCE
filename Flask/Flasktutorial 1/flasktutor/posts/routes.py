from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flasktutor import db
from flasktutor.models import Post
from flasktutor.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods = ['GET', 'POST']) #since we will need to accept post request, we need to add a GET, POST method to the route
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # To add a post to our database is similar to adding a user to the database but easier since we dont need to hash password
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash ('Your Post has been created!' 'success',)
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = 'New Post',
                            form=form, legend='New Post')

#We want to be able to delete posts. So create a route to single posts. variables within the route.
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) #get_or_404, means get the queried page and return 404 if it does not exist
    return render_template('post.html', title=post.title, post=post)

#Route to display the form to update a post
@posts.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: #check to make sure only the user who created the post can update it.
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # only commit not add since the post already exists.
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                            form=form, legend='Update Post') #create the links for this in the post template.

@posts.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: #check to make sure only the user who created the post can update it.
        abort(403)
    db.session.delete()
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

