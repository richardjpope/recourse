from flask import request, redirect, render_template, url_for, session, flash
from recourse import app
from recourse import forms
from recourse import models
from recourse import tasks

@app.route("/", methods=["GET"])
def index():
    session.clear()
    return render_template('index.html')

@app.route("/report/what", methods=["GET", "POST"])
def what():

    if not "case" in session:
        case = models.Case()
        session["case"] = case.to_json()

    case = models.Case.from_json(session["case"])
    form = forms.What(request.form)

    if request.method == "GET":
        form.type.data =  case.type

    if request.method == "POST":
        if form.validate():
            case.type = form.type.data
            session["case"] = case.to_json()
            return redirect(url_for("service"))

    return render_template("what.html", form=form)

@app.route("/report/service", methods=["GET", "POST"])
def service():

    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Service(request.form)
    
    if request.method == "GET":
        form.service_name.data = case.service_name

    if request.method == "POST":
        if form.validate():
            case.service_name = form.service_name.data
            session["case"] = case.to_json()
            return redirect(url_for("who"))

    return render_template('service.html', form=form)

@app.route("/report/who", methods=["GET", "POST"])
def who():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Who(request.form)

    if request.method == "GET":
        form.affected_party.data = case.affected_party

    if request.method == "POST":
        if form.validate():
            case.affected_party = form.affected_party.data
            session["case"] = case.to_json()
            return redirect(url_for("rights"))

    return render_template('who.html', form=form)

@app.route("/report/rights", methods=["GET", "POST"])
def rights():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Escalate(request.form)

    if request.method == "GET":
        pass

    if request.method == "POST":
        if form.validate():
            session["case"] = case.to_json()
            return redirect(url_for("details"))

    return render_template('rights.html', form=form)

@app.route("/report/details", methods=["GET", "POST"])
def details():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Details(request.form)

    if request.method == "GET":
        form.description.data = case.details_description

    if request.method == "POST":
        if form.validate():
            case.details_description = form.description.data
            session["case"] = case.to_json()
            return redirect(url_for("outcome"))

    return render_template('details.html', form=form)

@app.route("/report/outcome", methods=["GET", "POST"])
def outcome():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Outcome(request.form)

    if request.method == "GET":
        form.description.data = case.outcome_description
   
    if request.method == "POST":
        if form.validate():
            case.details_description = form.description.data
            session["case"] = case.to_json()
            return redirect(url_for("contact"))

    return render_template('outcome.html', form=form)

@app.route("/report/contact", methods=["GET", "POST"])
def contact():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Contact(request.form)
 
    if request.method == "GET":
        form.name.data = case.contact_name
        form.email.data = case.contact_email
 
    if request.method == "POST":
        if form.validate():
            case.contact_name = form.name.data
            case.contact_email = form.email.data
            session["case"] = case.to_json()
            return redirect(url_for("review"))

    return render_template('contact.html', form=form)

@app.route("/report/review", methods=["GET", "POST"])
def review():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Review(request.form)
    if request.method == "POST" and form.validate():
        session["case"] = None
        return redirect(url_for("confirmation"))

    return render_template('review.html', form=form, case=case)

@app.route("/confirmation", methods=["GET"])
def confirmation():
    if not "case" in session:
       return redirect(url_for('index'))

    return render_template("confirmation.html")


