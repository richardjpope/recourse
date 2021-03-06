from flask_script import Manager, prompt_bool
from recourse import app, models
from mongoengine import connect, DoesNotExist
from slugify import slugify
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
       
        #connect to database
        #db = connect(app.config['MONGODB_DB'], host=app.config['MONGODB_HOST'],  port=app.config['MONGODB_PORT'])       
        db = connect(app.config['MONGODB_HOST'])       

        #Get all the yaml files from the directory
        harms_directory ="%s/data/harms/" %  os.path.dirname(os.path.abspath(__file__))
        
        #categories
        unique_categories = []
        models.Category.objects().delete()

        for file_path in glob.iglob("%s*.yaml" % harms_directory):
            with open(file_path) as f:
                data = yaml.safe_load(f)
                for item in data["categories"]:
                    if not item in unique_categories:
                        unique_categories.append(item)

        for item in unique_categories:
            category = models.Category()
            category.name = item
            category.slug = slugify(item)
            category.save()

        #harms
        models.Harm.objects().delete()
        for file_path in glob.iglob("%s*.yaml" % harms_directory):
             with open(file_path) as f:
                data = yaml.safe_load(f)
                harm = models.Harm()
                harm.title = data["title"]
                harm.slug = slugify(data["title"])
                harm.description = data["description"]
                harm.rights_markdown = data["rights"]
                harm.support_markdown = data["support"]

                for item in data["categories"]:
                    try:
                        category = models.Category.objects.get(slug=slugify(item))
                        harm.categories.append(category)
                    except DoesNotExist:
                        pass

                try:
                    for item in data["report to"]:
                        try:
                            harm.support_groups.append(item)
                        except DoesNotExist:
                            pass
                except TypeError:
                    pass

                harm.save()
        
        #meta
        meta_directory ="%s/data/meta/" %  os.path.dirname(os.path.abspath(__file__))
        with open("%s/categories.yaml" % meta_directory) as f:
            data = yaml.safe_load(f)
            categories = models.Category.objects()
            for category in categories:
                category.description = data.get(category.name, None)
                category.save()


        print("Done")

if __name__ == "__main__":
    manager.run()
