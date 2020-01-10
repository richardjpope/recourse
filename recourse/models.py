from datetime import datetime
from mongoengine import Document, StringField,EmailField,  IntField, DateTimeField, signals
from recourse import tasks
from recourse import app

class Case(Document):
    type = StringField()
    service_name = StringField()
    affected_party = StringField()
    details_description = StringField()
    outcome_description = StringField()
    contact_name = StringField()
    contact_email = EmailField()
