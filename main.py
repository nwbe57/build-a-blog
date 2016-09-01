
import webapp2

class Index(webapp2.RequestHandler):
    def get(self):


app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
