from mongoengine import Document, ReferenceField, ListField, StringField, EmailField, IntField, DateTimeField, signals
from recourse import app

class Category(Document):
    name = StringField(required=True, unique=True)
    description = StringField(required=False)
    slug = StringField(required=True, unique=True)

class Harm(Document):
    title = StringField(required=True, unique=True)
    slug = StringField(required=True, unique=True)
    categories = ListField(ReferenceField(Category))
    support_groups = ListField(StringField())
    description = StringField()
    rights_markdown = StringField()
    support_markdown = StringField()

class Case(Document):
    harm = ReferenceField(Harm)
    category = ReferenceField(Category)
    service_name = StringField()
    affected_party = StringField()
    details_description = StringField(default="")
    outcome_description = StringField(default="")
    impact_description = StringField(default="")
    contact_name = StringField()
    contact_email = EmailField()