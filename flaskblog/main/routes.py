import flask as fk
from flaskblog.model import Post

main=fk.Blueprint("main",__name__)

@main.route("/")
def homePage():
    page=fk.request.args.get("page",default=1,type=int)
    posts=Post.query.order_by(Post.date_post.desc()).paginate(page=page,per_page=5)
    return fk.render_template("home.html",posts=posts)

@main.route("/about")
def aboutPage():
    return fk.render_template("about.html")

