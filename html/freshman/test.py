import cgi
import os
import sys
#sys.path.append("C:\Program Files\Google\google_appengine")
#import jinja2

#jinja_environment = jinja2.Environment(
#    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#from google.appengine.api import users

sys.stdout = sys.stderr

def get():
    
    template_values = {
        "title" : "JavaScript",
        "css"   :   "./css/basic.css",
        "homepagelink": "",
        }
    h = ""
    with open("./templates/index.html") as template:
        h = str(template.read())
        print(h)

    k = h.format(title = template_values["title"],css = template_values["css"],homepagelink = template_values["homepagelink"])
    print(k)
    #template = jinja_environment.get_template("../freshman/templates/index.html")        
    #print(template.render(template_values))


get()
