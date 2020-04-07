from flask import request, redirect, render_template, url_for, session, flash
from recourse import app
from recourse import forms
from recourse import models

def get_obj_or_404(cls, *args, **kwargs):
    try:
        return cls.objects.get(*args, **kwargs)
    except cls.DoesNotExist:
        raise Http404

@app.route("/", methods=["GET"])
def landing():
    return render_template('landing.html')

@app.route("/start", methods=["GET"])
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
    categories = models.Category.objects().order_by('name')
    form = forms.What(request.form)
    form.type.choices = [(category.slug, category.name) for category in categories]
    for category in categories:
        form.type.option_hints[category.slug] = {"text": category.description}


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
        if form.harm.data == None:
            form.harm.data = False
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
            if case.service_name.lower() == "msgr":
                return redirect(url_for("report_service_confirm"))
            else:
                return redirect(url_for("report_who"))

    return render_template('report/service.html', form=form)

@app.route("/report/service-confirm", methods=["GET", "POST"])
def report_service_confirm():

    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.ServiceConfirm(request.form)

    if request.method == "POST":
        if form.validate():
            session["case"] = case.to_json()
            return redirect(url_for("report_who"))

    return render_template('report/service_confirm.html', form=form)

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
            return redirect(url_for("report_impact_outcome"))

    return render_template('report/details.html', form=form, service_name=case.service_name)

@app.route("/report/impact-outcome", methods=["GET", "POST"])
def report_impact_outcome():
 
    if not "case" in session:
        return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    form = forms.ImpactOutcome(request.form)

    #hide impact if reporting harm not directly related to an individual
    if case.affected_party == "everyone":
        form.impact.validators = []
    #change label depending on effected party
    impact_label_text = form.impact.label.text
    if case.affected_party == "reporter":
        impact_label_text += " on you"
    elif case.affected_party == "another":
        impact_label_text += " on the person it happened to"
    form.impact.label.text = impact_label_text 

    if request.method == "GET":
        form.impact.data = case.impact_description
        form.outcome.data = case.outcome_description

    if request.method == "POST":
        if form.validate():
            case.impact_description = form.impact.data
            case.outcome_description = form.outcome.data
            session["case"] = case.to_json()
            return redirect(url_for("report_contact"))

    return render_template('report/impact_outcome.html', form=form, affected_party = case.affected_party, service_name = case.service_name)

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

    return render_template('report/contact.html', form=form, service_name=case.service_name)

@app.route("/report/review", methods=["GET", "POST"])
def report_review():
    
    if not "case" in session:
        return redirect(url_for('index'))
    
    case = models.Case.from_json(session["case"])
    summary = {"rows": [		
               {		
                 "key": {		
                  "text": "Description of the issue"		
                 },		
                 "value": {		
                   "text": case.details_description		
                 },		
                 "actions": {		
                   "items": [{		
                     "href": url_for("report_details"),		
                     "text": "Change",                    		
                     "visuallyHiddenText": "name"		
                   }]		
                 }		
               },		
               {		
                 "key": {		
                  "text": "What you would like to happen"		
                 },		
                 "value": {		
                   "text": case.outcome_description		
                 },		
                 "actions": {		
                   "items": [{		
                     "href": url_for("report_impact_outcome"),		
                     "text": "Change",                    		
                     "visuallyHiddenText": "name"		
                   }]		
                 }		
               }]		
           }
    if case.affected_party != "everybody":
        summary["rows"].append(
                {		
                 "key": {		
                  "text": "What was the impact"		
                 },		
                 "value": {		
                   "text": case.impact_description		
                 },		
                 "actions": {		
                   "items": [{		
                     "href": url_for("report_impact_outcome"),		
                     "text": "Change",                    		
                     "visuallyHiddenText": "name"		
                   }]		
                 }
                })

    summary["rows"].append({		
                 "key": {		
                  "text": "Name"		
                 },		
                 "value": {		
                   "text": case.contact_name		
                 },		
                 "actions": {		
                   "items": [{		
                     "href": url_for("report_contact"),		
                     "text": "Change",                    		
                     "visuallyHiddenText": "name"		
                   }]		
                 }		
               })
    summary["rows"].append(
               {		
                 "key": {		
                  "text": "Email"		
                 },		
                 "value": {		
                   "text": case.contact_email		
                 },		
                 "actions": {		
                   "items": [{		
                     "href": url_for("report_contact"),		
                     "text": "Change",                    		
                     "visuallyHiddenText": "name"		
                   }]		
                 }		
               })

    form = forms.Review(request.form)
    if request.method == "POST" and form.validate():
        return redirect(url_for("report_confirmation"))

    return render_template('report/review.html', form=form, summary=summary, case=case)

@app.route("/confirmation", methods=["GET"])
def report_confirmation():
    if not "case" in session:
       return redirect(url_for('index'))

    case = models.Case.from_json(session["case"])
    return render_template("report/confirmation.html", case=case)

#Page per thing
@app.route("/harms/", methods=["GET"])
def harm_index():
    data = []
    categories = models.Category.objects().order_by('name')
    for category in categories:
        harms = models.Harm.objects().filter(categories=category).order_by('title')
        data.append({'title': category.name, 'harms': harms})
    return render_template("harms/index.html", data=data)

@app.route("/harms/<slug>")
def harm_item(slug):
    harm = get_obj_or_404(models.Harm, slug=slug) 
    return render_template("harms/harm.html", harm=harm)

@app.route("/harms/<slug>/report")
def harm_report(slug):
    if "case" in session:
        session.pop("case")

    harm = get_obj_or_404(models.Harm, slug=slug) 
    case = models.Case()
    case.harm = harm
    case.category = harm.categories[0]
    
    session["case"] = case.to_json()

    return redirect(url_for('report_service'))

#Static pages
@app.route("/robots.txt", methods=["GET"])
def robots():
    return render_template("robots.txt")

@app.route("/about/companies", methods=["GET"])
def about_companies():
    return render_template("about/companies.html")

@app.route("/about/support-organisations", methods=["GET"])
def about_support_organisations():
    return render_template("about/about_support_organisations.html")

@app.route("/about/prototype", methods=["GET"])
def about_prototype():
    return render_template("about/prototype.html")

#Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
