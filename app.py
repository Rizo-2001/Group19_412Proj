from email.policy import default
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
    return render_template('index.html')

@app.route('/animals')
def animals():
    animals = Animals.query.all()
    return render_template("animals.html", animals = animals)

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

        flash("Animal Inserted Successfully")

        return redirect(url_for('animals'))

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
        flash("Animal Updated Successfully")

        return redirect(url_for('animals'))

@app.route('/delete/<a_scientific_name>/', methods = ['GET', 'POST'])
def delete(a_scientific_name):
    my_data = Animals.query.get(a_scientific_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Animal Deleted Successfully")

    return redirect(url_for('animals'))

#--------------Mammals-------------------------------------------------------------------------
class Mammals(db.Model):
    m_scientific_name=db.Column(db.String, primary_key=True)
    m_common_name=db.Column(db.String)
    hibernates=db.Column(db.Boolean, default=False)
    offspring_count=db.Column(db.Integer)


    def __init__(self, m_scientific_name, m_common_name, hibernates, offspring_count):
        self.m_scientific_name = m_scientific_name
        self.m_common_name = m_common_name
        self.hibernates = hibernates
        self.offspring_count = offspring_count

@app.route('/mammals')
def mammals():
    mammals = Mammals.query.all()
    return render_template("mammals.html", mammals = mammals)

@app.route('/mammal_insert', methods = ['POST'])
def mammal_insert():

    if request.method == 'POST':
        is_checked = request.form.get('hibernates')
        if is_checked == 'on':
            checkbox_bool = True
        else:
            checkbox_bool = False
        s_name = request.form['scientific_name']
        c_name = request.form['common_name']
        offspring_count = request.form['offspring_count']


        my_data = Mammals(s_name, c_name, checkbox_bool, offspring_count)
        db.session.add(my_data)
        db.session.commit()

        flash("Mammal Inserted Successfully")

        return redirect(url_for('mammals'))

@app.route('/mammal_update/<m_scientific_name>/', methods = ['GET', 'POST'])
def mammal_update(m_scientific_name):

    if request.method == 'POST':
        my_data = Mammals.query.get(m_scientific_name)

        my_data.s_name = request.form['scientific_name']
        my_data.c_name = request.form['common_name']
        my_data.hibernates = request.form['hibernates']
        my_data.offspring_count = request.form['offspring_count']

        db.session.commit()
        flash("Mammal Updated Successfully")

        return redirect(url_for('mammals'))

@app.route('/mammal_delete/<m_scientific_name>/', methods = ['GET', 'POST'])
def mammal_delete(m_scientific_name):
    my_data = Mammals.query.get(m_scientific_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Mammal Deleted Successfully")

    return redirect(url_for('mammals'))

#--------------fish-------------------------------------------------------------------------
class Fish(db.Model):
    f_scientific_name=db.Column(db.String, primary_key=True)
    f_common_name=db.Column(db.String)
    minimum_catch_size=db.Column(db.Integer)
    legal_catch_season=db.Column(db.String)

    def __init__(self, f_scientific_name, f_common_name, minimum_catch_size, legal_catch_season):
        self.f_scientific_name = f_scientific_name
        self.f_common_name = f_common_name
        self.minimum_catch_size = minimum_catch_size
        self.legal_catch_season = legal_catch_season

@app.route('/fish')
def fish():
    fish = Fish.query.all()
    return render_template("fish.html", fish = fish)

@app.route('/fish_insert', methods = ['POST'])
def fish_insert():

    if request.method == 'POST':
        s_name = request.form['scientific_name']
        c_name = request.form['common_name']
        minimum_catch_size = request.form['minimum_catch_size']
        legal_catch_season = request.form['legal_catch_season']


        my_data = Fish(s_name, c_name, minimum_catch_size, legal_catch_season)
        db.session.add(my_data)
        db.session.commit()

        flash("Fish Inserted Successfully")

        return redirect(url_for('fish'))

@app.route('/fish_update', methods = ['GET', 'POST'])
def fish_update():

    if request.method == 'POST':
        my_data = Fish.query.get(request.form.get('f_scientific_name'))

        my_data.s_name = request.form['scientific_name']
        my_data.c_name = request.form['common_name']
        my_data.minimum_catch_size = request.form['minimum_catch_size']
        my_data.legal_catch_season = request.form['legal_catch_season']

        db.session.commit()
        flash("Fish Updated Successfully")

        return redirect(url_for('fish'))

@app.route('/fish_delete/<f_scientific_name>/', methods = ['GET', 'POST'])
def fish_delete(f_scientific_name):
    my_data = Fish.query.get(f_scientific_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Fish Deleted Successfully")

    return redirect(url_for('fish'))
#--------------trails-------------------------------------------------------------------------
class Trails(db.Model):
    trail_name=db.Column(db.String, primary_key=True)
    experience_level=db.Column(db.String)
    mile_length=db.Column(db.Numeric)
    elevation_peak_ft=db.Column(db.Integer)
    nearest_post_location=db.Column(db.String)

    def __init__(self, trail_name, experience_level, mile_length, elevation_peak_ft, nearest_post_location):
        self.trail_name = trail_name
        self.experience_level = experience_level
        self.mile_length = mile_length
        self.elevation_peak_ft = elevation_peak_ft
        self.nearest_post_location = nearest_post_location

@app.route('/trails')
def trails():
    trails = Trails.query.all()
    return render_template("trails.html", trails = trails)

@app.route('/trails_insert', methods = ['POST'])
def trails_insert():

    if request.method == 'POST':
        t_name = request.form['trail_name']
        experience_level = request.form['experience_level']
        mile_length = request.form['mile_length']
        elevation_peak_ft = request.form['elevation_peak_ft']
        nearest_post_location = request.form['nearest_post_location']


        my_data = Fish(t_name, experience_level, mile_length, elevation_peak_ft, nearest_post_location)
        db.session.add(my_data)
        db.session.commit()

        flash("Trail Inserted Successfully")

        return redirect(url_for('trails'))

@app.route('/trails_update', methods = ['GET', 'POST'])
def trails_update():

    if request.method == 'POST':
        my_data = Trails.query.get(request.form.get('f_scientific_name'))

        my_data.s_name = request.form['scientific_name']
        my_data.c_name = request.form['common_name']
        my_data.minimum_catch_size = request.form['minimum_catch_size']
        my_data.legal_catch_season = request.form['legal_catch_season']

        db.session.commit()
        flash("Trail Updated Successfully")

        return redirect(url_for('trails'))

@app.route('/trails_delete/<trail_name>/', methods = ['GET', 'POST'])
def trails_delete(trail_name):
    my_data = Trails.query.get(trail_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Trail Deleted Successfully")

    return redirect(url_for('trails'))
#--------------bird-------------------------------------------------------------------------
class Bird(db.Model):
    b_scientific_name=db.Column(db.String, primary_key=True)
    b_common_name=db.Column(db.String)
    migration=db.Column(db.String)
    coloration=db.Column(db.String)

    def __init__(self, b_scientific_name, b_common_name, migration, coloration):
        self.b_scientific_name = b_scientific_name
        self.b_common_name = b_common_name
        self.migration = migration
        self.coloration = coloration


#--------------geyser-------------------------------------------------------------------------
class Geysers(db.Model):
    geyser_name=db.Column(db.String, primary_key=True)
    average_height=db.Column(db.Integer)
    is_active=db.Column(db.Boolean)
    g_trail_name=db.Column(db.String)

    def __init__(self, geyser_name, average_height, is_active, g_trail_name):
        self.geyser_name = geyser_name
        self.average_height = average_height
        self.is_active = is_active
        self.g_trail_name = g_trail_name
#--------------rivers-------------------------------------------------------------------------
class Rivers(db.Model):
    river_name=db.Column(db.String, primary_key=True)
    depth=db.Column(db.Integer)
    river_length=db.Column(db.Integer)
    r_trail_name=db.Column(db.String)

    def __init__(self, river_name, depth, river_length, r_trail_name):
        self.river_name = river_name
        self.depth = depth
        self.river_length = river_length
        self.r_trail_name = r_trail_name
#--------------plants-------------------------------------------------------------------------
class Plants(db.Model):
    scientific_name=db.Column(db.String, primary_key=True)
    common_name=db.Column(db.String)
    poisonous=db.Column(db.Boolean)
    environment=db.Column(db.String)
    p_trail_name=db.Column(db.String)

    def __init__(self, scientific_name, common_name, poisonous, environment, p_trail_name):
        self.scientific_name = scientific_name
        self.common_name = common_name
        self.poisonous = poisonous
        self.environment = environment
        self.p_trail_name = p_trail_name

if __name__ == "__main__":
    app.run(debug = True, port=8000)