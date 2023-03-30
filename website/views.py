from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from .models  import Movie
from . import db

views = Blueprint('views', __name__)
UPLOAD_FOLDER = 'website/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@views.route('/', methods=['GET', 'POST'])
def home():
    movies = Movie.query.all()
    return render_template("home.html", movies=movies)

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        title = request.form.get('title')
        poster = request.files['poster']
        description = request.form.get('description')

        if len(title) < 1:
            flash('Please enter a movie title.', category='error')
        elif len(description) < 1:
            flash('Please enter a movie description.', category='error')
        elif not poster:
            flash("Please upload a valid movie poster.", category='error')
        else:
            poster_filename = secure_filename(poster.filename)
            poster.save(os.path.join(app.config['UPLOAD_FOLDER']))
            new_movie = Movie(title=title, poster_filename=poster_filename, description=description)
            db.session.add(new_movie)
            db.session.commit()
            flash('Movie added.', category='success')
            return redirect(url_for('views.home'))

    return render_template("register.html")