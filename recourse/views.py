from flask import request, redirect, render_template, url_for, session, flash
from mongoengine import NotUniqueError
from recourse import app
from recourse import forms
from recourse import models
from recourse import tasks

@app.route("/", methods=["GET"])
def index():
    session["case"] = None
    return render_template("index.html")

@app.route("/report/what", methods=["GET", "POST"])
def what():
    form = forms.What(request.form)
    if request.method == "POST" and form.validate():
        session["case"] = None
        return redirect(url_for("service"))
    return render_template('what.html', form=form)

@app.route("/report/service", methods=["GET", "POST"])
def service():
    form = forms.Service(request.form)
    if request.method == "POST" and form.validate():
        session["case"] = None
        return redirect(url_for("who"))

    return render_template('service.html', form=form)

@app.route("/report/who", methods=["GET", "POST"])
def who():
    form = forms.Who(request.form)
    if request.method == "POST" and form.validate():
        session["case"] = None
        return redirect(url_for("rights"))

    return render_template('who.html', form=form)

@app.route("/report/rights", methods=["GET", "POST"])
def rights():
    form = forms.Escalate(request.form)
    if request.method == "POST" and form.validate():
        session["case"] = None
        return redirect(url_for("details"))

    return render_template('rights.html', form=form)

@app.route("/report/details", methods=["GET", "POST"])
def details():
    form = forms.Details(request.form)
    if request.method == "POST" and form.validate():
        session["case"] = None
        return redirect(url_for("outcome"))

    return render_template('details.html', form=form)

@app.route("/report/outcome", methods=["GET", "POST"])
def outcome():
    form = forms.Outcome(request.form)
    if request.method == "POST" and form.validate():
        session["case"] = None
        return redirect(url_for("contact"))

    return render_template('outcome.html', form=form)

@app.route("/report/contact", methods=["GET", "POST"])
def contact():
    form = forms.Contact(request.form)
    if request.method == "POST" and form.validate():
        session["case"] = None
        return redirect(url_for("review"))

    return render_template('contact.html', form=form)

@app.route("/report/review", methods=["GET", "POST"])
def review():
    form = forms.Review(request.form)
    if request.method == "POST" and form.validate():
        session["case"] = None
        return redirect(url_for("confirmation"))

    return render_template('review.html', form=form)

@app.route("/confirmation", methods=["GET"])
def confirmation():
    session["case"] = None
    return render_template("confirmation.html")


