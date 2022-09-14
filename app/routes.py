# this routes file will only have the main index route..nothing else needed for frontend, maybe use this to test flask?
from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')
