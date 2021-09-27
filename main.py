from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
import requests
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///movies.db'
db = SQLAlchemy(app)

API_KEY = os.environ.get('MOVIES_API')




class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('Title', db.String(100), unique=True)
    year = db.Column('year', db.String )
    description = db.Column('description', db.String(1000))
    rating = db.Column('rating', db.Float())
    ranking = db.Column('ranking', db.Integer())
    review = db.Column('review', db.String(1000))
    img_url = db.Column('url', db.String(1000))
db.create_all()

class EditForm(FlaskForm):
    editrating = StringField('Edit Your Rating')
    editreview = StringField('Edit Review')
    submit = SubmitField('Done')

class Add(FlaskForm):
    name = StringField('Movie Title')
    add = SubmitField('Add')




@app.route("/", methods=['POST', 'GET'])
def home():

    all_data = Movies.query.order_by(Movies.rating).all()
    for i in range(len(all_data)):
        all_data[i].ranking = len(all_data) - i
    db.session.commit()
    return render_template("index.html", movies = all_data)

@app.route('/edit', methods=['POST', 'GET'])
def rate_movie():
    form = EditForm()
    movie = request.args.get("id")
    movies = Movies.query.get(movie)
    if form.validate_on_submit():
        movies.rating = float(form.editrating.data)
        movies.review = form.editreview.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',movies=movies , form=form)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    movie = request.args.get("id")
    movies = Movies.query.get(movie)
    db.session.delete(movies)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=['POST', 'GET'])
def add():
    form = Add()
    if form.validate_on_submit():
        parameters = {
            'api_key': API_KEY,
            'query': form.name.data
        }
        responce = requests.get('https://api.themoviedb.org/3/search/movie?', params=parameters)
        data = responce.json()

        return render_template('select.html', data=data['results'])
    return render_template('add.html', form=form)

@app.route('/find')
def find_movie():
    movie_id = request.args.get('id')
    print(movie_id)
    if movie_id:
        movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        parameters = {
            'api_key': API_KEY,

        }
        responce = requests.get(movie_url, params=parameters)
        data = responce.json()
        print(data)
        new_movie = Movies(
            title=data["original_title"],
            year=data["release_date"].split("-")[0],
            img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('rate_movie', id=new_movie.id))





if __name__ == '__main__':
    app.run(debug=True)
