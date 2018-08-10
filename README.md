# PopulationAnalysis
Website: [PopulationAnalysis](https://populationanalysis.herokuapp.com/)

Analysis of the data sets found at [https://data.gov.sg/](https://data.gov.sg/), the key topic of this analysis is the declining population and potential causes of it.

[Planning Document](https://github.com/woojiahao/pds-analysis/blob/master/planning.md)

## Installation Guide:
### Required Modules:
1. flask
2. flask-sqlalchemy
3. flask-migrate
4. SQLAlchemy
5. gunicorn 
6. numpy
7. matplotlib
8. pandas
9. psycopg2
10. python-dotenv

```bash
pip isntall flask flask-sqlalchemy flask-migrate sqlalchemy gunicorn numpy matplotlib pandas psycopg2 python-dotenv
```

**Explanation:**
* `flask` will be used to create the web page
* `flask-sqlalchemy` is a wrapper over `SQLAlchemy` to reduce overheard upfront for setting up SQLAlchemy to work with the Flask app
* `flask-migrate` is a module that assists with database migrations 
* `SQLAlchemy` is a Object Relational Mapper(ORM) that provides a layer of abstraction for the developer to reduce interaction with raw SQL and instead allow the developer to interact with the database through objects in Python
* `gunicorn` is Heroku's preferred library for running a Flask application on
* `numpy`, `matplotlib` and `pandas` these are all for the data science part of the application
* `psycopg2` is a wrapper to provide connectivity to the PostgreSQL database and it is used with `SQLAlchemy` and by extension of that, `flask-sqlalchemy`
* `python-dotenv` is used to provide support for `.env` files that the local copy of the application will be working on

### Pre-requisites:
1. PostgreSQL installed and setup for this project on your local machine, [guide here](https://github.com/woojiahao/pds-analysis/blob/master/readme.md#setting-up-postgres)
2. [Modules needed](https://github.com/woojiahao/pds-analysis#required-modules) 

You are able to load the application both on your local machine and on a Heroku server and the installation guide will go into detail on how to do both:

### Local Instance
1. Clone this repository and navigate into it
```bash
git clone https://github.com/woojiahao/pds-analysis.git
cd pds-analysis
```
2. If you have modified aspects of the postgres database, you will have to configure the `config.json`, and alter the `local_database_url` value to match the modified connection string, otherwise, if you followed the set-up guide for PostgreSQL earlier, then skip this step
```bash
cd pds-analysis
cd config 
vim config.json

{
    "local_database_url": "modified connection string"
}

:wq!
```
3. Now to load the data into the database from the `.csv` files
```bash
cd pds-analysis
flask shell

>>> manager = Manager()
>>> manager.load_data()
...
Data loaded
```
4. Verify that the database has the tables for `enrolment`, `gdp`, `mothers_occupation` and `live_births`, by opening pgAdmin and verifying that the database contains these tables and using the following queries to ensure that the data is correctly loaded:
```sql
SELECT * FROM enrolment;
SELECT * FROM gdp;
SELECT * FROM mothers_occupation;
SELECT * FROM live_births;
```
5. Run the application:
```bash
cd pds-analysis
flask run
```
6. Go to the localhost link, which should be: [http:localhost:5000/](http:localhost:5000/)

### Heroku instance
This guide will be broken down into 2 segments, the first for [setting up Heroku](https://github.com/woojiahao/pds-analysis#setting-up-heroku) and the second to [set up this application](https://github.com/woojiahao/pds-analysis#setting-up-application):

#### Setting up Heroku:
1. Install Heroku and the Heroku CLI to your local machine, in-depth instructions found [here](https://devcenter.heroku.com/articles/heroku-cli)
2. Clone this repository and navigate into it
```bash
git clone https://github.com/woojiahao/pds-analysis.git
cd pds-analysis
```
3. Create a heroku application for this repository, you can optionally specify a custom site name:
```bash
heroku create <optional custom name>
```
4. Verify that the set up is correct by making sure that there is now a `heroku` remote that your repository:
```bash
git remote -v

heroku  https://git.heroku.com/populationanalysis.git (fetch)
heroku  https://git.heroku.com/populationanalysis.git (push)
origin  https://github.com/woojiahao/pds-analysis (fetch)
origin  https://github.com/woojiahao/pds-analysis (push)
```
5. Run the `heroku addons` command and check that there is an add-on for `heroku-postgresql`, if you don't visit [this site](https://elements.heroku.com/addons/heroku-postgresql), and click on the `Install Heroku Postgres` button, you will then be prompted to enter the name of the application you wish to add the addon to, specify the name of the app previously created in step 3 and select `Provision add-on`
6. Verify that you are connected to the new PostgreSQL database provided by Heroku using `heroku config` and you should see that now there is an [environment variable](https://devcenter.heroku.com/articles/config-vars) for the database connection string

#### Setting up application:
1. After you have configured Heroku, push this repository to the `heroku` remote, you will see that Heroku handles all the installation and configuring of the needed modules specified in the [`requirements.txt`](https://github.com/woojiahao/pds-analysis/blob/master/requirements.txt) file
```bash
git push -u heroku master
```
2. Load the data into the Heroku database in this manner:
```bash
heroku run flask shell

>>> manager = Manager()
>>> manager.load_data()
...
Data loaded
```
3. Exit the flask shell:
```bash
>>> exit()
```
4. Activate the web [dyno](https://www.heroku.com/dynos) to start the website
```bash
heroku ps:scale web=1

Scaling dynos... done, now running web at 1:Free
```
5. Open the webpage
```bash
heroku open
```