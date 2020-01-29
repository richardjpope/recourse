from flask import request, redirect, render_template, url_for, session, flash
from recourse import app
from recourse import forms
from recourse import models

@app.route("/", methods=["GET"])
def index():
    if "case" in session:
        session.pop("case")
    return render_template('index.html')

@app.route("/report/what", methods=["GET", "POST"])
def report_what():

    if not "case" in session:
        case = models.Case()
        session["case"] = case.to_json()

    case = models.Case.from_json(session["case"])
    form = forms.What(request.form)
    form.type.choices = [(category.slug, category.name) for category in models.Category.objects().order_by('name')]

    if request.method == "GET":
        if case.category:
            form.type.data =  case.category.slug

    if request.method == "POST":
        if form.validate():
            case.category = models.Category.objects.get(slug=form.type.data)
            session["case"] = case.to_json()
            return redirect(url_for("report_harm"))

    return render_template("report/what.html", form=form)

@app.route("/report/harm", methods=["GET", "POST"])
def report_harm():

    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Harm(request.form)
    harms = models.Harm.objects(categories=case.category).order_by('title')
    form.harm.choices = [(harm.slug, harm.title) for harm in harms]
    for harm in harms:
        form.harm.option_hints[harm.slug] = {"text": harm.description}

    if request.method == "GET":
        if case.harm:
            form.harm.data = case.harm.slug

    if request.method == "POST":
        if form.validate():
            case.harm = models.Harm.objects.get(slug=form.harm.data)
            session["case"] = case.to_json()
            print(session["case"])
            return redirect(url_for("report_service"))

    return render_template("report/harm.html", form=form)

@app.route("/report/service", methods=["GET", "POST"])
def report_service():

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
            return redirect(url_for("report_who"))

    return render_template('report/service.html', form=form)

@app.route("/report/who", methods=["GET", "POST"])
def report_who():
 
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
            return redirect(url_for("report_rights"))

    return render_template('report/who.html', form=form)

@app.route("/report/rights", methods=["GET", "POST"])
def report_rights():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Escalate(request.form)

    if request.method == "GET":
        pass

    if request.method == "POST":
        if form.validate():
            session["case"] = case.to_json()
            return redirect(url_for("report_details"))

    return render_template('report/rights.html', form=form, case=case)

@app.route("/report/details", methods=["GET", "POST"])
def report_details():
 
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
            return redirect(url_for("report_outcome"))

    return render_template('report/details.html', form=form)

@app.route("/report/outcome", methods=["GET", "POST"])
def report_outcome():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Outcome(request.form)

    if request.method == "GET":
        form.description.data = case.outcome_description
   
    if request.method == "POST":
        if form.validate():
            case.outcome_description = form.description.data
            session["case"] = case.to_json()
            return redirect(url_for("report_contact"))

    return render_template('report/outcome.html', form=form)

@app.route("/report/contact", methods=["GET", "POST"])
def report_contact():
 
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
            return redirect(url_for("report_review"))

    return render_template('report/contact.html', form=form)

@app.route("/report/review", methods=["GET", "POST"])
def report_review():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.Review(request.form)
    if request.method == "POST" and form.validate():
        return redirect(url_for("report_confirmation"))

    return render_template('report/review.html', form=form, case=case)

@app.route("/confirmation", methods=["GET"])
def report_confirmation():
    if not "case" in session:
       return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    return render_template("report/confirmation.html", case=case)

#Page per thing
@app.route("/harms/", methods=["GET"])
def harm_index():

    harms = models.Harm.objects().order_by('title')
    return render_template("harms/index.html", harms=harms)


@app.route("/harms/<slug>", methods=["GET", "POST"])
def harm_item(slug):
    form = forms.HarmItem(request.form)
    return render_template("harms/harm.html", form=form)

#Static pages
@app.route("/about/documentation", methods=["GET"])
def about_documentation():
    return render_template("about/documentation.html")

#Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

