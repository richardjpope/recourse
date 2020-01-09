from flask import Flask, request, redirect, render_template, url_for
from flask.ext.mongoengine import MongoEngine
from mongoengine import NotUniqueError
from celery import Celery
import jinja2
import os

app = Flask(__name__)
app.config.from_object(os.environ['SETTINGS'])

#Database
db = MongoEngine(app)

#Templates
multi_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.PrefixLoader({'govuk-jinja-components': jinja2.PackageLoader('govuk-jinja-components')})
    ])
app.jinja_loader = multi_loader

#Tasks
celery = Celery('app', broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
TaskBase = celery.Task

class ContextTask(TaskBase):
    abstract = True
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)
celery.Task = ContextTask

#Import everything else
from recourse import forms
from recourse import models
from recourse import views
