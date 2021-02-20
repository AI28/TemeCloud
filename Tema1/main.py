import os
import os.path
from subprocess import run

def create_index():

    if os.path.exists("./static/") == False:
        os.mkdir("static")

    if os.path.exists("./static/index.html") == False:
        with open("index.tpl", "r") as template:
                    with open("./static/index.html", "w") as index:
                            tpl_string = template.read()
                            api_key = os.getenv("GOOGLE_MAPS_KEY")
                            index.write(tpl_string % api_key)


def main():
   
    create_index()
    run(["mod_wsgi-express", "start-server","--url-alias", "/static","./static", "app.py"])

if __name__ == "__main__":
    main()
