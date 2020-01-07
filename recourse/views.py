from flask import request, redirect, render_template, url_for, session, flash
from mongoengine import NotUniqueError
from recourse import app
import forms
import models
import tasks

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/report/service", methods=['GET', 'POST'])
def service():
    return render_template('service.html')


