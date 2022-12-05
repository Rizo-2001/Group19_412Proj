from email.policy import default
from os import environ
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from numpy import average, may_share_memory
from pkg_resources import safe_name

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql+psycopg2://postgres:Password1!@localhost:5432/Yellowstone_Data_Logs')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

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

@app.route('/delete/<a_scientific_name>/', methods = ['GET', 'POST'])
def delete(a_scientific_name):
    my_data = Animals.query.get(a_scientific_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Animal Deleted Successfully")

    return redirect(url_for('animals'))

@app.route('/endangerment_filter1', methods = ['GET', 'POST'])
def endangerment_filter1():
    animals = Animals.query.filter_by(extinction_threat = 'Least Concern').all()
    return render_template("animals.html", animals = animals)

@app.route('/endangerment_filter2', methods = ['GET', 'POST'])
def endangerment_filter2():
    animals = Animals.query.filter_by(extinction_threat = 'Not Endangered').all()
    return render_template("animals.html", animals = animals)

@app.route('/endangerment_filter3', methods = ['GET', 'POST'])
def endangerment_filter3():
    animals = Animals.query.filter_by(extinction_threat = 'Threatened').all()
    return render_template("animals.html", animals = animals)

@app.route('/endangerment_filter4', methods = ['GET', 'POST'])
def endangerment_filter4():
    animals = Animals.query.filter_by(extinction_threat = 'Most Endangered').all()
    return render_template("animals.html", animals = animals)

@app.route('/diet_filter1', methods = ['GET', 'POST'])
def diet_filter1():
    animals = Animals.query.filter_by(diet = 'Carnivore').all()
    return render_template("animals.html", animals = animals)

@app.route('/diet_filter2', methods = ['GET', 'POST'])
def diet_filter2():
    animals = Animals.query.filter_by(diet = 'Omnivore').all()
    return render_template("animals.html", animals = animals)

@app.route('/diet_filter3', methods = ['GET', 'POST'])
def diet_filter3():
    animals = Animals.query.filter_by(diet = 'Herbivore').all()
    return render_template("animals.html", animals = animals)
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

@app.route('/mammals/<m_scientific_name>/mammal_update', methods = ['POST', 'GET'])
def mammal_update(m_scientific_name):
    mammal = Mammals.query.filter_by(m_scientific_name = m_scientific_name).first()
    if request.method == 'POST':
        if mammal:
            db.session.delete(mammal)
            db.session.commit()

    return render_template('mammals.html')
        # my_data.m_scientific_name = request.form['m_scientific_name']
        # my_data.m_common_name = request.form['m_common_name']
        # my_data.hibernates = request.form['hibernates']
        # my_data.offspring_count = request.form['offspring_count']

        # db.session.commit()
        # flash("Mammal Updated Successfully")

        # return redirect(url_for('mammals'))

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

@app.route('/catch_filter1', methods = ['GET', 'POST'])
def catch_filter1():
    fish = Fish.query.filter_by(legal_catch_season = 'January-December').all()
    return render_template("fish.html", fish = fish)

@app.route('/catch_filter2', methods = ['GET', 'POST'])
def catch_filter2():
    fish = Fish.query.filter_by(legal_catch_season = 'Can\'t Catch').all()
    return render_template("fish.html", fish = fish)

@app.route('/catch_filter3', methods = ['GET', 'POST'])
def catch_filter3():
    fish = Fish.query.filter((Fish.legal_catch_season = 'January-December') | (Fish.legal_catch_season = 'Can\'t Catch')))
    return render_template("fish.html", fish = fish)
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


        my_data = Trails(t_name, experience_level, mile_length, elevation_peak_ft, nearest_post_location)
        db.session.add(my_data)
        db.session.commit()

        flash("Trail Inserted Successfully")

        return redirect(url_for('trails'))

@app.route('/trails_update', methods = ['GET', 'POST'])
def trails_update():

    if request.method == 'POST':
        my_data = Trails.query.get(request.form.get('f_scientific_name'))

        my_data.t_name = request.form['trail_name']
        my_data.exp_level = request.form['experience_level']
        my_data.mile_length = request.form['mile_length']
        my_data.elevation_peak = request.form['elevation_peak_ft']
        my_data.nearest_post = request.form['nearest_post_location']

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

@app.route('/birds')
def bird():
    bird = Bird.query.all()
    return render_template("birds.html", bird = bird)

@app.route('/bird_insert', methods = ['POST'])
def bird_insert():

    if request.method == 'POST':
        s_name = request.form['scientific_name']
        c_name = request.form['common_name']
        migration = request.form['migration']
        coloration = request.form['coloration']


        my_data = Bird(s_name, c_name, migration, coloration)
        db.session.add(my_data)
        db.session.commit()

        flash("Bird Inserted Successfully")

        return redirect(url_for('bird'))

@app.route('/bird_update', methods = ['GET', 'POST'])
def bird_update():

    if request.method == 'POST':
        my_data = Bird.query.get(request.form.get('b_scientific_name'))

        my_data.s_name = request.form['scientific_name']
        my_data.c_name = request.form['common_name']
        my_data.migraiton = request.form['migration']
        my_data.coloration = request.form['coloration']

        db.session.commit()
        flash("Bird Updated Successfully")

        return redirect(url_for('bird'))

@app.route('/bird_delete/<b_scientific_name>/', methods = ['GET', 'POST'])
def bird_delete(b_scientific_name):
    my_data = Bird.query.get(b_scientific_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Bird Deleted Successfully")

    return redirect(url_for('bird'))

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

@app.route('/geysers')
def geysers():
    geysers = Geysers.query.all()
    return render_template("geysers.html", geysers = geysers)

@app.route('/geysers_insert', methods = ['POST'])
def geysers_insert():

    if request.method == 'POST':
        is_checked = request.form.get('is_active')
        if is_checked == 'on':
            checkbox_bool = True
        else:
            checkbox_bool = False
        geyser_name = request.form['geyser_name']
        average_height = request.form['average_height']
        along_trail = request.form['along_trail']


        my_data = Geysers(geyser_name, average_height, checkbox_bool, along_trail)
        db.session.add(my_data)
        db.session.commit()

        flash("Geyser Inserted Successfully")

        return redirect(url_for('geysers'))

@app.route('/geysers_update', methods = ['GET', 'POST'])
def geysers_update():

    if request.method == 'POST':
        my_data = Geysers.query.get(request.form.get('geyser_name'))

        my_data.scientific_name = request.form['geyser_name']
        my_data.common_name = request.form['common_name']
        my_data.poisonous = request.form['poisonous']
        my_data.p_trail_name = request.form['along_trail']

        db.session.commit()
        flash("Plants Updated Successfully")

        return redirect(url_for('geysers'))

@app.route('/geysers_delete/<geyser_name>/', methods = ['GET', 'POST'])
def geysers_delete(geyser_name):
    my_data = Geysers.query.get(geyser_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Geyser Deleted Successfully")

    return redirect(url_for('geysers'))
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

@app.route('/rivers')
def rivers():
    rivers = Rivers.query.all()
    return render_template("rivers.html", rivers = rivers)

@app.route('/rivers_insert', methods = ['POST'])
def rivers_insert():

    if request.method == 'POST':
        river_name = request.form['river_name']
        depth = request.form['depth']
        river_length = request.form['river_length']
        along_trail = request.form['along_trail']


        my_data = Rivers(river_name, depth, river_length, along_trail)
        db.session.add(my_data)
        db.session.commit()

        flash("River Inserted Successfully")

        return redirect(url_for('rivers'))

@app.route('/rivers_update', methods = ['GET', 'POST'])
def rivers_update():

    if request.method == 'POST':
        my_data = Rivers.query.get(request.form.get('rivers_name'))

        my_data.river_name = request.form['river_name']
        my_data.depth = request.form['depth']
        my_data.river_length = request.form['river_length']
        my_data.r_trail_name = request.form['along_trail']

        db.session.commit()
        flash("River Updated Successfully")

        return redirect(url_for('rivers'))

@app.route('/rivers_delete/<river_name>/', methods = ['GET', 'POST'])
def rivers_delete(river_name):
    my_data = Rivers.query.get(river_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("River Deleted Successfully")

    return redirect(url_for('rivers'))
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

@app.route('/plants')
def plants():
    plants = Plants.query.all()
    return render_template("plants.html", plants = plants)


@app.route('/plants_insert', methods = ['POST'])
def plants_insert():

    if request.method == 'POST':
        is_checked = request.form.get('poisonous')
        if is_checked == 'on':
            checkbox_bool = True
        else:
            checkbox_bool = False
        s_name = request.form['scientific_name']
        c_name = request.form['common_name']
        environment = request.form['environment']
        along_trail = request.form['along_trail']


        my_data = Plants(s_name, c_name, checkbox_bool, environment, along_trail)
        db.session.add(my_data)
        db.session.commit()

        flash("Plant Inserted Successfully")

        return redirect(url_for('plants'))

@app.route('/plants_update', methods = ['GET', 'POST'])
def plants_update():

    if request.method == 'POST':
        my_data = Plants.query.get(request.form.get('scientific_name'))

        my_data.scientific_name = request.form['scientific_name']
        my_data.common_name = request.form['common_name']
        my_data.poisonous = request.form['poisonous']
        my_data.environment = request.form['environment']
        my_data.p_trail_name = request.form['along_trail']

        db.session.commit()
        flash("Plants Updated Successfully")

        return redirect(url_for('plants'))

@app.route('/plants_delete/<scientific_name>/', methods = ['GET', 'POST'])
def plants_delete(scientific_name):
    my_data = Plants.query.get(scientific_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Plants Deleted Successfully")

    return redirect(url_for('plants'))

@app.route('/poison_filter1', methods = ['GET', 'POST'])
def poison_filter1():
    
    animals = Plants.query.filter_by().all()
    return render_template("plants.html", animals = animals)

@app.route('/poison_filter2', methods = ['GET', 'POST'])
def poison_filter2():
    animals = Plants.query.filter_by(poisonous = False).all()
    return render_template("plants.html", animals = animals)

#--------------park_rangers-------------------------------------------------------------------------
class Park_Rangers(db.Model):
    ranger_name=db.Column(db.String, primary_key=True)
    age=db.Column(db.Integer)
    badge_num=db.Column(db.Integer)
    num_of_years_worked=db.Column(db.Integer)
    job_position=db.Column(db.String)
    post_location=db.Column(db.String)
    is_admin=db.Column(db.Boolean)
    userrname=db.Column(db.String)

@app.route('/park_rangers')
def park_rangers():
    park_rangers = Park_Rangers.query.all()
    return render_template("park_rangers.html", park_rangers = park_rangers)


@app.route('/park_rangers_insert', methods = ['POST'])
def park_rangers_insert():

        checkbox_bool = True
        username = 'aaa'
        ranger_name = request.form['park_ranger_name']
        age = request.form['age']
        badge_num = request.form['badge_num']
        num_of_years_worked = request.form['num_of_years_worked']
        job_position = request.form['job_position']
        post_location = request.form['post_location']


        my_data = Park_Rangers(ranger_name, age, badge_num, num_of_years_worked, job_position, post_location, checkbox_bool, username)
        db.session.add(my_data)
        db.session.commit()

        flash("Park Ranger Inserted Successfully")

        return redirect(url_for('park_rangers'))

@app.route('/park_rangers_update', methods = ['GET', 'POST'])
def park_rangers_update():

    if request.method == 'POST':
        my_data = Park_Rangers.query.get(request.form.get('park_ranger_name'))

        my_data.ranger_name = request.form['park_ranger_name']
        my_data.age = request.form['age']
        my_data.badge_num = request.form['badge_num']
        my_data.num_of_years_worked = request.form['num_of_years_worked']
        my_data.job_position = request.form['job_position']
        my_data.post_location = request.form['post_location']

        db.session.commit()
        flash("Park Ranger Updated Successfully")

        return redirect(url_for('park_rangers'))

@app.route('/park_rangers_delete/<park_ranger_name>/', methods = ['GET', 'POST'])
def park_rangers_delete(park_ranger_name):
    my_data = Park_Rangers.query.get(park_ranger_name)
    db.session.delete(my_data)
    db.session.commit()
    flash("Park Ranger Deleted Successfully")

    return redirect(url_for('park_rangers'))

if __name__ == "__main__":
    app.run(debug = True, port=8000)