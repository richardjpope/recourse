from flask.ext.script import Manager, prompt_bool
from recourse import app
from mongoengine import connect
import os
import yaml
import glob

manager = Manager(app)

@manager.command
def reset():
    "Delete all data, reset everything"
    if prompt_bool("Are you absolutely certain you want to delete all this things?"):

      #reset mongo
      db = connect(app.config['MONGODB_DB'], host=app.config['MONGODB_HOST'],  port=app.config['MONGODB_PORT'])
      db.drop_database(app.config['MONGODB_DB'])
      print("Deleted all collections from database ...")

      #reset celery
      #celery_discard_all()
      #print("Deleted all pending tasks from the message que ...")

      print("Done")

@manager.command
def importdata():
    "Import data from YAML files"
    if prompt_bool("Import YAML files and replace existing data?"):

        harms_directory ="%s/data/harms/" %  os.path.dirname(os.path.abspath(__file__))
        for file_path in glob.iglob("%s*.yaml" % harms_directory):
            with open(file_path) as f:
                data = yaml.safe_load(f)
                print(data)

        print("Done")

if __name__ == "__main__":
    manager.run()
