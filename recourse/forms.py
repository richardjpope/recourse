from recourse import app
from flask_wtf import Form, FlaskForm
from flask_wtf.file import FileField
from wtforms import BooleanField, TextField, TextAreaField, RadioField, validators, ValidationError
from flask import render_template

class govukRadioField(RadioField):
    
    def __init__(self, label='', validators=None, is_page_heading=True, hint="", option_hints={}, **kwargs):
       super(govukRadioField, self).__init__(label, validators, **kwargs)
       self.is_page_heading =  is_page_heading
       self.hint = hint
       self.option_hints = option_hints

    def widget(self, field, **kwargs):
        items = []

        #error messages
        error_message = None
        if field.errors:
            error_message = {"text": " ".join(field.errors).strip()}

        #convert choices to ones govuk understands
        for choice in field.choices:
            checked = field.data == choice[0]
            hint = self.option_hints.get(choice[0], None)
            items.append({"value":choice[0], "text": choice[1], "checked": checked, "hint": hint})
        #convert to parameters that govuk understands
        label_classes = ""
        if self.is_page_heading:
            label_classes = "govuk-fieldset__legend--xl"
        params = {
                    "idPrefix": field.id, 
                    "name": field.name,
                    "hint": {
                        "text": self.hint,
                    },
                    "fieldset":{
                        "legend": {
                                "text": field.label.text,
                                "classes": label_classes,
                              },
                        },
                    "errorMessage": error_message,
                    "items": items,
                }
        return render_template('govuk-jinja-components/radios/template.jinja', params=params)

class govukTextField(TextField):
    
    def __init__(self, label='', validators=None, hint=None, **kwargs):
       super(govukTextField, self).__init__(label, validators, **kwargs)
       self.hint = hint
    def widget(self, field, **kwargs):

        #error messages
        error_message = None
        if field.errors:
            error_message = {"text": " ".join(field.errors).strip()}

        #convert to parameters that govuk understands
        params = {
                    "id": field.id, 
                    "name": field.name,
                    "label": {"text": field.label.text},
                    "value": field.data, 
                    "hint": self.hint,
                    "errorMessage": error_message,
                }
        return render_template('govuk-jinja-components/input/template.jinja', params=params)

class govukTextAreaField(TextAreaField):
    
    def __init__(self, label='', validators=None, hint=None, **kwargs):
       super(govukTextAreaField, self).__init__(label, validators, **kwargs)
       self.hint = hint
    def widget(self, field, **kwargs):

        #error messages
        error_message = None
        if field.errors:
            error_message = {"text": " ".join(field.errors).strip()}

        #convert to parameters that govuk understands
        params = {
                    "id": field.id, 
                    "name": field.name,
                    "label": {"text": field.label.text},
                    "value": field.data, 
                    "hint": self.hint,
                    "errorMessage": error_message,
                }
        return render_template('govuk-jinja-components/textarea/template.jinja', params=params)

class govukFileField(FileField):
    
    def __init__(self, label='', validators=None, hint=None, **kwargs):
       super(govukFileField, self).__init__(label, validators, **kwargs)
       self.hint = hint

    def widget(self, field, **kwargs):

        #error messages
        error_message = None
        if field.errors:
            error_message = {"text": " ".join(field.errors).strip()}

        #convert to parameters that govuk understands
        params = {
                    "id": field.id, 
                    "name": field.name,
                    "label": {"text": field.label.text},
                    "hint": self.hint,
                    "errorMessage": error_message,
                }
        return render_template('govuk-jinja-components/file-upload/template.jinja', params=params)



class What(FlaskForm):
    type = govukRadioField("What does your problem relate to?", [validators.Required(message="You need to choose an option")], hint="Choose the option that best describes your problem. If you are unsure, please choose \"other\"", choices=[])

class Harm(FlaskForm):
    harm = govukRadioField("What happened?", [validators.Required(message="You need to choose an option")], hint="Choose the option that best describes your problem. If you are unsure, please \"choose other\"", choices=[("foo", "foo"), ("bar", "bar")])


class Service(FlaskForm):
    service_name = govukTextField("Name of service or app", [validators.Required(message="Enter the name of a service, app or website")], {"text": "e.g. Facebook or Daily Mail"})

    url = govukTextField("or paste a URL", [])

class Who(Form):
    affected_party = govukRadioField(
            "Who did it affect?", 
            [validators.Required(message="You need to choose an option")], 
            choices=[("reporter", "You"), ("another", "Someone else"), ("everyone", "Everybody")], 
            option_hints={
                "reporter": {"text": "It is something that affected you directly"}, 
                "another": {"text": "For example, a friend, colleague or family member"}, 
                "everyone": {"text": "It has not affected a particular person, but is of general concern"}}
            )

class Escalate(Form):
    pass

class Details(FlaskForm):
    description = govukTextAreaField("Describe what happened", [validators.Required()], {"text":"Please give as much information as possible"})
    screenshot = govukFileField("Upload a screenshot (optional)")
    date_occured = govukTextField("When did it happen (optional)", [], {"text":"(e.g. “23/01”, “25 Jan”, or “last Monday”)"})

class Outcome(FlaskForm):
    description = govukTextAreaField("Describe what a good solution would look like to you", [validators.Required()], {"text":"Please give as much information as possible"})

class Contact(FlaskForm):
    name = govukTextField("Full name", [validators.Required()])
    email = govukTextField("Email address", [validators.Required(), validators.Email()])

class Review(Form):
    pass


