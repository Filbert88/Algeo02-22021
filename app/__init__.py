from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/img/user'
app.config['DATASET_FOLDER'] = 'data/img/dataset'

from app import views
