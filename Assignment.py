from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///playlists.db'
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    duration = db.Column(db.Integer, nullable=False)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class PlaylistSongs(db.Model):
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)

class SongForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    artist = StringField('Artist', validators=[DataRequired(), Length(max=100)])
    album = StringField('Album', validators=[Length(max=100)])
    genre = StringField('Genre', validators=[Length(max=50)])
    duration = IntegerField('Duration (seconds)', validators=[DataRequired()])
    submit = SubmitField('Add Song')

class PlaylistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Add Playlist')

@app.route('/')
def index():
    playlists = Playlist.query.all()
    return render_template('index.html', playlists=playlists)

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        song = Song(
            title=form.title.data,
            artist=form.artist.data,
            album=form.album.data,
            genre=form.genre.data,
            duration=form.duration.data
        )
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form, action="add_song")

@app.route('/add_playlist', methods=['GET', 'POST'])
def add_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        playlist = Playlist(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(playlist)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form, action="add_playlist")

if __name__ == '__main__':
    app.run(debug=True)
