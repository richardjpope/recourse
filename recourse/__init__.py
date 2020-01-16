from flask import Flask, request, redirect, render_template, url_for
from flask.ext.mongoengine import MongoEngine
from mongoengine import NotUniqueError
from flaskext.markdown import Markdown
import jinja2
import os

app = Flask(__name__)
app.config.from_object(os.environ['SETTINGS'])
db = MongoEngine(app)
Markdown(app)

#Templates
multi_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.PrefixLoader({'govuk-jinja-components': jinja2.PackageLoader('govuk-jinja-components')})
    ])
app.jinja_loader = multi_loader

#Import everything else
from recourse import forms
from recourse import models
from recourse import views
