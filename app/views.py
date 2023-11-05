from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/developers')
def developers():
    return render_template('developers.html')

@app.route('/guides')
def guides():
    return render_template('guides.html')

@app.route('/program')
def program():
    return render_template('program.html')