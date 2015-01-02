from google.appengine.ext import ndb

from google.appengine.api import users

import webapp2
import os
import urllib
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Todo(ndb.Model):
    task = ndb.StringProperty()
    complete = ndb.BooleanProperty()
    author = ndb.UserProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        
        if not current_user:
            self.redirect(users.create_login_url(self.request.uri))
        
        todo_query = Todo.query(Todo.author == current_user)
        todos = todo_query.fetch(10)
        
        template_values = {
            'todos': todos,
        }
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        current_user = users.get_current_user()
        if not current_user:
            self.redirect('/')
        todo = Todo()
        todo.task = self.request.get('txtTask')
        todo.complete = False
        todo.author = current_user
        todo.put()
        
        self.redirect('/')
        
        
class CompleteHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        if not current_user:
            self.redirect('/')
        id = int(self.request.get('id'))
        todo = Todo.get_by_id(id)
        todo.complete = True
        todo.put()
        
        self.redirect('/')


application = webapp2.WSGIApplication([
    ('/complete', CompleteHandler),
    ('/', MainPage),
], debug=True)