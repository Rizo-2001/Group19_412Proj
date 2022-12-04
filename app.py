from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql+psycopg2://postgres:Password1!@localhost:5432/Yellowstone_Data_Logs')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Animals(db.Model):
    a_scientific_name = db.Column(db.String, primary_key=True)
    a_common_name=db.Column(db.String)
    diet=db.Column(db.String)
    mating_season=db.Column(db.String)
    population=db.Column(db.Integer)
    extinction_threat=db.Column(db.String)

    def __init__(self, a_scientific_name, a_common_name, diet, mating_season, population,  extinction_threat):
        self.a_scientific_name = a_scientific_name
        self.a_common_name = a_common_name
        self.diet = diet
        self.mating_season = mating_season
        self.population = population
        self.extinction_threat = extinction_threat

@app.route('/')
def index():
    animals = Animals.query.all()
    return render_template("index.html", animals = animals)

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        s_name = request.form['scientific_name']
        c_name = request.form['common_name']
        diet = request.form['diet']
        m_season = request.form['mating_season']
        population = request.form['population']
        endangerment = request.form['endangerment']


        my_data = Animals(s_name, c_name, diet, m_season, population, endangerment)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Animals.query.get(request.form.get('a_scientific_name'))

        my_data.a_scientific_name = request.form['a_scientific_name']
        my_data.a_common_name = request.form['a_common_name']
        my_data.diet = request.form['diet']
        my_data.m_season = request.form['mating_season']
        my_data.population = request.form['population']
        my_data.endangerment = request.form['endangerment']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('index'))

@app.route('/delete/<a_scientific_name>/', methods = ['GET', 'POST'])
def delete(a_scientific_name):
    my_data = Animals.query.get(a_scientific_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('index'))

#--------------Mammals-------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug = True, port=8000)