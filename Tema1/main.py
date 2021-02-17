from os import getenv
import os.path
from subprocess import run

def create_index():

   with open("index.tpl", "r") as template:
       with open("index.html", "w") as index:
            
            tpl_string = template.read()
            api_key = os.getenv("GOOGLE_MAPS_KEY")
            index.write(tpl_string % api_key)


def main():
   
   if os.path.exists("index.html") is False:
       create_index()

   run(["mod_wsgi-express", "start-server", "app.py"])


if __name__ == "__main__":
    main()
