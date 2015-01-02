from google.appengine.ext import ndb


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


class MainPage(webapp2.RequestHandler):
    def get(self):
        todo_query = Todo.query()
        todos = todo_query.fetch(10)
        
        template_values = {
            'todos': todos,
        }
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        todo = Todo()
        todo.task = self.request.get('txtTask')
        todo.complete = False
        todo.put()
        
        self.redirect('/')
        
        
class CompleteHandler(webapp2.RequestHandler):
    def get(self):
        id = int(self.request.get('id'))
        todo = Todo.get_by_id(id)
        todo.complete = True
        todo.put()
        
        self.redirect('/')


application = webapp2.WSGIApplication([
    ('/complete', CompleteHandler),
    ('/', MainPage),
], debug=True)