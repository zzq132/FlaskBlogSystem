import flask as fk
from flaskblog.model import Post
from flaskblog import db
from flaskblog.posts.forms import PostForm
from flask_login import current_user,login_required

posts=fk.Blueprint("posts",__name__)

@posts.route("/post/new",methods=["GET","POST"])
@login_required
def newPost():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        fk.flash("Your post has been created!","success")
        return fk.redirect(fk.url_for("main.homePage"))
    return fk.render_template("create_post.html",title="New Post",form=form,legend="New Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return fk.render_template("post.html",title=post.title,post=post)

@posts.route("/post/<int:post_id>/update",methods=["GET","POST"])
@login_required
def updatePost(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        fk.abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        fk.flash("Your post has been updated!","success")
        return fk.redirect(fk.url_for("posts.post",post_id=post_id))
    elif fk.request.method=="GET":
        form.title.data=post.title
        form.content.data=post.content
    return fk.render_template("create_post.html",title="Update Post",form=form,legend="Update Post")

@posts.route("/post/<int:post_id>/delete",methods=["GET","POST"])
@login_required
def deletePost(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        fk.abort(403)
    db.session.delete(post)
    db.session.commit()
    fk.flash("Your post has been deleted!","success")
    return fk.redirect(fk.url_for("main.homePage"))
