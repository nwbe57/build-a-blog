import webapp2
import cgi
import os
import re
import jinja2

from google.appengine.ext import db


#set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                            autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    title = db.StringProperty(required= True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, ID):

        post = Post.get_by_id(int(ID))

        self.response.write("<a href='/'>blog!</a><br><br>")
        self.response.write("<a href='/newpost'>enter new post</a>")
        self.response.write("<br><p style='font-size:30px'><strong>" + post.title + "</strong></p><br><br>" + post.post + "<br><br>")
        self.response.write("<br><br>created ")
        self.response.write(post.created)

class Blog(Handler):
    def render_blog(self, title="", created="", post=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")

        self.render("blog.html", title=title, created=created, post=post, posts=posts)

    def get(self):
        self.render_blog()

    def post(self):
        self.render_blog(posts)

class NewPost(Handler):
    def render_newpost(self, title="", post="", error=""):

        self.render("newpost.html", title=title, post=post, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")

        if title and post:
            a = Post(title=title, post=post)
            a.put()

            self.redirect("/blog/%s" %(a.key().id()))

        else:
            error = "we need both title and post"
            self.render_newpost(title, post, error)


app = webapp2.WSGIApplication([
    ('/newpost', NewPost),('/', Blog),webapp2.Route('/blog/<ID:\d+>', ViewPostHandler)
], debug=True)
