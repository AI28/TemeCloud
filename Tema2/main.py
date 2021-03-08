import os
import os.path
from subprocess import run
import sys

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
    
    web_app_startup = ["mod_wsgi-express", "start-server"]

    if "serve-front" in sys.argv:
        create_index()
        web_app_startup.append("--url-alias", "/static", "./static")

    web_app_startup.append("app.py")

    run(web_app_startup)

if __name__ == "__main__":
    main()
