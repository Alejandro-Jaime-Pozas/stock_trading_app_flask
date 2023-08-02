# this routes file will only have the main index route..nothing else needed for frontend, maybe use this to test flask?
from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return "<h1>this is a test, don't know if this will display visually in app, most prob not</h1>"