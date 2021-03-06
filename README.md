#Recourse


* [Local development](#local-development)
* [Settings](#settings)
* [Running tests](#testing)
* [Importing data](importing data)

##Local development

This section describes how to get a development copy of Beckton working.

You must have the following things installed before you start

* [Node](https://nodejs.org/en/)
* [Python](https://www.python.org)
* [Virtualenv](https://virtualenv.pypa.io/en/stable/)
* [MongoDB](https://www.mongodb.com)


Clone this repository and install the requirements:

```
git clone git+https://github.com/richardjpope/recourse.git
cd recourse
virtualenv .
source bin/activate
pip install -r requirements.txt
npm install
```

To run recourse, you need to run several different things:

To run the web app:

```
source bin/activate
export SETTINGS='config.DevelopmentConfig'
python server.py
```

Run the assets compiler (in a separate terminal):

```
grunt
```

##Testing

To run the tests:

```
source bin/activate
export SETTINGS='config.TestingConfig'
python tests.py
```

##Importing data
```
python manage.py importdata
```
