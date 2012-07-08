import cgi
import webapp2
import os
import sys
import jinja2
import time

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.api import users
from google.appengine.ext import db

class resource(db.Model):
    """Models an url link"""
    categlory = db.StringProperty()
    description = db.StringProperty()
    url = db.StringProperty(multiline=True)
    
def generateSubPage(keyword):
    urldatas = db.GqlQuery("SELECT * FROM resource WHERE categlory = :1 ", keyword)
    results = urldatas.fetch(100)
    
    urlli = r"<ul>"
    for idx,urldata in enumerate(results):
        urlli += r"<li><a href =" + urldata.url + r">" + urldata.description + r"</li>"
    urlli += r"</ul>"
    template_values = {
        "title" : keyword,
        "css"   :  os.path.join(os.getcwd(),"css","basic.css"),
        "link_list"   :urlli,
        "homepagelink": "/",
        }
    k = ""
    with open("./templates/index.html") as template:
        h = str(template.read())

        k = h.format(title = template_values["title"],
                     css = template_values["css"],
                     link_list = template_values["link_list"],
                     homepagelink = template_values["homepagelink"])
    return k

class SubPage(webapp2.RequestHandler):
    def get(self):
        categlory = self.request.get("categlory")
        k = generateSubPage(categlory)
        self.response.out.write(k)

class MainPage(webapp2.RequestHandler):
    def get(self):
        k = self.generateMainPage()
        self.response.out.write(k)
    def generateMainPage(self):
        urldatas = db.GqlQuery("SELECT categlory FROM resource")
        results = urldatas.fetch(100)
    
        urlli = r"<ul>" +'\n'
        for idx,urldata in enumerate(results):
            urlli += r"<li><a action = '/subpage' method = 'get' name = 'categlory' value = " + urldata.categlory + r">" + urldata.categlory + r"</li>" + '\n'
        urlli += r"</ul>"
        template_values = {
            "title" : "",
            "css"   :  os.path.join(os.getcwd(),"css","basic.css"),
            "link_list"   :urlli,
            "homepagelink": "/",
        }
        
        k = ""
        with open("./templates/index.html") as template:
            h = str(template.read())

            k = h.format(title = template_values["title"],
                         css = template_values["css"],
                         link_list = template_values["link_list"],
                         homepagelink = template_values["homepagelink"])
        return k
    
    
class add_data(webapp2.RequestHandler):
    def post(self): 
        res = resource()
        res.categlory = self.request.get("categlory")
        res.url = self.request.get("link")
        res.description = self.request.get("description")
        if res.categlory and res.url and res.description:
            urldatas = db.GqlQuery("SELECT * FROM resource WHERE categlory = :1 AND url = :2", res.categlory,res.url)
            results = urldatas.get()
            if results == None:
                res.put()
            
        k = generateSubPage(res.categlory)
        self.response.out.write(k)   
            
app = webapp2.WSGIApplication([('/', MainPage),
                               ("/sign",add_data)],
                              debug=True)
